from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name="index"),
    path('product',views.productPage,name="product"),
    path('email',views.submit_email,name="submit_email")
]