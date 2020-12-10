from django.urls import path
from . import views

app_name = 'main_system'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('dashboard/', views.offer_list, name='offer_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:provider>/', views.offer_detail, name='offer_detail'),
    path('remove_offer/<int:offer_id>/', views.remove_offer, name='remove_offer'),
    path('take_offer/<int:offer_id>', views.take_offer, name='take_offer'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('estimate_costs/', views.estimate_costs, name='estimate_costs'),
]