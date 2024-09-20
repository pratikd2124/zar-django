# main_app/views.py
from django.shortcuts import render, redirect
from .forms import HomeOwnerForm, ServiceProviderForm, MaterialProviderForm

def home(request):
    return render(request, 'client/template.html')  

def validate(request):
    return render(request,'client/validate.html')

def home_owner_view(request):
    if request.method == 'POST':
        # Manually fetching form data
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        intrest = request.POST.get('intrest')

        # Creating a HomeOwner instance and saving it
        HomeOwner.objects.create(
            name=name,
            mobile=mobile,
            email=email,
            intrest=intrest
        )

        # Redirect to a success page or wherever after submission
        return redirect('success_page')
    
    return render(request, 'client/home-owner.html')




def submit_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ServiceProviderForm()
    return render(request, 'main_app/service_provider_form.html', {'form': form})

def submit_material_provider(request):
    if request.method == 'POST':
        form = MaterialProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = MaterialProviderForm()
    return render(request, 'main_app/material_provider_form.html', {'form': form})

def success_page(request):
    return render(request, 'main_app/success_page.html')
