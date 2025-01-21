from django.shortcuts import get_object_or_404
from .models import Product, Collection, Order, OrderItem, Cart, CartItem, Review
from django.http import HttpResponse
from .permissions import IsAdminOrReadOnly
# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

from django.db.models import Count

# def product_list(request):
#     return HttpResponse('Govno')

# @api_view() # Иметь интерфейс рест фрамеворк
# def product_list(request):
#     return Response('Govno')

# collection_list

# @api_view()
# def collection_list(request):
#     queryset = Collection.objects.all()
#     serializer = CollectionSerializer(queryset, many=True,
#                                       context={'request': request})
#     return Response(serializer.data)
#
#
# @api_view() # Иметь интерфейс рест фрамеворк
# def product_list(request):
#     # Выводим диапазон вывода
#     queryset = Product.objects.all()
#     serializer = ProductSerializer(queryset, many=True,
#                                       context={'request': request})
#     return Response(serializer.data)
#
# @api_view()
# def collection_detail(request, pk):
#     return Response(f'{pk} - Ok')


# @api_view()
# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk) # Может быть ошибка если отправят не тот pk
#         serializer = ProductSerializer(product)  # many не надо такак объект 1
#         return Response(serializer.data)
#     except:
#         # return Response(status=404)
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view()
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk) # Получение объекта или 404 ошибка
#     serializer = ProductSerializer(product, context={'request': request})
#     return Response(serializer.data)

# category = models.ForeignKey(Category, on_delete=models.CASCADE,
#                              related_name='gavriki')
#
#
# category = Category.objects.get(pk=pk)
# articles = Article.objects.filter(category=category)
#
# articles = category.article_set.all()  # Все дети
# articles = category.gavriki.all()

# @api_view(['GET', 'POST']) # Какие типы запросов мы поддерживаем
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     else: # POST
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data,
#                                           context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({
#                 'error': 'Категория не может быть удалена, так как в ней есть товары'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# # Реализуйте product_list  product_detail
#
# # annotate - не надо использовать
# # Проверка при удалении:
# # if product.orderitem_set.count() > 0
#
#
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True,
#                                        context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])  # Изменение
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product,
#                                        context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Товар не может быть удален. '
#                                       'Так как он есть в заказе'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin

# class ProductList(APIView, ListModelMixin):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         # select_related('collection') - Оптимизирует запросы в базу данных
#         # Добавит JOIN в запросы что ускорит загрузку данных
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product,
#                                        context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Товар не может быть удален. Так как он есть в заказе'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CollectionList(APIView, ListModelMixin):
#     def get(self, request):
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#         if collection.product_set.count() > 0:
#             return Response({'error': 'Категория не может быть удалена. '
#                                       'Так как в ней есть товары'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# class ProductList(ListCreateAPIView):
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
#     #
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()  # Нужно указывать диапазон поиска объекта
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Товар не может быть удален. Так как он есть в заказе'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#     def get_serializer_context(self):
#         return {'request', self.request}
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CollectionSerializer
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#
#     def delete(self, request, pk):
#         collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#         if collection.product_set.count() > 0:
#             return Response({'error': 'Категория не может быть удалена. '
#                                       'Так как в ней есть товары'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
# Добавление фильтров в запросы
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Товар не может быть удален. Он есть в заказах'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(products_count=Count('products')).all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Категория не может быть удалена. '
                                      'В ней есть товары'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # Надо указать какие именно отзывы выводить - только для определенного товара
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, UpdateCartItemSerializer
# Не будем реализовавывать показ ВСЕХ корзин - списка

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete'] # Какие методы поддерживаем

    # Какой сериалайзер использовать в зависимости от метода
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer # GET - в любом другом случае

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


from .serializers import CustomerSerializer
from .models import Customer
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            customer = Customer.objects.get(user_id=request.user.id)
        except:
            customer, created = Customer.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


from .serializers import OrderSerializer, OrderItemSerializer, \
    CreateOrderSerializer, UpdateOrderSerializer

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,
                                           context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = self.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        # only - возмет одно поле а не весь объект
        return Order.objects.filter(customer_id=customer_id)







