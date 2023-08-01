from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection

### Serialisers are external fields that are shown within the response of an api call as you may want them to be different to the full model.

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title'] 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','description','slug','inventory','price_with_tax','unit_price','collection'] 

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

