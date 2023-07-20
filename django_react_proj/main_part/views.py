from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from gappers.models import Gappers
from gappers.models import Final
from gappers.models import Upperblock
from gappers.models import Results
from gappers.models import Script4
from gappers.models import Stock_counts


from django.utils import timezone
import json

def index(request):
     now = timezone.now()
     gappers = Gappers.objects.filter(date__date__gte=(now - timedelta(hours=24)).date())
     upperblocks = Upperblock.getcsv()
     finalresults = Final.getcsv()
     finalresultsjson =  finalresults.to_json()

     rdata = Results.getcsv()
     rjson=rdata.reset_index().to_json(orient ='records')
     results = json.loads(rjson)

     s4data= Script4.getcsv()
     s4json =  s4data.to_json()

     stock_counts = Stock_counts.getcsv()

     return render(request, "main_part/home.html", {"gappers":gappers,"upperblocks":upperblocks,"finalresults":finalresults, "finalresultsjson":finalresultsjson , "results":results ,"s4json":s4json, "stock_counts":stock_counts})
