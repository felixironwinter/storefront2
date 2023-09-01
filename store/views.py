from typing import Any
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product,Collection,OrderItem,Review
from store.serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id') # define the query parameter you want to implement
        if collection_id is not None: # if someone has specified a parameter, then execute some task
            queryset = queryset.filter(collection_id=collection_id)

        return queryset
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destory(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() >0:
            return Response({'error':'Product Cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destory(self, request, *args, **kwargs):
        if Collection.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'product Cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}

    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(
    #     Collection.objects.annotate(
    #     products_count=Count('products')), pk=pk)
    #     if collection.products.count()>0:
    #         return Response({'error':'product Cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

