import requests

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Customer,ContactUs

from .forms import CustomerForm,contactForm

from .tokens import account_activation_token


# Create your views here.
def add_customer(request):
    """
    Add a customer.
    """
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            query = Customer.objects.filter(email=email)
            send_email = True
            resend_email = False
            if query.exists():
                q = Customer.objects.get(email=email)
                if q.email_verified:
                    messages.error(request,'An account with this email address already exists.')
                    send_email = False
                else:
                    resend_email = True
            if send_email:
                customer = None
                if not resend_email:
                    customer = form.save(commit=False)
                    customer.save()
                else:
                    customer = q
                mail_subject = 'Activate your NetRMM Trial Account.'
                message = render_to_string('emails/acc_active_email.html', {
                    'user': customer,
                    'scheme':request.scheme,
                    'host':request.get_host(),
                    'uid':urlsafe_base64_encode(force_bytes(customer.pk)),
                    'token':account_activation_token.make_token(customer),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.content_subtype = "html" 
                email.send()
                if resend_email:
                    msg = "An account already exists with the email address, But not verified yet, we've sent you verification email again !"
                else:
                    msg = "Please check your inbox and click on activate to confirm your registration and activate your account."

                context = {
                    'msg':msg
                }
                return render(request,'emails/email_sent.html',context)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,form.fields[field].label + " : " + error)
            return redirect('customers:add_customer')    
    context = {
                'form': form,
                'bool':settings.DEBUG,
                'page_name': 'Add Customer'
                }
    return render(request, 'contact/get-started.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        # TODO: Defunct code
        # Start User Trial
        # company_name = user.company_name
        # user_details = {
        #         'user_details':{
        #             'first_name':user.firstname,
        #             'last_name':user.lastname,
        #             'email':user.email,
        #             'subdomain':user.subdomain,
        #             'phone_number':f"{user.phone_number.as_e164}",
        #             'country':user.country.code
        #         }
        #     }
            
        # if company_name:
        #     user_details['user_details']['company_name'] = company_name
        # print(user_details)
        # start_trial(user_details)
        
        return render(request,'emails/email_activate.html',{'page_name': 'Account Activation'})
    else:
        return HttpResponse('Activation link is invalid!')

def contact_us(request):
    form = contactForm()
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            messages.success(request,"Contact Request Recieved.")
            return redirect('customers:contact_us')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,form.fields[field].label + " : " + error)
            return redirect('customers:contact_us')
            
    context = {
                'page_name': 'Contact Us',
                'form': form,
            }
    return render(request,'contact/contact-us.html',context)

# TODO: Defunct code
def start_trial(user_details):
    if settings.DEBUG:
        api_url = "http://127.0.0.1:8002/api/configs/subdomain-registration/"
        api_key = 'se9vIzU3.LerJDccrbvrTuKaGXZQfdXHu26BiKdK1'
    else:
        api_url = "https://demo.netrmm.com/api/configs/subdomain-registration/"
        api_key = 'zWF0CkfY.7NAz021AkGMlmO2dPaY5em0ONEoTP9Jj'
        
    # Define headers with the API key
    headers = {
        'Authorization': f'Api-Key {api_key}',
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(api_url, json=user_details, headers=headers)

    # Check the response
    if response.status_code == 201:
        data = response.json()
        print(f"Username: {data['username']}")
        print(f"Password: {data['password']}")
        mail_subject = 'Welcome to NetRMM'
        message = render_to_string('emails/onboard_email.html', {
            'data':data,
            'user':user_details['user_details'],
        })
        to_email = user_details['user_details']['email']
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html" 
        email.send()
    else:
        print(f"Error: {response.status_code} - {response.text}")