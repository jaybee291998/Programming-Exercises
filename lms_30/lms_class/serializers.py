from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
class SearchResultSerializer(serializers.Serializer):
	email 				= serializers.EmailField()
	first_name 			= serializers.CharField(max_length=255)
	last_name 			= serializers.CharField(max_length=255)
	profile_pic_url 	= serializers.CharField(max_length=2047)
	is_istructor		= serializers.BooleanField()
	course				= serializers.CharField()
	year 				= serializers.CharField()
	invite_link 		= serializers.CharField(max_length=2047)

class SearchInputSerializer(serializers.Serializer):
	search_input		= serializers.CharField(max_length=255)