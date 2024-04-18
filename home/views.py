from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from home import models
from django.views.generic import ListView,UpdateView
# Create your views here.
from django.shortcuts import render
from django.views.generic import FormView
from datetime import date as dt
from .forms import TransactionForm
from .models import Transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail

from django.contrib.auth.views import LoginView
from creaditsaver.settings import EMAIL_ADMIN,EMAIL_HOST_USER


from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
@login_required
def index(request):
    result = None
    if request.method == 'POST':
        if 'cash_amount' not in request.POST and 'online_amount' not in request.POST and 'total_amount' not in request.POST:

            value = request.POST.get('value')
            if value.isalpha()==True:
                return render(request, 'index.html', {'result': "SYNTAX ERROR"})
            elif value == '00':
                return date(request)
            elif value =='404':
                logout(request)
                return redirect('login')
                

            elif value.endswith('+') or value.endswith('-') or value.endswith('.'):

                return TransactionUpdateView.as_view()(request, date=dt.today(), previous_result=value)
            else:
                result = calculator(value)
            return render(request, 'index.html', {'result': result})

        else:
            date1 = request.POST.get('date')
            cash_amount = request.POST.get('cash_amount')
            online_amount = request.POST.get('online_amount')
            total_amount = request.POST.get('total_amount', "No Transactions are available")

            send_mail(
            'Credits of the Day',
            f'\nDate: {date1}\nTotal Amount: {total_amount} Rs.\nCash Amount: {cash_amount} Rs.\nOnline: {online_amount} Rs.\n',
            EMAIL_HOST_USER,
            [EMAIL_ADMIN],
            fail_silently=False
            )

            return render(request, 'index.html', {'result': "EMAIL SENT"})

    return render(request, 'index.html')

 

from django.views.generic import View
from django.shortcuts import get_object_or_404
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin

class TransactionUpdateView(View,LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        try:
            date = kwargs.get('date')
            previous_result = kwargs.get('previous_result')

            # Convert previous_result to a string
            previous_result = str(previous_result)

            transaction = get_object_or_404(Transaction, date=date)
            result = None

            if previous_result.endswith('+'):
                previous_result_float = float(previous_result[:-1])
                previous_result_decimal = Decimal(previous_result_float)
                new_cash_amount = transaction.cash_amount + previous_result_decimal
                transaction.cash_amount = new_cash_amount
                transaction.save()
                result = f"Cash added {previous_result_float} Rs"

            elif previous_result.endswith('.'):
                previous_result_float = float(previous_result[:-1])
                previous_result_decimal = Decimal(previous_result_float)
                new_online_amount = transaction.online_amount + previous_result_decimal
                transaction.online_amount = new_online_amount
                transaction.save()
                result = f"Online added {previous_result_float} Rs"

            elif previous_result.endswith('-'):
                previous_result_float = float(previous_result[:-1])
                previous_result_decimal = Decimal(previous_result_float)
                new_cash_amount = transaction.cash_amount - previous_result_decimal
                transaction.cash_amount = new_cash_amount
                transaction.save()
                result = f"Cash reduced {previous_result_float} Rs"
            else:
                result="SYNTAX ERROR"

        except Exception as e:
            result = "SYNTAX ERROR"

        return render(request,'index.html',{'result': result})


from datetime import datetime
@login_required
def date(request):
    return render(request,'date.html')



class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        date_param = self.request.GET.get('date')
        if date_param:
            return Transaction.objects.filter(date=date_param)
        return Transaction.objects.none()  # Return an empty queryset if date_param is None

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception :
            # Handle the exception here
            return render(request, 'date.html', {'message': "Date format?? YYYY-MM-DD"})



class CustomLoginView(LoginView):
    template_name='login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('home')
    






def calculator(a):
    try:
        if round(eval(a),2)==0:
            return '0'
        else:
            return f"{a} = {round(eval(a),2)} "
    except Exception as e:
        return 'SYNTAX ERROR'