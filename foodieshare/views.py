from django.shortcuts import render
from django.http import HttpResponse

def main_feed(request):
    return HttpResponse("FoodieShare says hey there partner!")