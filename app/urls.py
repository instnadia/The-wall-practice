from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'), #GET
    path('register', views.reg), #POST
    path('success', views.success), #GET
    path('login', views.log), # POST
    path('logout', views.logout), #GET - don't see the url
    path('messages/new', views.message), #POST
    path('comments/new/<int:id>', views.comment), #POST
    path('message/like/<int:id>', views.like), #POST
]