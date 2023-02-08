from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect

#ログイン時、投稿内容一覧表示画面に画面遷移
class TopView(TemplateView):

    def get(self,request):
        return redirect('testApp/')