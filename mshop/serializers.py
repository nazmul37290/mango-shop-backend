from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'product_id',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'order_details',
            'quantity',
            'total_price',
            'order_date',
            'status',
        ]
class CustomerOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'product_name', 
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'order_details',
            'quantity',
            'total_price',
            'order_date',
            'status',
        ]
