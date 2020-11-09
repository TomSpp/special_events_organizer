from django.db import models


class Location(models.Model):
    voivodeship = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

    def __str__(self):
        return self.town + ", powiat " + self.district + ", województwo " + self.voivodeship


class Contact(models.Model):
    phone_number = models.CharField(max_length=20)
    website = models.URLField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.phone_number + " " + self.website + " " + self.email


class Catering(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    with_local_only = models.BooleanField(default=False)
    min_cost_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    basic_offer = models.CharField(max_length=1000, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Local(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    catering = models.OneToOneField(Catering, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    max_people = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_parquet = models.CharField(max_length=100, null=True)
    air_conditioned = models.BooleanField(null=True)

    def __str__(self):
        return self.local + " - " + self.max_people + " osób"


class OtherOffer(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    min_cost = models.DecimalField(max_digits=10, decimal_places=2)
    basic_offer = models.CharField(max_length=1000, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
