from django.urls import path
from .views import SensorListCreateView, SensorUpdateView, MeasurementCreateView, SensorDetailView

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorUpdateView.as_view(), name='sensor-update'),
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
    path('sensors/<int:pk>/detail/', SensorDetailView.as_view(), name='sensor-detail'),
]

