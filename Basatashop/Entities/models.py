
from django.db import models
from registration.models import User

class Product_group (models.Model):
    name = models.CharField(max_length=30)
    namet = models.CharField(max_length=30, blank=True, null=True)
    picture = models.ImageField(upload_to='Entities/static/groups', blank=True, null=True)
    picture_l = models.ImageField(upload_to='Entities/static/groups', blank=True, null=True)
    picture_b = models.ImageField(upload_to='Entities/static/groups', blank=True, null=True)

    def __unicode__(self):
        return self.name
    
class Product_type (models.Model):
    group = models.ForeignKey(Product_group)
    name = models.CharField(max_length=30)
    namet = models.CharField(max_length=30, blank=True, null=True)
    picture = models.ImageField(upload_to='Entities/static/types', blank=True, null=True)
    picture_l = models.ImageField(upload_to='Entities/static/types', blank=True, null=True)
    picture_b = models.ImageField(upload_to='Entities/static/types', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Instruction (models.Model):
    text = models.TextField()
    name = models.CharField(max_length=60)
    picture = models.ImageField(upload_to='Entities/static/instructions', blank=True, null=True)
    picture_l = models.ImageField(upload_to='Entities/static/instructions', blank=True, null=True)
    picture_b = models.ImageField(upload_to='Entities/static/instructions', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
           
class Product (models.Model):
    prod_type = models.ForeignKey(Product_type)
    name = models.CharField(max_length=60)
    producer = models.CharField(max_length=30, blank=True, null=True)
    sdescription = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='Entities/static/products', blank=True, null=True)
    picture_l = models.ImageField(upload_to='Entities/static/products', blank=True, null=True)
    picture_b = models.ImageField(upload_to='Entities/static/products', blank=True, null=True)
    model = models.ImageField(upload_to='Entities/static/products', blank=True, null=True)
    quantity = models.IntegerField()
    #instrucrion = models.ForeignKey(Instruction, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Characteristic (models.Model):
    product = models.ForeignKey(Product)
    description = models.TextField()
    #charac_type = models.CharField(max_length=30, blank=True, null=True)
    #name = models.CharField(max_length=30, blank=True, null=True)
    #size = models.IntegerField()
    #prise = models.FloatField()
    
    def __unicode__(self):
        return self.description
    
class Price (models.Model):
    product = models.ForeignKey(Product)  
    value = models.FloatField()
    date_init = models.DateTimeField()  
    
    def __unicode__(self):
        return self.value  
    
class Delivery (models.Model):
    supplier = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField()
    total = models.FloatField()
    
class Del_item (models.Model):
    delivery = models.ForeignKey(Delivery)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.FloatField()    

class Basket (models.Model):
    BASKET_CHOICES = (
                      (u'N', u'New'),
                      (u'R', u'Ready'),
                      (u'F', u'Finished'),
                      )
    user = models.ForeignKey(User) 
    adding_time = models.DateTimeField()
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    comment = models.TextField(blank=True, null=True)
    #summ = models.FloatField()
    total = models.FloatField() 
    btype = models.CharField(max_length=2, choices=BASKET_CHOICES) 
    
class Order (models.Model):
    basket = models.ForeignKey(Basket)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.FloatField()
    #characteristic = models.ForeignKey(Characteristic)
    #numb = models.IntegerField()
    
#class Company (models.Model):
#    user = models.ForeignKey(User)
#    name = models.CharField(max_length=50)
#    tel = models.CharField(max_length=20)
#    city = models.CharField(max_length=50)
#    address = models.CharField(max_length=100)
#    post = models.CharField(max_length=50)
#    description = models.TextField()
    
#class DocumentFile (models.Model):
#    doc_file = models.FileField(upload_to = 'Entities/static/files')
#    doc_type = models.CharField(max_length = 10)
#    description = models.TextField()
    
    
class News (models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    picture = models.ImageField(upload_to='Entities/static/news', blank=True, null=True)
    picture_l = models.ImageField(upload_to='Entities/static/news', blank=True, null=True)
    picture_b = models.ImageField(upload_to='Entities/static/news', blank=True, null=True)

class Question (models.Model):
    fio = models.CharField(max_length=50)
    mail = models.EmailField()
    text = models.TextField()
    adding_time = models.DateTimeField()
    answer = models.TextField(blank=True, null=True)  
        
class SUser (models.Model):
    login = models.CharField(max_length = 30)
    password = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    birthday = models.DateField()
    country = models.CharField(max_length = 20)
    city = models.CharField(max_length = 20)
    street = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 40)    
    getSpam = models.BooleanField()
    is_staff = models.BooleanField()