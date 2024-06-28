from django.shortcuts import render,HttpResponse, redirect
import joblib
import psycopg2
import pandas as pd
import numpy as np
import json, os
from .models import EHR_project

# Create your views here.
def index(request):
    return render(request, "index.html")

#stage 5 modification of views.py
def result(request):
    model = joblib.load("models.joblib")  # We need to call the ML model here

    ############### Codes to get sex column in text #########
    sex_input = request.GET['sex'].lower() 
    if sex_input == 'male':
        sex_value = 1
    elif sex_input == 'female':
        sex_value = 0
    else:
        return HttpResponse("Invalid input for 'sex'. Please enter 'male' or 'female'.")
    
    ########################################################################   
    data_list = []  # Creating an empty list
    data_list.append(float(request.GET['HAEMATOCRIT']))
    data_list.append(float(request.GET['HAEMOGLOBIN']))
    data_list.append(float(request.GET['ERYTHROCYTE']))
    data_list.append(float(request.GET['LEUCOCYTE']))
    data_list.append(int(request.GET['THROMBOCYTE']))
    data_list.append(float(request.GET['MCH']))
    data_list.append(float(request.GET['MCHC']))
    data_list.append(float(request.GET['MCV']))
    data_list.append(int(request.GET['AGE']))
    data_list.append(sex_value)
    
    # Complete data present in list will be passed to ML model now
    answer = model.predict([data_list]).tolist()[0]  # This line will predict & display the result.
    rounded_answer = round(answer)  # Round the result to the nearest integer (0 or 1)
    
    # Determine the result message based on the rounded answer
    result_message = "inside_patient" if rounded_answer == 1 else "Out-patient"

    b = EHR_project(
        HAEMATOCRIT=request.GET['HAEMATOCRIT'], 
        HAEMOGLOBIN=request.GET['HAEMOGLOBIN'], 
        ERYTHROCYTE=request.GET['ERYTHROCYTE'],
        LEUCOCYTE=request.GET['LEUCOCYTE'], 
        THROMBOCYTE=request.GET['THROMBOCYTE'], 
        MCH=request.GET['MCH'],
        MCHC=request.GET['MCHC'], 
        MCV=request.GET['MCV'], 
        AGE=request.GET['AGE'], 
        SEX=sex_value,
    )
    b.save() 
    
    return render(request, "result.html", {'answer':result_message}) #result_message


