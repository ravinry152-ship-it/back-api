from rest_framework import serializers
from django.utils import timezone
from .models import OrderItem, Order,Product,Decount,CheckOut
 
class ProductSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    time_summary = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'order_qty', 'order_price', 'time_summary']

    def get_time_summary(self, obj):
        # យកម៉ោងបច្ចុប្បន្ននៅខ្មែរ
        now = timezone.localtime(timezone.now())
        order_time = timezone.localtime(obj.order.order_datetime)
        
        # Logic ឆែកមើលលក្ខខណ្ឌ
        status = {
            "is_today": order_time.date() == now.date(),
            "is_this_month": order_time.month == now.month and order_time.year == now.year,
            "is_this_year": order_time.year == now.year,
            "week_number": order_time.isocalendar()[1]
        }
        return status
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_datetime', 'items']
        read_only_fields = ['id', 'user', 'order_datetime'] 

    def create(self, validated_data):
        items_data = validated_data.pop('items') 
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class DecountSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Decount
        fields = '__all__'

class CheckOutSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CheckOut
        fields = '__all__'       