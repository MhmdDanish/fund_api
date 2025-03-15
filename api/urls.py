from django.urls import path
from .views import RetrieveListFund,CreateFund,RetrieveFund,UpdateFundPerformance,DeleteFund

urlpatterns = [
    path('list-funds/', RetrieveListFund.as_view(), name=RetrieveListFund.name), # Url to retrieve fund
    path('create-fund/', CreateFund.as_view(), name=CreateFund.name),  #Url to create fund
    path('get-fund/<int:fund_id>/', RetrieveFund.as_view(), name=RetrieveFund.name), #Url to retrieve fund by id 
    path('update-performance/<int:fund_id>/', UpdateFundPerformance.as_view(), name=UpdateFundPerformance.name), #Url to update performance by id 
    path('delete-fund/<int:fund_id>/', DeleteFund.as_view(), name=DeleteFund.name),  #Url to delete fund using id

]
