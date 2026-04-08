from django.urls import path
from .views import *

urlpatterns = [
    path('menus', get_menus),
    path('menus/', get_menus),
    path('menus/create', create_menu),
    path('menus/<str:id>', get_menu_by_id),
    path('menus/<str:id>/update', update_menu),
    path('menus/<str:id>/delete', delete_menu),
]