from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.shortcuts import get_object_or_404

from products.models import Product
from products.serializers import ProductSerializer


@api_view(["POST"])
def api_home(req, *args, **kwargs):
    """
    DRF API VIEW
    """
    serializer = ProductSerializer(data=req.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET', 'POST'])
def product_alt_view(req, pk=None, *args, **kwargs):
    method = req.method

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
