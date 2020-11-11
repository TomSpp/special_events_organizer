from django.urls import path
from . import views

app_name = 'main_system'

urlpatterns = [
    path('', views.offer_list, name='offer_list'),
    path('<int:id>/<str:name>/', views.offer_detail, name='offer_detail'),
]