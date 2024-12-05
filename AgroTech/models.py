from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class contact_model(models.Model):
    name=models.CharField(max_length=1000)
    phone=models.CharField(max_length=12)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=RichTextField()
    def __str__(self):
        return self.name 

class user_register(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    password=models.CharField(max_length=40)
    dob=models.CharField(max_length=10,blank=True,null=True)
    phone=models.CharField(max_length=12,blank=True,null=True)
    pincode=models.CharField(max_length=10,blank=True,null=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    gender=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    profileimg=models.ImageField(upload_to="profile",blank=True,null=True)
    def __str__(self):
      return self.name

class indian_agriculture_university(models.Model):
    name=models.CharField(max_length=200)
    establish=models.CharField(max_length=50)
    desc=RichTextField()
    image=models.ImageField(upload_to="data",blank=True, null=True)
    director=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    def __str__(self):
      return self.name

class video(models.Model):
    title=models.CharField(max_length=100)
    des=RichTextField()
    video=models.FileField()
    def __str__(self):
      return self.title

class crop(models.Model):
    type=models.CharField(max_length=100)
    image=models.ImageField(upload_to="data",blank=True,null=True)
    desc=RichTextField()
    video=models.FileField()
    def __str__(self):
      return self.type

class farmers_call_centre(models.Model):
    title=models.CharField(max_length=200)
    details=RichTextField()
    image=models.ImageField(upload_to="data",blank=True,null=True)
    def __str__(self):
      return self.title

class farmers_scheme(models.Model):
    title=models.CharField(max_length=200)
    desc=RichTextField()
    image=models.ImageField(upload_to="data",blank=True,null=True)
    link=RichTextField()
    def __str__(self):
      return self.title

class latest_technology(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to="data",blank=True, null=True)
    desc=RichTextField()
    def __str__(self):
      return self.name
    
class Blog(models.Model):
    title=models.CharField(max_length=500)
    image=models.ImageField(upload_to="data",blank=True, null=True)
    desc=RichTextField()
    date=models.CharField(max_length=100)
    by=models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class AgricultureData(models.Model):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
         ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December')   
    ]
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    crops = models.TextField()  # Comma-separated list of crops
    crop_images = RichTextField(blank=True, null=True)
    fruits = models.TextField()  # Comma-separated list of fruits
    fruit_images=RichTextField(blank=True, null=True)
    vegetables = models.TextField()  # Comma-separated list of vegetables
    vegetable_images=RichTextField(blank=True, null=True)
    flowers = models.TextField()  # Comma-separated list of flowers
    flower_images=RichTextField(blank=True, null=True)

    def __str__(self):
        return f"{self.state.name} - {self.month}"
    


