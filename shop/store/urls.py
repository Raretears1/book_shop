from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name="intro"),
    path('store/', views.store, name="store"),

    path('store/<int:pk>/', views.PostDetailView.as_view(), name='product'),

    path('basket/', views.basket, name="basket"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),

    path('view_info/', views.view_info, name="view_info")

]
