from django.contrib import admin
from .models import Location, Contact, Local, Catering, Offer, Comment, OtherProvider

admin.site.register(Location)
admin.site.register(Contact)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(OtherProvider)
class OtherProviderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Comment)
