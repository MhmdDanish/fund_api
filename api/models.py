from django.db import models
from django.contrib.auth import get_user_model

class InvestmentFund(models.Model):
    fund_id = models.AutoField(primary_key=True) 
    fund_manager = models.CharField(max_length=255)  
    fund_name = models.CharField(max_length=255)
    fund_description = models.TextField()
    fund_nav = models.DecimalField(max_digits=20, decimal_places=2)
    fund_creation_date = models.DateField()
    fund_performance = models.FloatField(help_text="Performance in percentage")

    class Meta:
        db_table = "investment_funds"

    def __str__(self):
        return f"{self.fund_name} - Managed by {self.fund_manager}"
