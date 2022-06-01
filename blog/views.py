from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from .forms import NewsForm
from .models import News, Category  # беремо таблицю
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import MyMixin

class HomeNews(MyMixin, ListView):
    model = News
    mixin_prop = 'hello world'
    # template_name = news_list.html  it's-default.   we can create -'any_my.html'
    # context_object_name = 'news' variable for use instead default=object_list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page site'   # make sign on tab
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

# def index(request):
#     #news = News.objects.all()
#     news = News.objects.order_by('-created_at')
#     #categories = Category.objects.all()
#     context = { #не обовязково
#             'news':news,
#             'title':'Cписок новин'   }
#     return render(request, template_name='blog/index.html', context=context )
#     #return HttpResponse('<h1> Hello wolrd</h1>')

class HomeAltGrid(ListView):
    model = News
    template_name = 'blog/home_altern_grid.html'


class NewsByCategor(ListView):
    model = News
    template_name = 'blog/news_list.html'  # default var =object_list
    allow_empty = False # to disable NULL categories in list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk= self.kwargs['category_id'])  # make sign on tab
        return context
    def get_queryset(self):
        return News.objects.filter( category_id= self.kwargs['category_id'] , is_published=True)

# def get_category(request, category_id):
#     news= News.objects.filter(category_id = category_id)
#     categor = Category.objects.get(pk = category_id)
#     return render(request, 'blog/index.html', {'news':news, 'category':categor})
# # Create your views here.

class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    template_name = 'blog/article_one_news.html'
# def get_article(request, news_id):  # news_id беремо з urls.} get one news
#     news_item = News.objects.get(pk=news_id)
#     return render(request, 'blog/article_one_news.html', {'news_item':news_item })


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'blog/add_news.html'
    login_url = '/admin/'  # redirect if not authorized
    # raise_exception = True   # exeption = if not authorized

# https://djbook.ru/rel3.0/topics/forms/index.html
# def add_news(request):
#     if request.method == 'POST':
#         form= NewsForm(request.POST) # забираємо дані
#         if form.is_valid():
#             # print(form.cleaned_data) dict
#             #News.objects.create(**form.cleaned_data) # це якщо прописуємо форму вручну
#             # якщо Meta: model = News fields = '__all__ то просто: form.save()
#             news_new = form.save()
#             return redirect(news_new)
#             #return redirect('home')
#     else:
#         form = NewsForm() #створ екземпл пустої форми
#     return render(request, 'blog/add_news.html', {'form':form} )

def for_delete( request):
    return render(request, 'blog/for_delete.html')