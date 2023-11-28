from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Project

class ProjectSerializers(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'