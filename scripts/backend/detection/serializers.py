from rest_framework import serializers
from .models import DetectionLog


class DetectionInputSerializer(serializers.Serializer):
    """Serializer for intrusion detection input"""
    duration = serializers.FloatField(default=0)
    protocol_type = serializers.CharField(default='tcp')
    service = serializers.CharField(default='http')
    flag = serializers.CharField(default='SF')
    src_bytes = serializers.FloatField(default=0)
    dst_bytes = serializers.FloatField(default=0)
    land = serializers.IntegerField(default=0)
    wrong_fragment = serializers.IntegerField(default=0)
    urgent = serializers.IntegerField(default=0)
    hot = serializers.IntegerField(default=0)
    num_failed_logins = serializers.IntegerField(default=0)
    logged_in = serializers.IntegerField(default=1)
    num_compromised = serializers.IntegerField(default=0)
    root_shell = serializers.IntegerField(default=0)
    su_attempted = serializers.IntegerField(default=0)
    num_root = serializers.IntegerField(default=0)
    num_file_creations = serializers.IntegerField(default=0)
    num_shells = serializers.IntegerField(default=0)
    num_access_files = serializers.IntegerField(default=0)
    num_outbound_cmds = serializers.IntegerField(default=0)
    is_host_login = serializers.IntegerField(default=0)
    is_guest_login = serializers.IntegerField(default=0)
    count = serializers.FloatField(default=1)
    srv_count = serializers.FloatField(default=1)
    serror_rate = serializers.FloatField(default=0)
    srv_serror_rate = serializers.FloatField(default=0)
    rerror_rate = serializers.FloatField(default=0)
    srv_rerror_rate = serializers.FloatField(default=0)
    same_srv_rate = serializers.FloatField(default=1)
    diff_srv_rate = serializers.FloatField(default=0)
    srv_diff_host_rate = serializers.FloatField(default=0)
    dst_host_count = serializers.IntegerField(default=0)
    dst_host_srv_count = serializers.IntegerField(default=0)
    dst_host_same_srv_rate = serializers.FloatField(default=0)
    dst_host_diff_srv_rate = serializers.FloatField(default=0)
    dst_host_same_src_port_rate = serializers.FloatField(default=0)
    dst_host_srv_diff_host_rate = serializers.FloatField(default=0)
    dst_host_serror_rate = serializers.FloatField(default=0)
    dst_host_srv_serror_rate = serializers.FloatField(default=0)
    dst_host_rerror_rate = serializers.FloatField(default=0)
    dst_host_srv_rerror_rate = serializers.FloatField(default=0)
    
    model_type = serializers.ChoiceField(
        choices=['logistic', 'svm'],
        default='logistic'
    )


class DetectionResultSerializer(serializers.Serializer):
    """Serializer for detection result"""
    prediction = serializers.CharField()
    probability = serializers.FloatField()
    class_probabilities = serializers.DictField()
    model_used = serializers.CharField()


class SpamDetectionInputSerializer(serializers.Serializer):
    """Serializer for spam detection input - simple email and content"""
    email = serializers.EmailField(required=True)
    content = serializers.CharField(required=True, max_length=10000)


class ModelResultSerializer(serializers.Serializer):
    """Serializer for individual model result"""
    model = serializers.CharField()
    prediction = serializers.CharField()
    is_spam = serializers.BooleanField()
    confidence = serializers.FloatField()


class SpamDetectionResultSerializer(serializers.Serializer):
    """Serializer for spam detection result with 4 models"""
    final_prediction = serializers.CharField()
    is_spam = serializers.BooleanField()
    confidence = serializers.FloatField()
    spam_votes = serializers.IntegerField()
    ham_votes = serializers.IntegerField()
    spam_score = serializers.IntegerField()
    ham_score = serializers.IntegerField()
    reasons = serializers.ListField(child=serializers.CharField())
    model_results = ModelResultSerializer(many=True)


class DetectionLogSerializer(serializers.ModelSerializer):
    """Serializer for detection log"""
    class Meta:
        model = DetectionLog
        fields = '__all__'
