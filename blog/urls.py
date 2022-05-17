from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('article/<int:news_id>/', get_article, name='article_detail_url'),
    path('article/add-news', add_news, name= 'add_news'),
    path('article/extra_del', for_delete, name= 'for_delete'),

]