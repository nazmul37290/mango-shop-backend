from django.db import models
from decimal import Decimal
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('আম', 'আম'),
        ('খেজুর', 'খেজুর'),
        ('বাদাম', 'বাদাম'),
        ('কিচমিচ', 'কিচমিচ'),
        ('কালোজিরা', 'কালোজিরা'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount=models.DecimalField(max_digits=8, decimal_places=2,default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,default='আম' )

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True, default=None)
    customer_phone = models.CharField(max_length=20)
    customer_address=models.CharField(max_length=500)
    order_details=models.CharField(max_length=500,null=True, blank=True, default="")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False,default=0)  # 👈 New field
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def save(self, *args, **kwargs):
    # Check if this is a new order (no primary key yet)
        if not self.pk:
            # Only subtract stock on creation
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save()
            else:
                raise ValueError("Not enough stock available.")

        # Calculate total price based on discount or regular price
        unit_price = self.product.discount if self.product.discount > 0 else self.product.price
        self.total_price = unit_price * Decimal(self.quantity)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
