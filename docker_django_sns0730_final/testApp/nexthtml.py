from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import SnsMessageModel,SnsCommentModel
from .forms import SnsMessageForm,SnsCommentForm

#mysnsshow画面に遷移するクラス
class RenderMysnsshow:
    def __init__(self):
        self.params = {
            'user':'',
            'data':'',
        }

    #mysnsshow画面に遷移する前に必要な情報を取得し遷移
    def rendermysnsshow(self,request):
        user = request.user
        self.params['user'] = user
        self.params['data'] = SnsMessageModel.objects.filter(user_id=user.id).order_by('id').reverse()

        return render(request,'testApp/mysnsshow.html',self.params)

    #検索テキストボックスからmysnsshow画面に遷移する前に必要な情報を取得し遷移
    def postrendermysnsshow(self,request):

        #検索結果取得
        search = request.POST['search']
        
        user = request.user
        self.params['user'] = user
        self.params['data'] = SnsMessageModel.objects.filter(message__icontains=search).filter(user_id=user.id).order_by('id').reverse()

        return render(request,'testApp/mysnsshow.html',self.params)