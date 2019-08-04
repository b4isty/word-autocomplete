from django.urls import path
from .views import search_word, search

app_name = "search"

urlpatterns = [
    path("", search, name="search"),
    path("search/", search_word, name="search_word")
]