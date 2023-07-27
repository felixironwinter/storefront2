from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection

### Serialisers are external fields that are shown within the response of an api call as you may want them to be different to the full model.

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title'] 

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)