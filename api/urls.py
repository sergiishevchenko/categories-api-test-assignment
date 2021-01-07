from django.urls import path
from .views import CategoriesView, CategoriesGetView

urlpatterns = [
    path('categories/<id>', CategoriesGetView.as_view()),
    path('categories', CategoriesView.as_view()),
]
