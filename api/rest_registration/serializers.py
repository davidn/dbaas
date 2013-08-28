from rest_framework import serializers

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, source='user')
