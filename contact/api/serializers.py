from rest_framework import serializers
from ..models import Contact

class ContactCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

    def validate(self, attrs):
        name = attrs.get("name")

        if name:
            if not name.replace(" ", "").replace(",", "").replace(".", "").isalpha():
                raise serializers.ValidationError({"error": "Name misspelled"})

        return attrs