from apps.gist.views.logger import LogHelper
from apps.accounts.serializers.users_serializer import UserRegisterSerializer
from apps.accounts.models.users import User
from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiResponse



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
        instance = serializer.save()
        LogHelper.fail_log("User created: " + str(instance))

    def create(self, request, _args, _kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": True, "message": "User created successfully"}, status=201)