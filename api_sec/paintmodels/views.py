
from rest_framework import viewsets
from .models import Company, Order, Paint, UserProfile
from .serializers import CompanySerializer, OrderSerializer, PaintSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class PaintViewSet(viewsets.ModelViewSet):
    queryset = Paint.objects.all()
    serializer_class = PaintSerializer
    permission_classes = (IsAuthenticated,)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request):
        print(request.data)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                            'user': serializer.data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_quantity = int(request.data.get('quantity'))
        if new_quantity is None:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
        if order.paint.quantity < new_quantity:
            return Response({"error": "Not enough paint in stock"}, status=status.HTTP_400_BAD_REQUEST)
        order.paint.quantity = order.paint.quantity - new_quantity
        order.paint.save()
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        color = request.data.get('color')
        quantity = int(request.data.get('quantity'))
        paint = Paint.objects.get(name=color)
        if paint.quantity < quantity:
            return Response({"error": "Not enough paint in stock"}, status=status.HTTP_400_BAD_REQUEST)
        paint.quantity = paint.quantity - quantity
        paint.save()
        order = Order(user=request.user, paint=paint, quantity=quantity, company=request.user.userprofile.company)
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenVerifyView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response({"detail": "Token is valid", "status": status.HTTP_200_OK})

