from django.urls import path
from . import views

app_name = 'main_system'

urlpatterns = [
    path('', views.offer_list, name='offer_list'),
    path('<int:id>/<str:name>/', views.offer_detail, name='offer_detail'),
    path('<int:id>/<str:name>/<int:room_id>/', views.take_room_offer, name='take_room_offer'),
    path('remove_room_offer/<int:room_id>/', views.remove_room_offer, name='remove_room_offer'),
    path('remove_offer/<int:id>/<str:name>/', views.remove_offer, name='remove_offer'),
    path('<int:id>/<str:name>/take_offer/', views.take_offer, name='take_offer'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('estimate_costs/', views.estimate_costs, name='estimate_costs'),
]