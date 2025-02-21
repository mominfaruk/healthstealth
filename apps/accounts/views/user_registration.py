from apps.gist.views.logger import LogHelper
from apps.accounts.serializers.users_serializer import UserRegisterSerializer
from apps.accounts.models.users import User
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response



@extend_schema(
    description="This endpoint allows you to register a new user.",
    responses={
        201: UserRegisterSerializer,
        400: OpenApiResponse(description="Bad request"),
    }
)
class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
        except Exception as e:
            LogHelper.fail_log(e)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": True, "message": "User created successfully"}, status=201)