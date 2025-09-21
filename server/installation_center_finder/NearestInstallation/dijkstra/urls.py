from django.urls import path
from .views import NearestCentersView

urlpatterns = [
    path('nearest-centers/', NearestCentersView.as_view(), name='nearest-centers'),
]
