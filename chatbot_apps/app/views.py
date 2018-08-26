from django import forms

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext
from datetime import datetime

from app.models import User
from app.forms import UserForm
from app.predictor import Predictor

#from rest_framework.views import APIView
import csv
import pandas as pd
import datetime

chat_data = [['sentence','label']]
learning_data = [['sentence','label']]

class StaticClass:
    static_cnt = 0
    static_sentence_csv = pd.read_csv('learning_data.csv')
    static_reply_csv = pd.read_csv('reply.csv')

    def __init__(self, str):
        StaticClass.static_cnt += 1

    def get_sentence_csv(self):
        return static_sentence_csv[static_cnt]

    def get_reply_json_all(self):
        return static_reply_csv.to_json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def chat(request):
    assert isinstance(request, HttpRequest) #例外処理
    return render(
        request,
        'app/chat.html',
        {
            'title':'チャットページ'
        }
   )
    
def registryUser(request):
    assert isinstance(request, HttpRequest)
    userform = UserForm()
    return render(
        request,
        'app/registry.html',
        {
            'title':'登録',
            'user_form':userform,
        }
    )

def registryFriend(request):
    assert isinstance(request, HttpRequest)
    userform = UserForm()
    return render(
        request,
        'app/registry_friend.html',
        {
            'title':'登録',
            'user_form':userform,
        }
    )

def predict(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        sentence = request.GET.get('sentence')
        p = Predictor()
        result = p.execute(sentence)
        chat_data.append = [sentence,result['Label']]
        return HttpResponse(result['Words'])
    else:
        return HttpResponse("データが不正です")

def preserve(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        exit = request.GET.get('exit')
        if exit:
            date = datetime.datetime.now()
            file_date = date.year + date.month + date.day + date.hour + date.minute + date.second
            file_name = 'data'+ file_date +'.csv'
            chat_data.to_csv(file_name)
            print(file_name + "を作成しました")
    else:
        print("ERROR:CSVの書き込みに失敗しました")

def learning(request):
    assert isinstance(request, HttpRequest) #例外処理
    return render(
        request,
        'app/learning.html',
        {
            'title':'学習用ページ'
        }
   )

def training(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        return HttpResponse(StaticClass.get_sentence_csv())
    elif request.method == "POST";
        sentence = request.POST.get('sentence')
        label = request.POST.get('label')
        learning_data.append(sentence,label)
        

def reply(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        return HttpResponse(StaticClass.get_reply_json_all())