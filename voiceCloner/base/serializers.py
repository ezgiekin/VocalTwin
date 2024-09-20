from rest_framework import serializers
from .models import VoiceRecording, AudioFile, CustomUser

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['recording', 'file']

class VoiceRecordingSerializer(serializers.ModelSerializer):
    files = AudioFileSerializer(many=True, read_only=True)

    class Meta:
        model = VoiceRecording
        fields = ['id', 'user', 'name', 'gender','cloned', 'uploaded_at', 'files']
        extra_kwargs = {
            'cloned': {'required': False}
        }

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']