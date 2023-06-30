from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import UserBase
from django.conf import settings
from django.core.mail import send_mail
from services.generator import CodeGenerator


Users = get_user_model()

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})

    class Meta:
        model = Users
        fields = ("email", "password")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user or not Users.objects.filter(email=email):
            raise serializers.ValidationError({"error", "Email or password wrong "})

        return attrs

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        user = Users.objects.get(email=instance.get("email"))
        token = RefreshToken.for_user(user)
        repr_["token"] = {"refresh": str(token), "access": str(token.access_token)}

        return repr_


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = Users
        fields = ("email", "username", "first_name", "last_name", "password", "password_confirm")
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email already exists"})
        if Users.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "This username already exists"})
        if password != password_confirm:
            raise serializers.ValidationError({"error": "Password don't match"})

        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        user = Users.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
            activation_code=CodeGenerator.create_activation_link_code(size=6, model_=Users)
        )
        user.set_password(password)
        user.save()

        # sending mail

        message = f"Please write activation code below: \n {user.activation_code}"

        send_mail(
            'Activate your account',  # subject
            message,  # message
            'settings.EMAIL_HOST_USER',  # from mail
            [user.email],  # to mail
            fail_silently=False,
        )

        return user
    
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["slug"] = instance.slug

        return repr_


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField()


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    old_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = Users
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"error": "Old password is not correct"})

        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'about', 'profile_photo', 'email')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'about': {'required': False},
            'profile_photo': {'required': False},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if Users.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"error": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if Users.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"error": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('first_name', instance.last_name)
        instance.about = validated_data.get('about', instance.about)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = ('email', )

    def validate(self, attrs):
        email = attrs.get("email")

        if not Users.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "There is no user with this e-mail address"})

        return attrs


class ResetPasswordCompleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = Users
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match"})

        return attrs

