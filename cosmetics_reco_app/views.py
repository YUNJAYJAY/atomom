from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'main.html')
def skin_result(request):
    return render(request, 'skin_result.html')

def skin_select(request):
    return render(request, 'skin_select.html')

def cosmetics_result1(request):
    return render(request, 'cosmetics_result1.html')

def cosmetics_result2(request):
    return render(request, 'cosmetics_result2.html')

def cosmetics_result3(request):
    return render(request, 'cosmetics_result3.html')

def cosmetics_result4(request):
    return render(request, 'cosmetics_result4.html')

def cosmetics_result5(request):
    return render(request, 'cosmetics_result5.html')
