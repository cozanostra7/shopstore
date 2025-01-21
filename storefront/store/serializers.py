from rest_framework import serializers
from .models import Product, Collection, ProductImage, Review, Cart, CartItem, Order, OrderItem, Customer
from decimal import Decimal
from django.db import transaction
from .signals import order_created
# Сериализер - это класс, который передовит ОБЪЕКТ из базы данных в JSON

# id title
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True) # Менять нельзя. Только смотреть


# class ProductSerializer(serializers.Serializer):
#     # Указывать какие поля хотите видеть в ответе
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2,
#                                      source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax'
#     )
#
#     # Как вывести категорию
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()  # Диапазон поиска в связи
#     # )
#
#     # Строковое представление
#     # collection = serializers.StringRelatedField()
#     # collection = CollectionSerializer()
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(), view_name='collection-detail'
#     )
#     def calculate_tax(self, product: Product):
#         return round(product.unit_price * Decimal(1.1),   2)

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description',
                  'slug', 'inventory', 'price_with_tax', 'collection', 'images']

    price = serializers.DecimalField(max_digits=6, decimal_places=2,
                                     source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)


    def create(self, validated_data):
        # validated_data - данные отправленные на сохранение
        product = Product(**validated_data) # Как kwargs - словарь отправляем
        product.other = 1
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
    #   {
    #         'id': 1,
    #         'date': '16-05-2023',
    #         'name': 'Евгений',
    #         'description': 'Лучший товар'
    #    }
    # Логика сохранения. Нам надо принимать все данные и вытаскивать
    # id товара из контекста
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        # Отправляем конкретно product_id а остальные данные в в иде словаря



# Так как мы разботаем с REST API то нам надо отправлять JSON

# 1) - Переделать <QuerySet> ->  JSON Где в Meta мы указываем какие поля видим

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

'''
cart/27bda4c0-3577-4188-be11-a9e3cc808dbe/


{
    'id': 27bda4c0-3577-4188-be11-a9e3cc808dbe,
    'items': [
        {
            'id': 1,
            'quantity': 10,
            'total_price': 1000,
            'product':  {
                "id": 1002,
                "title": "7up Diet, 355 Ml123",
                "unit_price": 100,
            } 
        },
        {
            'id': 1,
            'quantity': 10,
            'total_price': 1000,
            'product':  {
                "id": 1002,
                "title": "7up Diet, 355 Ml123",
                "unit_price": 100,
            } 
        }
    ],
    'total_price': 2000
}


'''

# Отдельный сериалайзер для добавления товара в корзину
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # Сделаем метод который будет проверять есть ли товар по поданному id
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists(): # Если нет товара
            raise serializers.ValidationError('Нет товара с данным id')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id'] # В какую корзину
        product_id = self.validated_data['product_id'] # ЧТо положить
        quantity = self.validated_data['quantity']  # ЧТо положить

        try: # Сначала пытаемся положить в существующую корзину
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # Думаем что у нас есть такая корзина с таким товаром
            cart_item.quantity += quantity  # Добавляем товар
            cart_item.save()
            self.instance = cart_item
        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']



# Отдельный сериалайзер для обновления кол-ва товаров
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Не существующий ID корзины')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('Корзина пустая')
        return cart_id


    def save(self, **kwargs):
        with transaction.atomic(): # На случай ошибки, чтобы изменения откатились
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [OrderItem(
                order=order,
                product=item.product,
                unit_price=item.product.unit_price,
                quantity=item.quantity
            ) for item in cart_items]

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order






