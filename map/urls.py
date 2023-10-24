
from django.urls import path
from map import views

app_name = 'map'

urlpatterns = [
    path("", views.DailyReadingView.as_view(), name="home"),
    path("livedata/<live>/", views.DailyReadingView.as_view(), name="livedata"),
    path("historical/", views.HistoricalReadingView.as_view(), name="historical"),
    path("livesignal/", views.LiveSignalView.as_view(), name="livesignal"),
    
    
]

