from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'