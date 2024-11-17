from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import send_message, message_history

#here write your urls
#list of urls
 
#here write your urls
#list is genetad to create urls
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search/', views.search_profiles, name='search'),
    path('profile/<int:user_id>/', views.view_profile, name='profile'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('skills/', views.skill_list, name='skill_list'),
    path('trade/initiate/', views.initiate_trade, name='initiate_trade'),
    path('trade/list/', views.trade_list, name='trade_list'),
    path('trade/accept/<int:trade_id>/', views.accept_trade, name='accept_trade'),
    path('trade/decline/<int:trade_id>/', views.decline_trade, name='decline_trade'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('home/', views.home, name='home'),
    path('send_message/', send_message, name='send_message'),
    path('message_history/', message_history, name='message_history'),
    path('send_message/<int:user_id>/', views.send_message_detail, name='send_message_detail'),
]
