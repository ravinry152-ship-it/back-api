from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny 
from .models import Product,Order,OrderItem,Decount,CheckOut
from .serializers import ProductSerializer ,OrderSerializer,OrderItemSerializer,DecountSerializer,CheckOutSerializer
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import authenticate , login 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class product(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self , request , format =None) :
       serializer = ProductSerializer(data = request.data)
       if serializer.is_valid() :
           serializer.save()
           return Response(serializer.data , status=status.HTTP_201_CREATED)
       print(serializer.errors)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetail(APIView)  :
    permission_classes = [IsAuthenticated,]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404 
    def get(self, request, pk,format=None) :
        products = self.get_object(pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    def put(self , request , pk, format=None) :
        products= self.get_object(pk)
        serializer = ProductSerializer(products, data= request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer, status=status.HTTP_200_OK)
        print( serializer.errors)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    def delete(self , request , pk ,format=None) :
        products = self.get_object(pk)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#==========================================Create order======================== 
#=========================================Category=============================
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, category, format=None):
        products = Product.objects.filter(category__iexact=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateOrder(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#=======================================OrderSummary===========================
class orderitem(APIView) :
    permission_classes = [IsAuthenticated,]
    def get(self , request ,formet=None) :
        orderitems = OrderItem.objects.all()
        serlizer= OrderItemSerializer(orderitems, many=True)
        return Response(serlizer.data, status=status.HTTP_200_OK)
    def post(self , request ,format =None) :
        serializer= OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

#=======================================OrderSummary===========================
class OrderSummaryView(APIView):
    permission_classes = [IsAuthenticated,] 
    def get(self, request, format=None):
        # ហៅប្រើ Method ពី OrderManager ដែលយើងបានបង្កើតក្នុង models.py
        today_orders = Order.objects.today()           
        month_orders = Order.objects.this_month()      
        year_orders = Order.objects.this_year()
        week_orders = Order.objects.this_week()

        # បង្កើត JSON Object ដើម្បីបោះទៅឱ្យ Frontend
        data = {
            "today": {
                "count": today_orders.count(),
                "orders": OrderSerializer(today_orders, many=True).data
            },
            "this_month": {
                "count": month_orders.count(),
                "orders": OrderSerializer(month_orders, many=True).data
            },
            "this_year": {
                "count": year_orders.count(),
            },
            "this_week_count": week_orders.count(),
        }

        return Response(data, status=status.HTTP_200_OK)
    
#=============================================User regester=============================    
class RegisterAPI(APIView):
    permission_classes = [AllowAny,] 
    authentication_classes = []
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            # 1. Validation check(អត់Email and password and username is error)
            if not email or not password or not username:
                return Response(
                    {'error': "Username, email, and password are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username).exists():
                return Response({'error': "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Account created successfully",
                "email": user.email,
                "user_id": user.id,
                "access": str(refresh.access_token), 
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#======================================Login-API=======================================
class login_api(APIView) :
    permission_classes = [AllowAny,]
    def post(self , request , format=None) :
         email = request.data.get('email')
         password = request.data.get('password')
         if not email or not password :
             return Response({
                 "error": "សូមបញ្ចូល Email និងលេខសម្ងាត់"
             } , status=status.HTTP_400_BAD_REQUEST)
         try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
         except User.DoesNotExist:
            return Response({
                "error": "មិនមានគណនីប្រើប្រាស់អ៊ីមែលនេះទេ"
            }, status=status.HTTP_401_UNAUTHORIZED)
         user = authenticate(request, username=username, password=password)
    #========================================================================
         if user is not None:
          login(request, user) 
          refresh = RefreshToken.for_user(user)
          access_token = str(refresh.access_token)
          role = "admin" if user.is_staff else "user"
          return Response({
            "message": "Login successful",
            "access": access_token,   
            "refresh": str(refresh),
            "email": user.email,
            "user_id": user.id,
            "is_staff": user.is_staff,
            "role": role
        }, status=status.HTTP_200_OK)
         else:
           return Response({
            "error": "Invalid credentials.",
        }, status=status.HTTP_401_UNAUTHORIZED)
#========================================Update Decount============================
class decount(APIView) :
    permission_classes = [IsAuthenticated,] 
    def get(self ,request , format=None) :
        productdecount = Decount.objects.all()
        serializer = DecountSerializer(productdecount ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self , request ,format=None) :
        serializer= DecountSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
#===============================chackout=============================================
class checkout(APIView) :
    permission_classes= [IsAuthenticated,]
    def post(self ,request , format=None)  :
        serializer = CheckOutSerializer(data = request.data) 
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
