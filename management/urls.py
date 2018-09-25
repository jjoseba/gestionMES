
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^users/$', views.UsersListView.as_view(), name='users_list'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_detail'),

]


