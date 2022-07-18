from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins, permissions, authentication
from django.shortcuts import get_object_or_404

from products.models import Product
from products.serializers import ProductSerializer
from products.permission import IsStaffEditorPermission


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
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

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


class ProductUpdateApiView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##


class ProductDestroyApiView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance
        return super().perform_destroy(instance)


# class ProductListApiView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, req,  *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(req, *args, **kwargs)
        return self.list(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "This is a single view doing cool stuff"
        serializer.save(content=content)


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
