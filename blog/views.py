from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import NewsForm
from .models import News, Category  # беремо таблицю


def index(request):
    #news = News.objects.all()
    news = News.objects.order_by('-created_at')
    #categories = Category.objects.all()
    context = { #не обовязково
            'news':news,
            'title':'Cписок новин'   }
    return render(request, template_name='blog/index.html', context=context )
    #return HttpResponse('<h1> Hello wolrd</h1>')

def get_category(request, category_id):
    news= News.objects.filter(category_id = category_id)
    categor = Category.objects.get(pk = category_id)
    return render(request, 'blog/index.html', {'news':news, 'category':categor})
# Create your views here.


def get_article(request, news_id):  # news_id беремо з urls.}
    news_item = News.objects.get(pk=news_id)
    return render(request, 'blog/article_one_news.html', {'news_item':news_item })

# https://djbook.ru/rel3.0/topics/forms/index.html
def add_news(request):
    if request.method == 'POST':
        form= NewsForm(request.POST) # забираємо дані
        if form.is_valid():
            # print(form.cleaned_data) dict
            #News.objects.create(**form.cleaned_data) # це якщо прописуємо форму вручну
            # якщо Meta: model = News fields = '__all__ то просто: form.save()
            news_new = form.save()
            return redirect(news_new)
            #return redirect('home')
    else:
        form = NewsForm() #створ екземпл пустої форми
    return render(request, 'blog/add_news.html', {'form':form} )

def for_delete(request):
    return render(request, 'blog/for_delete.html')