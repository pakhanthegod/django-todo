from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'todo'
urlpatterns = [
    path('', login_required(views.ItemView.as_view()), name='index'),
    path('update/<int:pk>/', login_required(views.ItemUpdateView.as_view()), name='update'),
    path('delete/<int:pk>/', login_required(views.ItemDeleteView.as_view()), name='delete'),
]