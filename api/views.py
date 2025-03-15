from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InvestmentFundSerializer, FundPerformanceSerializer
from .models import InvestmentFund

#Retrieve All Funds (GET)
class RetrieveListFund(generics.GenericAPIView):
    serializer_class = InvestmentFundSerializer
    name = "retrieve-list-fund"

    def get(self, request, *args, **kwargs):
        # Retrieve all funds with a message if none exist.
        funds = InvestmentFund.objects.all()
        if not funds.exists():
            return Response(
                {"message": "No investment funds available."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(funds, many=True)
        return Response(
            {"total_funds": funds.count(), "funds": serializer.data},
            status=status.HTTP_200_OK
        )

# Retrieve Specific Fund (GET)
class RetrieveFund(generics.GenericAPIView):
    serializer_class = InvestmentFundSerializer
    name = "retrieve-fund"

    def get(self, request, fund_id, *args, **kwargs):
        # Retrieve a specific fund by ID.
        fund = get_object_or_404(InvestmentFund, fund_id=fund_id)
        serializer = self.get_serializer(fund)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create Fund (POST)
class CreateFund(generics.GenericAPIView):
    serializer_class = InvestmentFundSerializer
    name = "create-fund"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Investment fund created successfully!", "fund": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Update Fund Performance (POST)
class UpdateFundPerformance(generics.GenericAPIView):
    serializer_class = FundPerformanceSerializer
    name = "update-fund-performance"

    def post(self, request, fund_id, *args, **kwargs):
        fund = get_object_or_404(InvestmentFund, fund_id=fund_id)

        # Check if request data is empty
        if not request.data:
            return Response(
                {"error": "No fund_performance provided."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(fund, data=request.data, partial=True)

        # Identify required fields that are missing
        required_fields = [
            field_name for field_name, field in serializer.fields.items()
            if field.required and field_name not in request.data
        ]
        
        if required_fields:
            return Response(
                {"error": "Missing required fields", "fields": required_fields},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Fund performance updated successfully!", "fund": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete Fund Data (POST) 
class DeleteFund(generics.GenericAPIView):
    queryset = InvestmentFund.objects.all()
    serializer_class = InvestmentFundSerializer
    lookup_field = "fund_id"
    name = "delete-fund"

    def post(self, request, fund_id, *args, **kwargs):
        try:
            #Here to fetch the api
            fund = InvestmentFund.objects.get(fund_id=fund_id) 
            fund.delete()
            return Response(
                {"message": "Investment fund deleted successfully!"},
                status=status.HTTP_200_OK
            )
        except InvestmentFund.DoesNotExist:
            return Response(
                {"error": "Investment fund not found."},
                status=status.HTTP_404_NOT_FOUND
            )
