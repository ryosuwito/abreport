from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from django.contrib.auth.models import User

class Campaign(models.Model):
    name = models.CharField(db_index=True,
            max_length = 100,
            help_text="Nama Campaign")
    photo = models.ImageField(upload_to = 'campaign_photo',
            blank=True,
            help_text="Foto Campaign")
    slug = AutoSlugField(max_length=100, 
            unique=True, 
            db_index=True,
            populate_from=('name',))
    description = models.TextField(blank=True,
            help_text="Deskripsi Campaign")
    is_archived = models.BooleanField(default = False,
            help_text="Centang untuk Menyembunyikan Campaign") 

    class Meta:
        verbose_name_plural = "Campaigns"


    def __str__(self):
       return self.name


    def get_photo_url(self):
        return "/media/%s" % (self.photo)
    def get_url(self):
        return "/campaign/detail/%s/" % (self.name.lower())

class CampaignData(models.Model):
    photo = models.ImageField(upload_to = 'campaign_data_photo',
            blank=True,
            help_text="Foto Campaign")
    campaign = models.ForeignKey(Campaign, 
            on_delete=models.SET_NULL,
            null=True,
            related_name="photos_in_campaign",
            help_text="Nama Campaign")
    uploader = models.ForeignKey(User, 
            on_delete=models.SET_NULL,
            null=True,
            related_name="photos_by_user",)

    is_approved = models.BooleanField(default = False,
            help_text="Centang untuk Menampilkan Data") 

    license_no = models.CharField(db_index=True,
    	    default="",
            max_length = 100,
            help_text="No Plat Driver")

    def get_photo_url(self):
        return "/media/%s" % (self.photo)

    class Meta:
        verbose_name_plural = "Photos"