from django.shortcuts import render

# Create your views here.
def crime_reports(request):
    return render(request,'crimes.html')