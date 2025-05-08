from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class GetUrlModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Product_URL = models.TextField()

    def __str__(self):
        return self.Product_URL
    

class StoreURLDetailsModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField()
    Product_URL = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/',blank=True,null=True)
    reviews = models.TextField(null=True)
    review_count = models.IntegerField(default=0)
    ratings_count = models.IntegerField(default=0)

    sentiment = models.TextField(null=True)


    def __str__(self):
        return f" {self.id} - {self.title}"
