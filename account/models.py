from django.db import models
from django.conf import settings
from main_system.models import Catering, Room, OtherOffer


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    caterings = models.ManyToManyField(Catering, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    other_offers = models.ManyToManyField(OtherOffer, blank=True)

    def __str__(self):
        return f'Profil użytkownika {self.user.username}'
