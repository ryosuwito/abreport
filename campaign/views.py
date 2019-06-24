from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from wsgiref.util import FileWrapper
from .models import Campaign, CampaignData

from zipfile import *
from datetime import datetime

@csrf_exempt
def upload_bukti_tayang(request, campaign_name, *args, **kwargs):
    files = request.FILES.getlist('photos') #'file_field' --> 'imagen' for you
    license_no = ""
    if request.method == "POST":
        if request.POST.get("license_no"):
            user = User.objects.get(username="driver")
            license_no = request.POST.get("license_no").replace(" ","").lower()
        if not request.user.is_authenticated:
            user = User.objects.get(username="project")
        else:
            user = request.user
    
        try:
            campaign = Campaign.objects.get(name=campaign_name.lower())
        except:
            return JsonResponse({"status":"Upload Failed"})    	
        for file in files:
            bukti_tayang = CampaignData.objects.create(campaign=campaign, photo=file, uploader=user, license_no=license_no)
        if files:
            return HttpResponseRedirect("/campaign/detail/%s/"%campaign_name)
        else:
            return JsonResponse({"status":"file empty"})
    else:	
        return render(request, "campaign/upload.html",
            {"campaign_name":campaign_name})

def download_image(request, campaign_name, *args, **kwargs):
    images=CampaignData.objects.filter(campaign__name=campaign_name)
    if images:
        with ZipFile('%s.zip'%campaign_name.lower(), 'w') as export_zip:
            for image in images:
                image_path = image.photo.path
                image_name = image.photo.name; # Get your file name here.
                export_zip.write(image_path, image_name)
    else:
        return JsonResponse({"status":"file empty"})


    wrapper = FileWrapper(open('%s.zip'%campaign_name.lower(), 'rb'))
    content_type = 'application/zip'
    content_disposition = 'attachment; filename=%s_%s.zip'%(campaign_name.lower(), datetime.now().strftime("%d-%m-%Y"))

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition
    return response

def photo_by_campaign(request, campaign_name, *args, **kwargs):
	campaign_data = CampaignData.objects.filter(campaign__name=campaign_name)
	return render(request, "campaign/detail.html",
		{"campaign_data":campaign_data,
		"campaign_name":campaign_name})

def photo_by_driver(request, campaign_name, license_no, *args, **kwargs):
	campaign_data = CampaignData.objects.filter(campaign__name=campaign_name,
		license_no=license_no)
    if not campaign_data:
	    return JsonResponse({"status":"file empty"})
	else:
		data = []
		for cd in campaign_data:
			data.append(cd.get_photo_url)
		return JsonResponse({"status":"OK",
			"data":data})

def index(request, *args, **kwargs):
	campaigns = Campaign.objects.all()
	return render(request, "campaign/index.html",
		{"campaigns":campaigns})