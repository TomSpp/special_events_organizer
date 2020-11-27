from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Location(models.Model):
    voivodeship = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    local_number = models.CharField(max_length=10)

    def __str__(self):
        return self.street + " " + self.local_number + " " + self.town


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
    added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique_for_date='added')

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.added.year, self.added.month,
                                                         self.added.day, self.slug])

    def __str__(self):
        return self.name


class Local(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    catering = models.OneToOneField(Catering, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique_for_date='added')

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.added.year, self.added.month,
                                                         self.added.day, self.slug])

    def __str__(self):
        return self.name


class OtherProvider(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique_for_date='added')

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('main_system:offer_detail', args=[self.added.year, self.added.month,
                                                         self.added.day, self.slug])

    def __str__(self):
        return self.name


class Offer(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, blank=True, null=True)
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE, blank=True, null=True)
    other_provider = models.ForeignKey(OtherProvider, on_delete=models.CASCADE, blank=True, null=True)
    max_people = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    offer_description = models.TextField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique_for_date='added')

    def get_absolute_url(self):
        return reverse('main_system:take_room_offer', args=[self.added.year, self.added.month,
                                                            self.added.day, self.slug])

    def __str__(self):
        if self.local is not None:
            provider_name = self.local.name
        elif self.catering is not None:
            provider_name = self.catering.name
        else:
            provider_name = self.other_provider.name
        return provider_name + " - " + str(self.name)


class Comment(models.Model):
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    other_provider = models.ForeignKey(OtherProvider, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Komentarz dodany przez {self.name} dla oferty .'
