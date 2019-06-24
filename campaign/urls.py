from django.urls import path, re_path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'campaign'

urlpatterns = [
    path('buktitayang/<str:campaign_name>/', views.upload_bukti_tayang),
    path('detail/<str:campaign_name>/', views.photo_by_campaign),
    path('download/<str:campaign_name>/', views.download_image),
    path('bukti/<str:campaign_name>/<str:license_no>/', views.photo_by_driver),
    re_path(r'^$', views.index, name='campaign_all'),
]