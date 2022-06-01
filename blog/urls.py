from django.urls import path
from .views import *


urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('article/home_alt/', HomeAltGrid.as_view(), name='home_altern_grid'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsByCategor.as_view(), name='category'),

    # path('article/<int:news_id>/', get_article, name='article_detail_url'),
    path('article/<int:pk>/', ViewNews.as_view(), name='article_detail_url'),

    # path('article/add-news', add_news, name= 'add_news'),
    path('article/add-news', CreateNews.as_view(), name= 'add_news'),

    path('article/extra_del', for_delete, name= 'for_delete'),

]