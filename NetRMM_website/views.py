import json
import urllib.parse

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.conf import settings

from customers.forms import CustomerForm

from blogs.models import Article, Tag



def homepage(request):
    articles = Article.objects.all().order_by('-created_at')[:3]
    context = {
        'page_name':"Home",
        'articles':articles
    }
    return render(request, 'homepage/index.html',context)

def login(request):
    if request.method == "POST":
        # Extract form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember-me')
        if remember != 'on':    
            remember = 'off'
        subdomain = request.POST.get('subdomain')

        # Create JSON object
        data = {
            'username': username,
            'password': password,
            'remember': remember
        }
        print(data)
        # Convert to JSON string and URL-encode
        encoded_data = urllib.parse.quote(json.dumps(data))

        # Redirect to subdomain with encoded data as parameter
        if settings.DEBUG:
            redirect_url = f"http://127.0.0.1:8002/accounts/login?data={encoded_data}"
        else:
            redirect_url = f"https://{subdomain}.netrmm.com/accounts/login?data={encoded_data}"
        print(redirect_url)
        return HttpResponseRedirect(redirect_url)
    return render(request, 'accounts/login.html', {'page_name': 'Login'})

def buildwithnetrmm(request):
    return render(request, 'buildwithnetrmm/buildwithus.html', {'page_name': 'Build with NetRMM'})

def pricing(request):
    return render(request, 'pricing/pricing.html', {'page_name': 'Pricing'})

def features(request):
    return render(request, 'features/features.html', {'page_name': 'Features'})

def faqs(request):
    return render(request, 'faq/faq.html', {'page_name': 'FAQs'})

def about(request):
    return render(request, 'about/about.html', {'page_name': 'About Us'})

def featurerequest(request):
    return render(request, 'featurerequest/featurerequest.html', {'page_name': 'Feature Request'})

def privacy_policy(request):
    return render(request, 'legal_pages/privacy_policy.html', {'page_name': 'Privacy Policy'})

def terms_of_service(request):
    return render(request, 'legal_pages/terms_of_service.html', {'page_name': 'Terms of Service'})

def security(request):
    return render(request, 'legal_pages/security.html', {'page_name': 'Security'})

def careers(request):
    return render(request, 'careers/careers.html', {'page_name': 'Careers'})