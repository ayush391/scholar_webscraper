from django.urls import include
from django.urls import path
from . import views

urlpatterns = {
    path('', views.home, name='home'),
    path("[% url 'get_query' %]", views.first_page),
    path('next_page/', views.next_page),
    path('next_page/next_page/', views.next_page2),
    # path("[% url 'get_profile' %]", views.get_profile, name='get_profile'),
    path('get_profile/<int:id>/', views.create_profile, name='create_profile'),
    # path('get_profile/<int:id>/sort_by_date/', views.sort_by_date, name='sort_by_date'),
    path('get_profile/<int:id>/sort_by_date/', views.profile_check),

}
# }