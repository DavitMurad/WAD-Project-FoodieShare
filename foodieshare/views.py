from django.shortcuts import render
from django.http import HttpResponse

def main_feed(request):
    return render(request, 'foodieshare/main_feed.html')