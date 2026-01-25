from django.urls import path
from.views import product
from . views import *
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('product/', product.as_view() , name='product'),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('OrderSummary/', OrderSummaryView.as_view()),
    path('creatorder/', CreateOrder.as_view()),
    path('orderitem/' , orderitem.as_view()),
    path('category/<str:category>/', CategoryAPIView.as_view()),
    path('resgister/', RegisterAPI.as_view()),
    path('login/', login_api.as_view()),
    path('decount/',decount.as_view()),
    path('checkout/' , checkout.as_view()),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),)

]

