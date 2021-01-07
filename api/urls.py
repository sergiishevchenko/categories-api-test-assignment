from django.urls import path
from .views import CategoriesAPI, CategoriesAPIView

urlpatterns = [
    path('categories/<id>', CategoriesAPIView.as_view()),
    path('categories', CategoriesAPI.as_view()),
]
