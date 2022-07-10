from audioop import avg
from os import O_NONBLOCK
from .models import Product 
from django.db.models import Q, Avg, Max
from django.db.models.functions import Length

class ProductCrud(Product):
    @classmethod
    def get_all_products(cls):
        return Product.objects.all()

    @classmethod
    def find_by_model(cls,model):
        return Product.objects.get(model=model)
    
    @classmethod
    def last_record(cls):
        return Product.objects.last()

    @classmethod
    def by_rating(cls,rating):
        return Product.objects.filter(rating=rating)

    @classmethod
    def by_rating_range (cls, rating_start,rating_end):
        return Product.objects.filter(rating__range=(rating_start,rating_end))
    
    @classmethod
    def by_rating_and_color(cls, rating, color):
        return Product.objects.filter(rating=rating,color=color)
    
    @classmethod
    def by_rating_or_color(cls,rating,color):
        return Product.objects.filter(Q(rating=rating) | Q(color=color))

    @classmethod
    def no_color_count(cls):
        return Product.objects.filter(color__isnull=True).count()
    
    @classmethod
    def below_price_or_above_rating(cls,price,rating):
        return Product.objects.filter(Q(price_cents__lt=price) | Q(rating__gt=rating))

    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        return Product.objects.all().order_by('category','-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls,manufacturer):
        return Product.objects.filter(manufacturer__icontains=manufacturer)

    @classmethod
    def manufacturer_names_for_query(cls,query):
        return Product.objects.filter(manufacturer__icontains=query).values_list('manufacturer',flat=True)
    
    @classmethod
    def not_in_a_category(cls, category):
        return Product.objects.exclude(category__contains=category)
    
    @classmethod
    def limited_not_in_a_category(cls, category, limit):
        return Product.objects.exclude(category__contains=category)[:limit]
    
    @classmethod
    def category_manufacturers(cls, category):
        return Product.objects.filter(category=category).values_list('manufacturer',flat=True)

    @classmethod
    def average_category_rating(cls,category):
        return Product.objects.filter(category=category).aggregate(Avg('rating'))

    @classmethod
    def greatest_price(cls):
        return Product.objects.all().aggregate(Max('price_cents'))
    
    @classmethod
    def longest_model_name(cls):
        return Product.objects.order_by(Length('model').desc()).values_list('id', flat=True)[0]
    
    @classmethod
    def ordered_by_model_length(cls):
        return Product.objects.order_by(Length('model'))
