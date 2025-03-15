from rest_framework import serializers
from .models import InvestmentFund

class InvestmentFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentFund
        fields = '__all__' 
        
class FundPerformanceSerializer(serializers.ModelSerializer):
     # Ensure it's required
    fund_performance = serializers.FloatField(required=True) 

    class Meta:
        model = InvestmentFund
        fields = ["fund_performance"]


