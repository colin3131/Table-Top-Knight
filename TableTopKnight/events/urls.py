from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ourteam/', views.ourteam, name='ourteam'),
    path('contactus/', views.contactus, name='contactus'),
    path('login/', views.login, name='login'),
    path('library/', views.library, name='library'),
    path('games/<int:gameID>/', views.game, name='game'),
    path('myevents/', views.myevents, name='myevents'),
    path('myevents/<int:eventID/', views.myevent, name='myevent'),
    path('friends/', views.friends, name='friends'),
    path('friends/<int:userID>/', views.friend, name='friend'),
]