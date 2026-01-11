from django.urls import path
from .views import DetectSpamView, DetectionLogsView, TrainModelsView, HealthCheckView

urlpatterns = [
    path('detect/', DetectSpamView.as_view(), name='detect'),
    path('logs/', DetectionLogsView.as_view(), name='logs'),
    path('train/', TrainModelsView.as_view(), name='train'),
    path('health/', HealthCheckView.as_view(), name='health'),
]
