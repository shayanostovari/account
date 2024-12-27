from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
