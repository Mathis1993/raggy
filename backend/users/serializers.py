from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def validate(self, data):
        # ToDo(ME-08.02.24): Add password strength validation
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            is_superuser=False,
            is_staff=False,
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
