from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('create_item', views.create_item),
    path('newitem', views.newitem),
    path('logout', views.logout),
    path('wishlistitems/<item_id>', views.wishlistitems),
    path('addtowishlist/<item_id>', views.addtowishlist),
    path('removefromwishlist/<item_id>', views.removefromwishlist),
    path('deleteitem/<item_id>', views.deleteitem),
]
