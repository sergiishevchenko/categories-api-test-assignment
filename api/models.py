from django.db import models
from django.db.models.signals import post_save


class CategoryName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Category's names"


class Categories(models.Model):
    category = models.OneToOneField(CategoryName, on_delete=models.CASCADE, related_name='category_object')
    children = models.ManyToManyField(CategoryName)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category.name

    def create_profile(sender, **kwargs):
        category = kwargs["instance"]
        if kwargs["created"]:
            profile = Categories(category=category)
            profile.save()

    post_save.connect(create_profile, sender=CategoryName)
