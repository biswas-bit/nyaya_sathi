from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import FIRReportForm, EvidenceImageFormSet
from .models import FIRReport, EvidenceImage
from .pdf_generator import download_fir_pdf

def report_fir(request):
    if request.method == 'POST':
        form = FIRReportForm(request.POST, request.FILES)
        evidence_formset = EvidenceImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and evidence_formset.is_valid():
            fir_report = form.save()
            
            # Save evidence images
            for evidence_form in evidence_formset:
                if evidence_form.cleaned_data and not evidence_form.cleaned_data.get('DELETE'):
                    if evidence_form.cleaned_data.get('image'):
                        evidence = evidence_form.save(commit=False)
                        evidence.fir_report = fir_report
                        evidence.save()
            
            pdf_url = reverse('fir:download_pdf', kwargs={'report_id': fir_report.id})
            messages.success(request, f'FIR Report submitted successfully! Report ID: {fir_report.id}. <a href="{pdf_url}" class="btn btn-sm btn-outline-primary ms-2">Download PDF</a>')
            return redirect('fir:report_fir')
    else:
        form = FIRReportForm()
        evidence_formset = EvidenceImageFormSet()
    
    return render(request, 'FIR/Report_FIR.html', {
        'form': form,
        'evidence_formset': evidence_formset
    })

def fir_list(request):
    reports = FIRReport.objects.all()
    return render(request, 'FIR/fir_list.html', {'reports': reports})

def download_pdf_view(request, report_id):
    fir_report = get_object_or_404(FIRReport, id=report_id)
    return download_fir_pdf(request, fir_report)
