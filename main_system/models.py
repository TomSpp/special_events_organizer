from django.db import models
from django.urls import reverse


class Location(models.Model):
    voivodeship = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    local_number = models.CharField(max_length=10)

    def __str__(self):
        return self.street + " " + self.local_number + " " + self.town + ", powiat " + self.district +\
               ", województwo " + self.voivodeship


class Contact(models.Model):
    phone_number = models.CharField(max_length=20)
    website = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        string_website = self.website
        string_email = self.email
        if string_website is None:
            string_website = ""
        if string_email is None:
            string_email = ""

        return self.phone_number + " " + string_website + " " + string_email


class Catering(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    with_local_only = models.BooleanField(default=False)
    min_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    basic_offer = models.CharField(max_length=1000, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.id, self.name])

    def __str__(self):
        return self.name


class Local(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    catering = models.OneToOneField(Catering, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.id, self.name])

    def __str__(self):
        return self.name


class Room(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    max_people = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_parquet = models.CharField(max_length=100, null=True, blank=True)
    air_conditioned = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.local.__str__() + " - " + str(self.max_people) + " osób"


class OtherOffer(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    min_cost = models.DecimalField(max_digits=10, decimal_places=2)
    basic_offer = models.CharField(max_length=1000, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.id, self.name])

    def __str__(self):
        return self.name


class Comment(models.Model):
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    other_offer = models.ForeignKey(OtherOffer, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Komentarz dodany przez {self.name} dla oferty .'