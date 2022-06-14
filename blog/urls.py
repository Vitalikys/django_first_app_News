from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name = 'register'),
    path('login/', user_login, name = 'login'),
    path('send_mail_test/', send_mail_test, name = 'send_mail_test'),
    path('logout/', user_logout, name = 'logout'),
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
    path('article/scraping', scraping, name= 'scraping'),

]