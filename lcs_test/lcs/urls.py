from django.conf.urls import url
from lcs import views

urlpatterns = [
  url('', views.find_lcs, name="find_lcs"),
]
