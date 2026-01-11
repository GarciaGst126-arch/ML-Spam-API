from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SpamDetectionInputSerializer, DetectionLogSerializer
from .models import DetectionLog
from .ml_models import get_models


class DetectSpamView(APIView):
    """API endpoint for spam detection using 4 ML models"""
    
    def post(self, request):
        serializer = SpamDetectionInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        email = data['email']
        content = data['content']
        
        try:
            models = get_models()
            result = models.predict_all_models(email, content)
            result['email'] = email
            
            # Log the prediction
            DetectionLog.objects.create(
                email=email,
                content=content[:500],
                prediction=result['final_prediction'],
                probability=result['confidence'] / 100,
                model_used='ensemble_4_models'
            )
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """Return API info"""
        return Response({
            'models_available': [
                'Regresión Lineal',
                'Regresión Logística', 
                'Pipeline Personalizado',
                'SVM (Support Vector Machine)'
            ],
            'description': 'Email spam detection using 4 ML models with voting',
            'required_fields': ['email', 'content']
        })


class DetectionLogsView(APIView):
    """API endpoint for detection logs"""
    
    def get(self, request):
        logs = DetectionLog.objects.all()[:100]
        serializer = DetectionLogSerializer(logs, many=True)
        return Response(serializer.data)


class TrainModelsView(APIView):
    """API endpoint to retrain models"""
    
    def post(self, request):
        try:
            models = get_models()
            results = models.train_models()
            return Response({
                'message': 'All 4 models trained successfully',
                'results': results
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckView(APIView):
    """Health check endpoint"""
    
    def get(self, request):
        return Response({'status': 'healthy', 'service': 'spam-detection-4-models'})
