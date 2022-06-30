from django.urls import path 
from . import views

app_name = "polls"

urlpatterns = [
    #example: /polls/
    path("", views.IndexView.as_view(), name="index"),
    #example: /polls/1
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    #example: /polls/1/result
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    #example: /polls/1/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]