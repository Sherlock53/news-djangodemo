from django.shortcuts import render,redirect
from django.views.generic.base import View
import json
import datetime
import random
# Create your views here.
from django.conf import settings as conf_settings

notfound = False
found_news =[]
class ComingSoonView(View):
    def get(self, request, *args,**kwargs):
        return redirect('/news')#render(request,'news/coming_soon.html')


class NewsContentView(View):
    def get(self, request, *args,**kwargs):
        list_id=kwargs['pk']
        news_data=self.readJson(list_id)
        return render(request,'news/news_detail.html',{'news_data': news_data})

    def readJson(self,pk):
        with open(conf_settings.NEWS_JSON_PATH) as news_file:
            data = json.load(news_file)
        for news in data:
            if int(news['link']) == pk:
                return news

class NewsMainView(View):
    def get(self, request, *args,**kwargs):
        news_data = self.readJson()

        if not request.GET.get('q') is None:
            search_title=request.GET.get('q')
            d = []
            if search_title != '':
                for news in news_data:
                    if search_title in news['title']:
                        d.append(news)
            news_data = d

        return render(request,'news/news_main.html',{'news_data': news_data})

    def readJson(self):
        with open(conf_settings.NEWS_JSON_PATH) as news_file:
            data = json.load(news_file)
        data.sort(reverse=True,key=lambda x: x.get('created'))
        for news in data:
            news['created'] = datetime.datetime.strptime(news['created'], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
        return data

class NewsCreateView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'news/news_create.html')

    def post(self,request,*args,**kwargs):
        news_title = request.POST.get('title')
        news_text = request.POST.get('news_text')
        created = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
        random.seed()
        link = random.randint(1,1000000)
        data=self.readJson()
        data.append({'created': created,'link': link,'text': news_text, 'title': news_title  })
        with open(conf_settings.NEWS_JSON_PATH,'w') as news_file:
            json.dump(data,news_file)
        return redirect('/news')
    def readJson(self):
        with open(conf_settings.NEWS_JSON_PATH) as news_file:
            data = json.load(news_file)
        return data