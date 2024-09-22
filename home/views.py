from django.shortcuts import render, redirect, get_object_or_404
from main_app.models import Community, User
from .models import Category
from django.contrib import messages
# Create your views here.
import random
def all_users(request):
    users = User.objects.all().exclude(is_superuser=True,is_staff=True).filter(type='Community User')
    
    community = request.GET.get('community')
    if community:
        users = users.filter(community__code=community)
    
    member_type = 'all_users'
    
    member_type = request.GET.get('memberType')
    if member_type == 'homeOwner':
        users = users.filter(type='Home Owner')
        
    if member_type == 'materialProvider':
        users = users.filter(type='Material Provider')  
        
    if member_type == 'serviceProvider':
        users = users.filter(type = 'Service Provider')
    
    return render(request,'dashboard/all-users.html',{'title':'User List','users':users,'member_type':member_type})




def dashboard(request):
    return render(request,'dashboard/index.html',{'title':'Dashboard'})



def all_community(request):
    community = Community.objects.all()
    if request.method == 'POST':
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        community = Community.objects.create(name=name,description=description)
        community.save()
        messages.success(request, 'Community created successfully.')
        return redirect('all_community')
    
    if request.GET.get('type') == 'regenerate':
        id = request.GET.get('id')
        community = Community.objects.get(id=id)
        community.code = community.generate_unique_code()
        community.save()
        messages.success(request, 'Community code regenerated successfully.')
        return redirect('all_community')
        
    
    if request.GET.get('type') == 'delete':
        id = request.GET.get('id')
        community = Community.objects.get(id=id)
        community.delete()
        messages.success(request, 'Community deleted successfully.')

        return redirect('all_community')
    
    
    return render(request,'dashboard/community.html',{ 'title':'Community' ,'community':community})


def all_category(request):
    categories = Category.objects.order_by('-id').all()
    
    if request.method == 'POST':
        if request.GET.get('type') == 'edit':
            id = request.POST.get('category_id')
            category = Category.objects.get(id=id)
            name = request.POST.get('name')
            parent = request.POST.get('parent')
            image = request.FILES.get('image')
            category.name = name
            if parent!='':
                category.parent = Category.objects.get(id=parent)
            category.parent = Category.objects.get(id=parent)
            if image:
                category.image = image
            
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
        
        
        name = request.POST.get('name')
        parent = request.POST.get('parent')
        image = request.FILES.get('image')
        category = Category.objects.create(name=name,image=image)
        if parent!='':
            category.parent = Category.objects.get(id=parent)
        category.save()
        messages.success(request, 'Category created successfully.')
        return redirect('category_list')
    
    if request.GET.get('type') == 'delete':
        id = request.GET.get('id')
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    
    
    return render(request,'dashboard/category.html',{'title':'Category','categories':categories})

def all_brand(request):
    brands = User.objects.order_by('-id').filter(type='Material Provider')
    categories = Category.objects.all()
    
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     category = request.POST.get('category')
    #     logo = request.FILES.get('logo')
    #     contact_person = request.POST.get('contact_person')
    #     email = request.POST.get('email')
    #     phone = request.POST.get('phone')
    #     address = request.POST.get('address')
    #     city = request.POST.get('city')
    #     state = request.POST.get('state')
    #     zip_code = request.POST.get('zip_code')
    #     country = request.POST.get('country')
        
        
        
    #     brand = Brand.objects.create(name=name,category=Category.objects.get(id=category),logo=logo,contact_person=contact_person,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code,country=country)
    #     brand.save()
    #     messages.success(request, 'Brand created successfully.')
    #     return redirect('brand_list')
        
        
        
    return render(request,'dashboard/brands.html',{'title':'Brand','brands':brands,'categories':categories})