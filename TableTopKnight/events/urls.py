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
    path('events/<int:eventID>/remove/', views.removeevent, name='removeevent'),
    path('events/<int:eventID>/join/', views.joinevent, name='joinevent'),
    path('events/<int:eventID>/leave/', views.leaveevent, name='leaveevent'),
    path('events/<int:eventID>/request/', views.eventrequest, name='eventrequest'),
    path('events/<int:eventID>/reject/', views.rejectevent, name='rejectevent'),
    path('events/<int:eventID>/addpending/', views.addpendingplayer, name='addpendingplayer'),
    path('friends/', views.friends, name='friends'),
    path('friends/<int:userID>/', views.friend, name='friend'),
    path('friends/add/', views.addfriend, name='addfriend'),
    path('friends/<int:userID>/accept', views.acceptfriend, name='acceptfriend'),
    path('friends/<int:userID>/reject', views.rejectfriend, name='rejectfriend'),
    path('friends/<int:userID>/request', views.friendrequest, name='friendrequest'),
    path('friends/<int:userID>/remove', views.removefriend, name='removefriend'),
]

handler404 = views.handler404
