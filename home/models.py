from django.db import models

# Create your models here.
 
class Transaction(models.Model):
    date = models.DateField(auto_now_add=False)
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    online_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    @property
    def total_amount(self):
        return self.cash_amount + self.online_amount

    def __str__(self):
        return f"Date-{self.date}: Cash - {self.cash_amount:.2f}, Online - {self.online_amount:.2f}, Total - {self.total_amount:.2f}"


