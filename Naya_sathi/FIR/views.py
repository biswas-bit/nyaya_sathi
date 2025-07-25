from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FIRReportForm
from .models import FIRReport

def report_fir(request):
    if request.method == 'POST':
        form = FIRReportForm(request.POST, request.FILES)
        if form.is_valid():
            fir_report = form.save()
            messages.success(request, f'FIR Report submitted successfully! Report ID: {fir_report.id}')
            return redirect('fir:report_fir')
    else:
        form = FIRReportForm()
    
    return render(request, 'FIR/Report_FIR.html', {'form': form})

def fir_list(request):
    reports = FIRReport.objects.all()
    return render(request, 'FIR/fir_list.html', {'reports': reports})
