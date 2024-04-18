 
from django.urls import path
from home import views
from .views import TransactionListView,CustomLoginView

urlpatterns = [
    
    path('',CustomLoginView.as_view(),name='login'),
    path('home',views.index,name='home'),
    path('transaction/', TransactionListView.as_view(), name='transaction'),
     
  
]