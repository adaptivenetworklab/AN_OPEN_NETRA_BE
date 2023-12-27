from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/tokens/access-token',
        '/api/v1/tokens/refresh-token',
        '/api/v1/tokens/my-api'
    ]
    return Response(routes)


class MyApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {"message": "Authenticated"}
        return Response(data)
