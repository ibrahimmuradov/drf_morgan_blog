from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .serializers import LoginSerializer, RegisterSerializer, ActivationSerializer, ChangePasswordSerializer, UpdateProfileSerializer, ResetPasswordSerializer, ResetPasswordCompleteSerializer

Users = get_user_model()

class LoginView(generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=201)


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer


class ActivationView(generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "slug"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {}

        if obj.activation_code == request.data.get("code"):
            user = Users.objects.get(email=obj.email)

            obj.is_active = True
            obj.activation_code = None
            obj.save()

            data["email"] = obj.email
            token = RefreshToken.for_user(user)
            data["token"] = {"refresh": str(token), "access": str(token.access_token)}

            return Response(data, status=201)
        else:
            return Response({"error": "Wrong code"})


class BlacklistTokenUpdateView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=205)
        except Exception as e:
            return Response(status=404)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    lookup_field = "pk"

    def put(self, request, *args, **kwargs):
        try:
            user = self.get_object()

            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            user.set_password(serializer.validated_data.get('password'))
            user.save()

            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            token_data = {"email": user.email}

            token = RefreshToken.for_user(user)
            token_data["token"] = {"refresh": str(token), "access": str(token.access_token)}

            return Response({**token_data})
        except Exception as e:
            return Response(status=404)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer


class ResetPasswordView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data.get("email")
        user = Users.objects.get(email=user_email)

        link = request.build_absolute_uri(reverse_lazy("account-api:reset_password_complete", kwargs={"slug": user.slug}))

        subject = 'Morgan Blog - Account verification link'
        message = f'You can verify your account by clicking the link below: \n {link}'

        send_mail(
            subject,  # subject
            message,  # message
            'settings.EMAIL_HOST_USER',  # from mail
            [user.email],  # to mail
            fail_silently=False,
        )

        return Response(serializer.data, status=201)


class ResetPasswordCompleteView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = ResetPasswordCompleteSerializer
    lookup_field = "slug"

    def put(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data.get('password'))
        user.save()

        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        token_data = {"email": user.email}

        token = RefreshToken.for_user(user)
        token_data["token"] = {"refresh": str(token), "access": str(token.access_token)}

        return Response({**token_data})
