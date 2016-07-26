from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from financial.models import Tax
from django.contrib.auth.models import User



class Manufacturer(models.Model):
    """
    Represents a Manufacturer
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="manufacturer_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="manufacturer_modified_by", null=True,blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name




class Category(models.Model):
    """
    Represents a Category for Products
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/categorievs', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='sub_categories', null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_expended = models.BooleanField(default=False, help_text='Catergory will always shown expended')
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="category_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="category_modified_by", null=True,blank=True)

    class Meta:
        ordering = ('display_order', 'id',)
        verbose_name_plural = 'Categories'



class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
    sales_account_code = models.CharField(max_length=100)
    supplier_code = models.CharField(max_length=100)
    purchase_account_code = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="product_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="product_modified_by", null=True,blank=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product)
    supply_price = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Per unit price')
    retail_price = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Per unit price')
    markup = models.FloatField(default=0.0)
    tax = models.ForeignKey(Tax)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="price_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="price_modified_by", null=True,blank=True)


class Variant(models.Model):
    product = models.ManyToManyField(Product)
    has_varient = models.BooleanField(default=True)
    default_value = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="product_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="product_modified_by", null=True,blank=True)


class Attribute(models.Model):
    variant = models.ForeignKey(Variant)
    option_name =  models.CharField(max_length=100)
    default_value = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="attribute_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="attribute_modified_by", null=True,blank=True)

STOCK_TYPE_CHOICES = (
    ('1','Standard'),
    ('2','Composite'),
    
)

class Inventory(models.Model):
    product = models.ForeignKey(Product)
    sku = models.CharField(max_length=100, unique=True)
    stock_type = models.CharField(max_length=100, choices=STOCK_TYPE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="inventory_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="inventory_modified_by", null=True,blank=True)


class StockControll(models.Model):
    inventory = models.ForeignKey(Inventory)
    current_stock = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)
    reorder_amount = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="inventory_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="inventory_modified_by", null=True,blank=True)

    
class ProductSpec(models.Model):
    """
    Represents product specification attribute
    """
    product = models.ForeignKey(Product, related_name='specs')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, related_name="product_spec_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="product_spec_modified_by", null=True,blank=True)

    class Meta:
        db_table = 'catalog_product_spec'
        ordering = ('display_order', 'id',)
        unique_together = ('product', 'name',)
        verbose_name_plural = 'Product Specs'

    def __unicode__(self):
        return '%s: %s' % (self.name, self.value)


class ProductPic(models.Model):
    """
    Represents product picture
    """
    product = models.ForeignKey(Product, related_name='pics')
    pic = models.ImageField(upload_to="images/catalog/products")
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.Foreign<Key(User, related_name="product_pic_created_by", null=True,blank=True)
    modified_by = models.ForeignKey(User, related_name="product_pic_modified_by", null=True,blank=True)
    class Meta:
        db_table = 'product_pic'
        verbose_name_plural = 'Product Pics'

    def __unicode__(self):
        return '%s [Pic #id %s]' % (self.product, self.id)