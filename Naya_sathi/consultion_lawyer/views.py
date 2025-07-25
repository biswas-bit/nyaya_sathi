from django.shortcuts import render


def consult(request):
    return render(request,'consult.html')