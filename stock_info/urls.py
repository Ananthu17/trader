from django.urls import path
from .views import Home_view


urlpatterns = [
    path('', Home_view.as_view(),
         name='home')
]
