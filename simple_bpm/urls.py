
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.ProcessesListView.as_view(), name='list'),

]


