from rest_framework import serializers

class DeadlineSerializer(serializers.Serializer):
	start_date		= serializers.DateTimeField()
	end_date 		= serializers.DateTimeField()