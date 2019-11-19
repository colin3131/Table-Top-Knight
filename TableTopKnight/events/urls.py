from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),    path('dashboard/', views.dashboard, name='dashboard'),
    path('ourteam/', views.ourteam, name='ourteam'),
    path('contactus/', views.contactus, name='contactus'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('library/', views.library, name='library'),
    path('games/', views.allgames, name='allgames'),
    path('games/<int:gameID>/', views.game, name='game'),
    path('games/<int:gameID>/add/', views.addgame, name='addgame'),
    path('games/<int:gameID>/remove/', views.removegame, name='removegame'),
    path('events/', views.myevents, name='myevents'),
    path('events/createevent/', views.newevent, name='newevent'),
    path('events/<int:eventID>/', views.myevent, name='myevent'),
    path('events/<int:eventID>/vote/', views.vote, name='vote'),
    path('friends/', views.friends, name='friends'),
    path('friends/<int:userID>/', views.friend, name='friend'),
    path('friends/<int:userID>/add', views.addfriend, name='addfriend'),
]

handler404 = views.handler404