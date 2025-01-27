from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

def home(request):
	return JsonResponse({"wha":"who"})

# def home(request):
# 	return HttpResponse("wha")
# Create your views here.
