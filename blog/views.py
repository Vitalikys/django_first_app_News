from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.core.mail import send_mail
from django.views.generic.base import View
from hitcount.views import HitCountDetailView

from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactFormMail, ReviewForm
from .models import News, Category  # беремо таблицю
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import MyMixin
from django.core.paginator import Paginator
from blog.bs4_news_scraping import scraping_fun, ScrapingError


def register(request):
    if request.method == 'POST':  # приймаємо дані з форми
        # form = UserCreationForm(request.POST) replace to .forms-> UserRegisterForm
        #  можна залишити без створення в формі
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # щоб зразу зайти після реєстрацї
            messages.success(request, 'Registation success !')
            return redirect('home')
        else:
            messages.error(request, 'Error of registration')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def send_mail_test(request):
    if request.method == 'POST':
        form = ContactFormMail(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'gonevich91@ukr.net',
                             ['vitalikys87@i.ua'], fail_silently=False)
            if mail:
                messages.success(request, 'Mail success !!)')
                return redirect('send_mail_test')
            else:
                messages.error(request, 'oops, got send error')
        else:
            messages.error(request, 'Помилка валідації')
    else:
        form = ContactFormMail()
    return render(request, 'blog/send_mail_test.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# https://docs.djangoproject.com/en/4.0/topics/pagination/
class HomeNews(MyMixin, ListView):  # Контроллери class a
    ''' Головна сторінка, список всіх новин'''
    model = News
    mixin_prop = 'hello world'
    paginate_by = 3  # set number of items for pages/

    # queryset = News.objects.select_related('category')  те саме що знизу
    # template_name = news_list.html  it's-default.   we can create -'any_my.html'
    # context_object_name = 'news' variable for use instead default=object_list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page site'  # make sign on tab
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# .select_related() жадно загружає добавляємо щоб менше SQL запросів було на сторінці
#  працює з ForeignKey -model
# .prefetch_related()  - ManyToMany

# def index(request):  # Контроллери функцфї
#     #news = News.objects.all()
#     news = News.objects.order_by('-created_at')
#     #categories = Category.objects.all()
#     context = { #не обовязково
#             'news':news,
#             'title':'Cписок новин'   }
#     return render(request, template_name='blog/index.html', context=context )
#     #return HttpResponse('<h1> Hello wolrd</h1>')

class NewsByCategor(ListView):
    ''' Головна сторінка, фільтр новин по категоріях'''
    model = News
    template_name = 'blog/news_list.html'  # default var =object_list
    allow_empty = False  # to disable NULL categories in list
    paginate_by = 3  # set number of items for pages/

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])  # make sign on tab
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


'''def get_category(request, category_id):
    news= News.objects.filter(category_id = category_id)
    categor = Category.objects.get(pk = category_id)
    return render(request, 'blog/index.html', {'news':news, 'category':categor})
'''


class ViewNews(HitCountDetailView):
    ''' Одна новина детальний огляд '''
    model = News
    # pk_url_kwarg = 'news_id'
    template_name = 'blog/article_one_news.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    def get_object(self):  # count views+1
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


# def get_article(request, news_id):  # news_id беремо з urls.} get one news
#     news_item = News.objects.get(pk=news_id)
#     return render(request, 'blog/article_one_news.html', {'news_item':news_item })


class CreateNews(LoginRequiredMixin, CreateView):
    '''добавлення новини з сторінки'''
    form_class = NewsForm
    template_name = 'blog/add_news.html'
    login_url = '/admin/'  # redirect if not authorized
    # raise_exception = True   # exeption = if not authorized


# https://djbook.ru/rel3.0/topics/forms/index.html
'''
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
'''


def for_delete(request):
    ''' проста сторінка для всякого непотребу, можна видалити '''
    return render(request, 'blog/for_delete.html')


def scraping(request):
    ''' сторінка для парсингу новин з сайту Львів_Портал, скачує 4шт новини'''
    if request.method == 'POST' and request.user.is_staff:
        try:
            scraping_fun()
            messages.success(request, 'Добавлeння новин пройшло успішно !!)')
        except ScrapingError as err:
            print(str(err))
            return render(request, 'blog/scraping.html', {'message': str(err)})
    return render(request, 'blog/scraping.html', {'message': None})


@login_required(login_url=reverse_lazy('login'))
def delete_one_new(request, pk):
    ''' видалення одної новини '''
    obj = get_object_or_404(News, id=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, 'Видалення статті успішне.)')
        return redirect('home')
    return render(request, 'blog/deleting_one_article_form.html', {'obj': obj})


'''
@login_required(login_url=reverse_lazy('login'))
def delete_one_new(request,id):
   # видалення одної новини без переходу на форму підтвердження, зразу з home      
    obj = get_object_or_404(News, id=id)
    obj.delete()
    return redirect('home')
'''


class AddReview(View):
    """ Відгуки Отзиви
    Уроки Django 3 - ForeignKey self django ответ на отзыв - урок 10 #django school
    https://stackoverflow.com/questions/60497516/django-add-comment-section-on-posts-feed
    problem 1:
     частые запросы в БД из шаблона (не соблюдение MVC/MVT) и присваивание значений в джанго-форму из-за пределов формы (O в SOLID).

problem 2:
     Не совсем понятно, зачем делать class-based view для обработки пост-запроса, если можно сделать обычную вьюху,
      но ещё более странно, что  метод get_review добавляется в модель муви, если можно сделать более проще
      и универсальнее в моделе review проверку на наличие отца(если нет, то значит пишем в первый уровень),
    ну и ещё данный метод не учитывает ответы на ответ, поэтому можно добавить возможность писать ответы на ответ
    (привязывать отзыв к вложенному отзыву) и для получения всех вложенных отзывов использовать
     bfs-поиск(поиск по графу в ширину), где вершина наш отзыв без родителя и возвращаться будет набор всех отзывов-детей,
      ответов в этом отзыве. Грубо говоря, сделать как в вк, где в комментариях можно отвечать на комментарии,
      но смещение будет только на 1 уровень.
     """

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        news = News.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # призупиняємо
            if request.POST.get("parent", None):
                # якщо є "parent" то в нього, else = None 
                form.parent_id = int(request.POST.get("parent"))
            form.news = news
            form.save()
        return redirect(news.get_absolute_url())
