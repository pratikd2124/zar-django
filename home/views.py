from django.shortcuts import render, redirect, get_object_or_404
from main_app.models import Community, User, SupportTickets
from .models import Category,PagesData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from main_app.funtions import Send_Code_email, Send_Welcome_email, Send_Payment_email

# Create your views here.
import random

@login_required(login_url='login')
def all_users(request):
    users = User.objects.all().exclude(is_superuser=True,is_staff=True)
    
    community = request.GET.get('community')
    member_type = 'Community User'
    if community:
        users = users.filter(community__code=community)
    
    else:
        member_type = request.GET.get('memberType')
        
        if member_type == 'homeOwner':
            users = users.filter(type='Home Owner')
            
        elif member_type == 'materialProvider':
            users = users.filter(type='Material Provider')  
            
        elif member_type == 'serviceProvider':
            users = users.filter(type = 'Service Provider')
        else:
            users = users.filter(type='Community User')
    
    return render(request,'dashboard/all-users.html',{'title':'User List','users':users,'member_type':member_type})



@login_required(login_url='login')
def dashboard(request):
    
    return render(request,'dashboard/index.html',{'title':'Dashboard'})


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 messages.success(request, 'Login successful.')
#                 return redirect('dashboard')
#             else:
#                 messages.warning(request, 'Not authorized.')
#                 return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')
#             return redirect('login')
#     return render(request,'dashboard/login.html',{'title':'Login'})



@login_required(login_url='login')
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



@login_required(login_url='login')
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



@login_required(login_url='login')
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



def send_passcode(request):
    if request.method =='POST':
        uid =request.POST.get('user_id')
        user = User.objects.get(uid=uid)
        if request.GET.get('type')=='send_code':
            Send_Code_email(user.code,user.email)
            user.payment_status = 'Code Sent'
            user.save()
            return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
        
        payment_link = request.POST.get('link')
        if request.GET.get('type')=='send_payment_link':
            Send_Payment_email(payment_link,user.email)
            
        user.code = user.generate_unique_code()
        user.payment_status = 'In Progress'
        user.save()
        return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
    return redirect(request.META.get('HTTP_REFERER', '/dashboard'))


def edit_pages(request):
    page = request.GET.get('page')
    page_data = PagesData.objects.first()
    if request.method == 'POST':
        
        if page == 'Privacy-Policy':
            page_data.privacy_policy = request.POST.get('data')
        elif page == 'Terms-and-Condition':
            page_data.terms_and_conditions = request.POST.get('data')
        elif page=='Guide':
            page_data.guide = request.POST.get('data')
        elif page == 'FAQ':
            page_data.faq = request.POST.get('data')
        
        page_data.save()
    
    
    return render(request,'dashboard/edit_pages.html',{'title':'Edit Data','page':page,'page_data':page_data})


def support_ticket(request):
    tickets = SupportTickets.objects.all()
    if request.method == 'POST':
        if request.POST.get('type') == 'reply':
            ticket = SupportTickets.objects.get(id=request.POST.get('ticket_id'))
            ticket.reply = request.POST.get('reply')
            ticket.save()
            messages.success(request, 'Reply sent successfully.')
            return redirect('support_ticket')

        if request.POST.get('type') == 'delete':
            ticket = SupportTickets.objects.get(id=request.POST.get('ticket_id'))
            ticket.delete()
            messages.success(request, 'Ticket deleted successfully.')
            return redirect('support_ticket')

        if request.POST.get('type') == 'close':
            ticket = SupportTickets.objects.get(id=request.POST.get('ticket_id'))
            ticket.status = 'Closed'
            ticket.save()
            messages.success(request, 'Ticket closed successfully.')
            return redirect('support_ticket')

        if request.POST.get('type') == 'open':
            ticket = SupportTickets.objects.get(id=request.POST.get('ticket_id'))
            ticket.status = 'Open'
            ticket.save()
            messages.success(request, 'Ticket opened successfully.')
            return redirect('support_ticket')
    
    return render(request,'dashboard/support-ticket.html',{'title':'Support Ticket','tickets':tickets})


def update_brand(request,id):
    brand = User.objects.get(uid=id)
    categories = Category.objects.all()
    return render(request,'dashboard/update-brand.html',{'title':'Update Brand','brand':brand,'categories':categories})