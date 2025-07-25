from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return redirect('home_page:showcase', step=1)

@login_required
def showcase(request, step):
    features = [
        {
            'title': 'Legal Guidance for the Public',
            'description': 'Comprehensive legal assistance for various issues including police misconduct, domestic violence, accidents, and more.',
            'icon': '⚖️',
            'details': 'Get information about constitutional laws, past case studies, and statistics to understand and deal with legal issues effectively.'
        },
        {
            'title': 'Faster and Transparent FIR Process',
            'description': 'Streamlined FIR filing process with photo/video evidence upload and automatic report generation.',
            'icon': '📋',
            'details': 'Upload evidence, fill forms, and automatically generate FIR reports with relevant legal articles. Also helps with missing person reports.'
        },
        {
            'title': 'Anonymous Crime Reporting',
            'description': 'Secure anonymous reporting system to report crimes without fear of retaliation.',
            'icon': '🔒',
            'details': 'Upload videos or evidence anonymously. Reports are sent directly to news channels and legal authorities to ensure safety.'
        },
        {
            'title': 'Support for Ongoing Legal Cases',
            'description': 'Verify legal decisions and get second opinions for ongoing court cases.',
            'icon': '🏛️',
            'details': 'Get expert opinions on lawyer decisions, understand case progress, and ensure fair legal proceedings.'
        }
    ]
    
    max_step = len(features)
    
    if step < 1 or step > max_step:
        return redirect('home_page:showcase', step=1)
    
    current_feature = features[step - 1]
    is_last_step = step == max_step
    
    context = {
        'current_feature': current_feature,
        'current_step': step,
        'total_steps': max_step,
        'is_last_step': is_last_step,
        'next_step': step + 1 if not is_last_step else None,
        'progress_percentage': (step / max_step) * 100
    }
    
    return render(request, 'home_page/showcase.html', context)

@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'stats': {
            'cases_filed': 847,
            'firs_filed': 156,
            'successful_cases': 245,
            'total': 1248
        }
    }
    return render(request, 'home_page/dashboard.html', context)

@login_required
def feature_selection(request):
    return render(request, 'home_page/feature_selection.html')
