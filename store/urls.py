from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products') # basename is prefix as we will have both product-reviews-list and product-reviews-detail
router.register('collections',views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')   # basename is prefix as we will have both product-reviews-list and product-reviews-detail

# URLConf
urlpatterns = [
    path('',include(router.urls)),
    path('',include(products_router.urls)),
               ]

