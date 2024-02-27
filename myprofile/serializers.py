from rest_framework import serializers
from .models import UserProfile, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "gender",
            "password",
            "password_confirmation",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        age = validated_data.pop("age", None)
        password_confirmation = validated_data.pop("password_confirmation")
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match")
        user = CustomUser.objects.create(**validated_data)
        if age is not None:
            user.age = age
            user.save()
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, age=age)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
