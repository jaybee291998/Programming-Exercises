from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class LogInSerializer(serializers.Serializer):
	email 		= serializers.EmailField()
	password	= serializers.CharField()

	# def validate_password(self, value):
		
