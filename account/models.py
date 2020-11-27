from django.db import models
from django.conf import settings
from main_system.models import Offer


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offers = models.ManyToManyField(Offer, blank=True, related_name='offers')

    def __str__(self):
        return f'Profil użytkownika {self.user.username}'
