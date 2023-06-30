from rest_framework import generics
from rest_framework.response import Response
from .serializers import ContactCreateSerializers
from ..models import Contact
from django.conf import settings
from django.core.mail import send_mail

class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subject = serializer.validated_data.get('subject')
        message = serializer.validated_data.get('message')

        send_mail(
            subject,  # subject
            message,  # message
            'settings.EMAIL_HOST_USER',  # from mail
            ['youremail@gmail.com', ],  # to mail
            fail_silently=False,
        )

        return Response(serializer.data, status=201)