
from rest_framework import generics, viewsets,status
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer,CustomerOrderSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [AllowAny()]
        return [IsAdminUser()]
# CustomerOrderList
class CustomerOrderList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        phone = request.query_params.get('customer_phone')
        if not phone:
            return Response({'error': 'মোবাইল নম্বর প্রদান করুন।'}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(customer_phone=phone).order_by('-order_date')
        serializer = CustomerOrderSerializer(orders, many=True)
        return Response(serializer.data)
# for login and logout automatically when browser close
@api_view(['POST'])
def custom_token_view(request):
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.contrib.auth import authenticate

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    print("Authentication failed or not staff")
    return Response({'error': 'Invalid credentials or not admin'}, status=401)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def order_summary(request):
    by_month = (
        Order.objects.annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total=Sum('total_price'), count=Count('id'))
        .order_by('month')
    )
    by_year = (
        Order.objects.annotate(year=TruncYear('order_date'))
        .values('year')
        .annotate(total=Sum('total_price'), count=Count('id'))
        .order_by('year')
    )
    return Response({
        "monthly": by_month,
        "yearly": by_year,
    })