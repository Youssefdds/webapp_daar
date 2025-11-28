from django.urls import path
from .views import search_books, search_regex, book_content, get_suggestions, enhanced_search

urlpatterns = [
    path("search/", search_books),
    path("search/regex/", search_regex),
    path("book_content/",book_content),
    path('suggestions/', get_suggestions), 
    path("enhanced-search/", enhanced_search),

]
