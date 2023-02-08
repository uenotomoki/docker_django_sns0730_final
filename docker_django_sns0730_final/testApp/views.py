
#cd django202107/docker_django_sns/myproject
#cd django202107/github/pushtest/authtest/default_allauth
#python manage.py runserver

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import SnsMessageModel,SnsCommentModel
from .forms import SnsMessageForm,SnsCommentForm
from . import nexthtml
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import SnsMessageModel,SnsCommentModel
from .forms import SnsMessageForm,SnsCommentForm

#投稿内容一覧表示クラス
class TopView(TemplateView):
    def __init__(self):
        self.params = {
            'user':'',
            'data':'',
            'data_user':'',
            'data_comment_num':[],
        }

    #@login_required
    def get(self,request,num=1):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #ログインユーザー情報を取得
        user = request.user
        self.params['user'] = user

        #メッセージ情報の取得(ページネーション)
        data = SnsMessageModel.objects.all()
        page = Paginator(data,3)
        self.params['data'] = page.get_page(num)

        data_user = User.objects.all()
        page = Paginator(data_user,3)
        self.params['data_user'] = page.get_page(num)

        """
        #投稿記事に対してのコメント数表示
        for i in range(SnsMessageModel.objects.aggregate(Max('id'))['id__max'] + 1):
            if SnsMessageModel.objects.filter(id=i).count() != 0:
                snsmessagemodel_id = SnsMessageModel.objects.filter(id=i)
                self.params['data_comment_num'].append(SnsCommentModel.objects.filter(snsmessagemodel_id = snsmessagemodel_id[0]).count())
        """
        return render(request,'testApp/home.html',self.params)

    def post(self,request,num=1):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #ログインユーザー情報を取得
        user = request.user
        self.params['user'] = user

        #検索結果取得
        search = request.POST['search']
        data = SnsMessageModel.objects.filter(message__icontains=search)
        page = Paginator(data,3)
        self.params['data'] = page.get_page(num)

        #ユーザー情報取得
        self.params['data_user'] = User.objects.all()
        
        """
        #投稿記事に対してのコメント数表示
        for i in range(SnsMessageModel.objects.aggregate(Max('id'))['id__max'] + 1):
            if SnsMessageModel.objects.filter(id=i).count() != 0:
                snsmessagemodel_id = SnsMessageModel.objects.filter(id=i)
                self.params['data_comment_num'].append(SnsCommentModel.objects.filter(snsmessagemodel_id = snsmessagemodel_id[0]).count())
        """
        return render(request,'testApp/home.html',self.params)

#自分の過去に投稿した記事一覧
class MySnsShowView(TemplateView):
    def __init__(self):
        self.params = {
            'user':'',
            'data':'',
        }

    #@login_required
    def get(self,request):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #next.pyよりrender実行
        return nexthtml.RenderMysnsshow().rendermysnsshow(request)

    def post(self,request):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #next.pyよりrender実行
        return nexthtml.RenderMysnsshow().postrendermysnsshow(request)

#投稿記事に対してコメントを投稿
class SnsCommentView(TemplateView):
    def __init__(self):
        self.params = {
            'user':'',
            'form':SnsCommentForm(),
            'data':'',
        }

    def get(self,request,num):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #記事を投稿する
        self.params['data'] = SnsMessageModel.objects.get(id=num)
        self.params['data_user'] = User.objects.get(id=self.params['data'].user_id)
        return render(request,'testApp/snscommentcreate.html',self.params)

    def post(self,request,num):
        if not request.user.is_active:
            return redirect('/accounts/login/')
        
        snsmessagemodel_id = SnsMessageModel.objects.get(id=num)
        message = request.POST['message']
        snscreate = SnsCommentModel(snsmessagemodel_id = snsmessagemodel_id,message = message)
        snscreate.save()

        return redirect('snscommentindex', num=num)

#投稿記事に対してのコメント一覧表示
class SnsCommentIndex(TemplateView):
    def __init__(self):
        self.params = {
            'user':'',
            'form':SnsCommentForm(),
            'data_message':'',
            'data_comment':'',
            'num':''
        }

    #投稿記事に対してのコメント一覧表示
    def get(self,request,num):
        if not request.user.is_active:
            return redirect('/accounts/login/')

        #投稿記事に対してのコメント一覧取得
        self.params['num'] = num
        self.params['data_message'] = SnsMessageModel.objects.get(id=num)
        self.params['data_comment'] = SnsCommentModel.objects.filter(snsmessagemodel_id=self.params['data_message'])
        self.params['data_user'] = User.objects.get(id=self.params['data_message'].user_id)
        return render(request,'testApp/snscommentindex.html',self.params)

    #検索テキストボックスからpostを受け取る
    def post(self,request,num):
        if not request.user.is_active:
            return redirect('/accounts/login/')
        
        #コメント検索機能
        self.params['num'] = num
        self.params['data_message'] = SnsMessageModel.objects.get(id=num)
        search = request.POST['search']
        self.params['data_comment'] = SnsCommentModel.objects.filter(snsmessagemodel_id=self.params['data_message']).filter(message__icontains=search)
        self.params['data_user'] = User.objects.get(id=self.params['data_message'].user_id)
        return render(request,'testApp/snscommentindex.html',self.params)

#画像とコメントをアップロードするためのクラス
class SnsCreateView(TemplateView):
    def __init__(self):
        self.params = {
            'user':'',
            'form':SnsMessageForm(),
            'data':'',
        }

    def get(self,request):
        #ログインしていない場合ログイン画面に遷移
        if not request.user.is_active:
            return redirect('/accounts/login/')
        return render(request,'testApp/snscreate.html',self.params)

    def post(self,request):
        #ログインしていない場合ログイン画面に遷移
        if not request.user.is_active:
            return redirect('/accounts/login/')
        
        #アップロードされたコメントと画像をDB(SnsMessageModel)に保存
        user_id = request.user.id
        message = request.POST['message']
        picture = request.FILES['picture']
        snscreate = SnsMessageModel(user_id = user_id,message = message,picture = picture)
        snscreate.save()

        #next.pyよりrender実行、mysnsshow.htmlに遷移(自分の過去に投稿した記事一覧)
        return nexthtml.RenderMysnsshow().rendermysnsshow(request)

#投稿した記事を削除するクラス
class SnsDeleteView(TemplateView):
    def __init__(self):
        self.params = {
            'data':'',
        }

    #投稿した記事削除画面の遷移
    def get(self,request,num):
        self.params['data'] = SnsMessageModel.objects.get(id=num)
        return render(request,'testApp/snsdelete.html',self.params)
    
    #投稿した記事を削除実行
    def post(self,request,num):
        data = SnsMessageModel.objects.get(id=num)
        data.delete()
        #next.pyよりrender実行、mysnsshow.htmlに遷移(自分の過去に投稿した記事一覧)
        return nexthtml.RenderMysnsshow().rendermysnsshow(request)