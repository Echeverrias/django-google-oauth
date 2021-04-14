from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    has_registered_with_this_app = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'({self.pk if self.pk else ""}) {self.username}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('get_user', args=(str(self.pk),))

class ProxyUser(User):

    """
    What is a Proxy Model?
    It is a model inheritance without creating a new table in the database.
    It is used to change the behaviour of an existing model (e.g. default ordering, add new methods, etc.)
     without affecting the existing database schema.

    When should I use a Proxy Model?
    You should use a Proxy Model to extend the existing User model when you don’t need to store
    extra information in the database, but simply add extra methods or change the model’s query Manager.
    """

    class Meta():
        proxy = True

    def say_hello(self):
        return f'Hello Im {self.username}'



class Profile(models.Model):

        """
        What is a One-To-One Link?
        It is a regular Django model that’s gonna have it’s own database table and will hold a
        One-To-One relationship with the existing User Model through a OneToOneField.

        When should I use a One-To-One Link?
        You should use a One-To-One Link when you need to store extra information about the existing User
        Model that’s not related to the authentication process. We usually call it a User Profile.
        """
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        bio = models.TextField(max_length=500, null=True, blank=True)
        location = models.CharField(max_length=30, null=True, blank=True)
        birth_date = models.DateField(null=True, blank=True)
        avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
        has_registered_with_this_app = models.BooleanField(default=False, null=True)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()