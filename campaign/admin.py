from django.contrib import admin
from .models import Campaign, CampaignData

class CampaignAdmin(admin.ModelAdmin):
    model = Campaign
  
class CampaignDataAdmin(admin.ModelAdmin):
    model = CampaignData

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignData, CampaignDataAdmin)