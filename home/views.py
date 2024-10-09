from django.shortcuts import render, redirect, get_object_or_404
from main_app.models import Community, User, SupportTickets,ProfileGallery,ConnectImpress,ProfileInfo,ContactPageDetails,TermsAndConditionsSection, PrivacyPolicySection, FAQSection,CustomEmail
from .models import Category,PagesData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from main_app.funtions import Send_Code_email, Send_Welcome_email, Send_Payment_email
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
import random
from .analytics import *
import json


@login_required(login_url='login')
def dashboard(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    categories = Category.objects.all()
    users = User.objects.all().exclude(is_superuser=True, is_staff=True)
    
    # Get analytics data from log files
    monthly_active_users_list, last_week_active_users_list, category_wise_visited_users_count,country_wise_users_count = analyze_user_activity_from_logs()
    last_week_active_users_list_json = json.dumps(last_week_active_users_list)
    monthly_active_users_list_json = json.dumps(monthly_active_users_list)
    category_wise_visited_users_count_json = json.dumps(category_wise_visited_users_count)
    country_wise_users_count = json.dumps(country_wise_users_count)
    
    material_provider_count = User.objects.filter(type='Material Provider').count()

    
    
    
    return render(request, 'dashboard/index.html', {
        'title': 'Dashboard',
        'categories': categories,
        'material_provider_count':material_provider_count,
        'Service_Provider_count':users.filter(type='Service Provider').count(),
        'Home_Owner_count':users.filter(type__in=['Home Owner', 'Community User']).count(),
        'users': users,
        'last_week_active_users_list': last_week_active_users_list_json,
        'monthly_active_users': monthly_active_users_list_json,
        'category_wise_visited_users_count': category_wise_visited_users_count_json,
        'country_wise_users_count':country_wise_users_count
    })








@login_required(login_url='login')
def all_users(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    if request.GET.get('action') == 'delete':
        id = request.GET.get('id')
        user = User.objects.get(uid=id)
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    
    
    
    users = User.objects.order_by('-id').all().exclude(is_superuser=True,is_staff=True)
    if request.GET.get('search'):
        query = request.GET.get('search')
        users = users.filter(Q(first_name__icontains =query)|Q(last_name__icontains=query)|Q(mobile__icontains=query)|Q(email__icontains=query))    
   
    community = request.GET.get('community')
    member_type = request.GET.get('memberType')
    
    if community or member_type:
        if community:
            users = users.filter(community__code=community)
        
        else:
            
            if member_type == 'homeOwner':
                users = users.filter(type='Home Owner')
                
            else:
                users = users.filter(type='Community User')
    else:
        users = users.filter(type__in= ['Home Owner', 'Community User'])
        member_type = 'all'
        
    
    page = request.GET.get('page', 1)  # Get the page number from the request
    paginator = Paginator(users, 5)  # Show 10 providers per page

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)  # If page is not an integer, show the first page
    except EmptyPage:
        users = paginator.page(paginator.num_pages)  # If page is out of range, show the last page
        
    return render(request,'dashboard/all-users.html',{'title':'User List','users':users,'member_type':member_type})




@login_required(login_url='login')
def all_community(request):
    community = Community.objects.order_by('-id').all()
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
def service_providers(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    providers_list = User.objects.order_by('-id').filter(type='Service Provider')
    categories = Category.objects.order_by('-id').all()
    if request.GET.get('search'):
        query = request.GET.get('search')
        providers_list = providers_list.filter(Q(first_name__icontains =query)|Q(last_name__icontains=query)|Q(mobile__icontains=query)|Q(email__icontains=query))    
    # Pagination setup
    page = request.GET.get('page', 1)  # Get the page number from the request
    paginator = Paginator(providers_list, 5)  # Show 10 providers per page

    try:
        providers = paginator.page(page)
    except PageNotAnInteger:
        providers = paginator.page(1)  # If page is not an integer, show the first page
    except EmptyPage:
        providers = paginator.page(paginator.num_pages)  # If page is out of range, show the last page

    return render(request, 'dashboard/service-provider.html', {
        'title': 'Service Provider',
        'providers': providers,
        'categories': categories
    })








@login_required(login_url='login')
def all_category(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    # Get all categories
    categories_list = Category.objects.order_by('-id').all()
    if request.GET.get('search'):
        query = request.GET.get('search')
        categories_list = categories_list.filter(Q(name__icontains =query)|Q(parent__name__icontains=query))    
    # Set up pagination
    page = request.GET.get('page', 1)  # Get the page number from the request, default is page 1
    paginator = Paginator(categories_list, 5)  # Show 10 categories per page

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        categories = paginator.page(paginator.num_pages)

    # Handle POST requests for Create and Edit
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        image = request.FILES.get('image')

        # Edit Category
        if request.GET.get('type') == 'edit':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category.name = name
            if parent_id:
                category.parent = get_object_or_404(Category, id=parent_id)
            if image:
                category.image = image
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')

        # Create Category
        else:
            category = Category.objects.create(name=name, image=image)
            if parent_id:
                category.parent = get_object_or_404(Category, id=parent_id)
            category.save()
            messages.success(request, 'Category created successfully.')
            return redirect('category_list')

    # Handle GET requests for Delete
    if request.GET.get('type') == 'delete':
        category_id = request.GET.get('id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

    # Render the categories page with paginated categories
    return render(request, 'dashboard/category.html', {
        'title': 'Category',
        'categories': categories  # Pass paginated categories here
    })



@login_required(login_url='login')
def all_brand(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    brands = User.objects.order_by('-id').filter(type='Material Provider')
    categories = Category.objects.order_by('-id').all()
    
    
    if request.GET.get('search'):
        query = request.GET.get('search')
        brands = brands.filter(Q(brand_name__icontains=query) | Q(email__icontains=query) | Q(mobile__icontains=query) | Q(contact_person__icontains=query))
    
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
        
    page = request.GET.get('page', 1)  # Get the page number from the request
    paginator = Paginator(brands, 10)  # Show 10 providers per page

    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)  # If page is not an integer, show the first page
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)  # If page is out of range, show the last page
        
    return render(request,'dashboard/brands.html',{'title':'Brand','brands':brands,'categories':categories})


@login_required(login_url='login')
def send_passcode(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    if request.method =='POST':
        uid =request.POST.get('user_id')
        profile_id = request.POST.get('profile_id')
        
        user = User.objects.get(uid=uid)
        if profile_id:
            profile = ProfileInfo.objects.get(id=profile_id)
        
        payment_link = request.POST.get('link')
        
        if request.GET.get('type')=='send_code':
            user.code = user.generate_unique_code()
            user.save()
            if user.type== 'Material Provider':
                    name = user.brand_name
            else:
                    name = str(user.first_name + ' '+user.last_name)
            Send_Code_email(user.code,user.email,name)
            if profile_id:
                profile.payment_status = 'Code Sent'
                profile.save()
            else:
                user.payment_status = 'Code Sent'
                user.save()
                
            messages.success(request, 'Code Sent Successfully.')
            return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
        
        if request.GET.get('type')=='send_payment_link':
            if payment_link:
                if user.type== 'Material Provider':
                    name = user.brand_name
                else:
                    name = str(user.first_name + ' '+user.last_name)
                Send_Payment_email(payment_link,user.email,name)
            else:
                messages.error(request, 'Payment Link is Required.')
                return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
            
            
        user.code = user.generate_unique_code()
        if profile_id:
            profile.payment_status = 'In Process'
            profile.save()
        else:
            user.payment_status = 'In Process'
            user.save()
            
            
        messages.success(request, 'Payment Link Sent Successfully.')
        return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
    return redirect(request.META.get('HTTP_REFERER', '/dashboard'))


@login_required(login_url='login')
def edit_pages(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
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


@login_required(login_url='login')
def support_ticket(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    tickets = SupportTickets.objects.order_by('-id').all()
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



@login_required(login_url='login')
def update_brand(request,id):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    brand = User.objects.get(uid=id)
    end_nodes = Category.objects.annotate(num_children=Count('children')).filter(num_children=0)
    selected_categories = brand.category.all()
    
    if request.GET.get('type')=='delete':
        id  = request.GET.get('image_id')
        profile_id = request.GET.get('profile_id')
        if profile_id:
            ProfileInfo.objects.get(id=profile_id).delete()
            messages.success(request, 'Profile deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        elif id:
            img = ProfileGallery.objects.get(id=id).delete()
            messages.success(request, 'Image deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        else:
            brand.delete()
            messages.success(request, 'Brand deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    if request.method == 'POST':
            if request.GET.get('type') == 'basic_info':
                brand_name = request.POST.get('brand_name')
                designation = request.POST.get('designation')
                contact_person = request.POST.get('contact_person_name')
                mobile = request.POST.get('mobile')
                firm_address = request.POST.get('firmAddress')
                country = request.POST.get('country')
                state = request.POST.get('state')
                city = request.POST.get('city')
                pincode = request.POST.get('pincode')
                new_categories = request.POST.get('new_categories')
                verified = request.POST.get('verified')
                
                
                brand.brand_name = brand_name
                brand.designation = designation
                brand.contact_person = contact_person
                
                brand.mobile = mobile
                brand.address = firm_address
                brand.country = country
                brand.state = state
                brand.city = city
                brand.zip_code = pincode
                if verified == 'Yes':
                    brand.is_active = True
                else:
                    brand.is_active = False
                
                
                brand.save()
                if new_categories:
                    for cat in  new_categories.split(','):
                            profile = ProfileInfo.objects.create(   
                            category = Category.objects.get(id=cat)
                            )
                            profile.save()
                            brand.profile.add(profile)
                            brand.save()
                            messages.success(request, 'New Category added successfully!!')
                            messages.info(request, 'New Category Under Review!')
                            return redirect(request.META.get('HTTP_REFERER', '/home'))
                    
                messages.success(request, 'Profile updated successfully')
                return redirect(request.META.get('HTTP_REFERER', '/home'))
            
            if request.GET.get('type') == 'professional':
                
                profile_id = request.GET.get('id')
                if profile_id:
                    profile = ProfileInfo.objects.get(id=profile_id)
                    bio = request.POST.get(f'bio{profile_id}')
                    
                    brand_name = request.POST.get(f'brand_name{profile_id}')
                    contact_person = request.POST.get(f'contact_person{profile_id}')
                    contact_number = request.POST.get(f'contact_number{profile_id}')
                    designation = request.POST.get(f'designation{profile_id}')
                    linked = request.POST.get(f'linkedin{profile_id}')
                    website = request.POST.get(f'website{profile_id}')
                    facebook = request.POST.get(f'facebook{profile_id}')
                    instagram = request.POST.get(f'instagram{profile_id}')
                    twitter = request.POST.get(f'twitter{profile_id}')
                    visible = request.POST.get(f'visible{profile_id}')
                    profilepic = request.FILES.get(f'profilepic{profile_id}')
                    brandlogo = request.FILES.get(f'brandlogo{profile_id}')
                    profileDocInput = request.FILES.get(f'profileDocInput{profile_id}')
                    visible = request.POST.get(f'visible{profile_id}')
                    verified = request.POST.get(f'verified{profile_id}')
                    payment_status = request.POST.get(f'payment_status{profile_id}')
                    
                    
                    profile.brand_name = brand_name
                    profile.contact_person = contact_person
                    profile.contact_number = contact_number
                    profile.designation = designation
                    profile.bio = bio
                    profile.social_links= {
                        "linkedin": linked,
                        "website": website,
                        "facebook": facebook,
                        "instagram": instagram,
                        "twitter": twitter
                    }
                    if profilepic:
                        profile.profile_pic = profilepic
                    if brandlogo:
                        profile.brand_logo = brandlogo
                    if profileDocInput:
                        profile.profile_doc = profileDocInput
                        
                    if verified == 'Yes':
                        profile.is_active = True
                    else:
                        profile.is_active = False
                        
                    profile.payment_status = payment_status
                    
                    if visible == 'Yes':
                        profile.visible = True
                    else:
                        profile.visible = False

                    profile.save()
                    messages.success(request, 'Profile updated successfully')
                    return redirect(request.META.get('HTTP_REFERER', '/home'))
                
                
            if request.GET.get('type') == 'gallery':
                profile_id = request.GET.get('id')
                if profile_id:
                    profile = ProfileInfo.objects.get(id=profile_id)
                    image = request.FILES.getlist('img')
                    if image:
                        for img in image:
                            profile_gallery = ProfileGallery.objects.create(image=img)
                            profile.profile_gallery.add(profile_gallery)
                            profile.save()
                        messages.success(request, 'Gallery updated successfully')
                        return redirect(request.META.get('HTTP_REFERER', '/home'))

    
    
    return render(request,'dashboard/update-brand.html',{'selected_categories':selected_categories,'title':'Update Brand','brand':brand,'categories':end_nodes})





@login_required(login_url='login')
def update_service(request,id):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    user = User.objects.get(uid=id)
    end_nodes = Category.objects.annotate(num_children=Count('children')).filter(num_children=0)
    
    
    if request.GET.get('type')=='delete':
        id  = request.GET.get('image_id')
        profile_id = request.GET.get('profile_id')
        if profile_id:
            ProfileInfo.objects.get(id=profile_id).delete()
            messages.success(request, 'Profile deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        if id:
            img = ProfileGallery.objects.get(id=id).delete()
            messages.success(request, 'Image deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    if request.method == 'POST':

        
            if request.GET.get('type') == 'basic_info':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                
                mobile = request.POST.get('mobile')
                firm_name = request.POST.get('firmName')
                firm_address = request.POST.get('firmAddress')
                country = request.POST.get('country')
                state = request.POST.get('state')
                city = request.POST.get('city')
                pincode = request.POST.get('pincode')
                new_categories = request.POST.get('new_categories')
                verified = request.POST.get('verified')
                
                
                user.mobile = mobile
                user.firm_name = firm_name
                user.first_name = first_name
                user.last_name = last_name

                user.address = firm_address
                user.country = country
                user.state = state
                user.city = city
                user.zip_code = pincode
                if verified == 'Yes':
                    user.is_active = True
                else:
                    user.is_active = False
                
                user.save()
                if new_categories:
                    for cat in  new_categories.split(','):
                        profile = ProfileInfo.objects.create(   
                        category = Category.objects.get(id=cat)
                        )
                        profile.save()
                        user.profile.add(profile)
                        user.save()
                        messages.success(request, 'New Category added successfully!!')
                        messages.info(request, 'New Category Under Review!')
                        return redirect(request.META.get('HTTP_REFERER', '/home'))
                
                
                messages.success(request, 'Profile updated successfully')
                return redirect(request.META.get('HTTP_REFERER', '/home'))
            
            if request.GET.get('type') == 'professional':
                
                profile_id = request.GET.get('id')
                if profile_id:
                    profile = ProfileInfo.objects.get(id=profile_id)
                    bio = request.POST.get(f'bio{profile_id}')
                    
                    linked = request.POST.get(f'linkedin{profile_id}')
                    website = request.POST.get(f'website{profile_id}')
                    facebook = request.POST.get(f'facebook{profile_id}')
                    instagram = request.POST.get(f'instagram{profile_id}')
                    twitter = request.POST.get(f'twitter{profile_id}')
                    visible = request.POST.get(f'visible{profile_id}')
                    verified = request.POST.get(f'verified{profile_id}')
                    payment_status = request.POST.get(f'payment_status{profile_id}')
                    profilepic = request.FILES.get(f'profilepic{profile_id}')
                    brandlogo = request.FILES.get(f'brandlogo{profile_id}')
                    profileDocInput = request.FILES.get(f'profileDocInput{profile_id}')
                    
                    profile.bio = bio
                    profile.social_links= {
                        "linkedin": linked,
                        "website": website,
                        "facebook": facebook,
                        "instagram": instagram,
                        "twitter": twitter
                    }
                    if profilepic:
                        profile.profile_pic = profilepic
                    if brandlogo:
                        profile.brand_logo = brandlogo
                    if profileDocInput:
                        profile.profile_doc = profileDocInput
                    
                    if verified == 'Yes':
                        profile.is_active = True
                    else:
                        profile.is_active = False
                        
                    profile.payment_status = payment_status
                    
                    if visible == 'Yes':
                        profile.visible = True
                    else:
                        profile.visible = False
                    profile.save()
                    messages.success(request, 'Profile updated successfully')
                    return redirect(request.META.get('HTTP_REFERER', '/home'))
                
                
                
            if request.GET.get('type') == 'gallery':
                profile_id = request.GET.get('id')
                if profile_id:
                    profile = ProfileInfo.objects.get(id=profile_id)
                    image = request.FILES.getlist('img')
                    if image:
                        for img in image:
                            profile_gallery = ProfileGallery.objects.create(image=img)
                            profile.profile_gallery.add(profile_gallery)
                            profile.save()
                        messages.success(request, 'Gallery updated successfully')
                        return redirect(request.META.get('HTTP_REFERER', '/home'))
    
    
    return render(request,'dashboard/update-service.html',{'title':'Update Brand','brand':user,'categories':end_nodes})


@login_required(login_url='login')
def update_gallery(request,id):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    user = User.objects.get(uid=id)
    gallery = ProfileGallery.objects.filter(user = user)
    
    if request.GET.get('type') == 'delete':
            gallery = ProfileGallery.objects.get(id=request.GET.get('img_id'))
            gallery.delete()
            messages.success(request, 'image deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    if request.method == 'POST':
        
        
        
        
        if request.GET.get('type') == 'Add':

            img = request.FILES.get('img')
            if img:
                gallery = ProfileGallery.objects.create(user=user,image=img)
                gallery.save()
                user.profile_gallery.add(gallery)
                user.save()
                messages.success(request, 'Gallery updated successfully.')
                return redirect(request.META.get('HTTP_REFERER'))
            
         
        
        
    return render(request,'dashboard/update-gallery.html',{'title':'Update Gallery','gallery':gallery,'user':user})



@login_required(login_url='login')
def update_user_info(request,id):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    user = User.objects.get(uid=id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('contact')
        email = request.POST.get('email')   
        verified = request.POST.get('verified')  
        payment_status = request.POST.get('payment_status')  
        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.email = email
        if verified == 'Yes':
            user.is_active = True
        else:
            user.is_active = False
        if payment_status:
            user.payment_status = payment_status
        user.save()
        messages.success(request, 'Information updated successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'dashboard/user-edit.html',{'title':'Update User Info','user':user})


# from main_app.models import ContactPageDetails
@login_required(login_url='login')
def contact_page(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        contact_number = request.POST.get('mobile')
        address = request.POST.get('address')
        twitter = request.POST.get('twitter')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        linkedin = request.POST.get('linkedin')
        contact = ContactPageDetails.objects.first()
        if contact:
            contact.email = email
            contact.phone = contact_number
            contact.address = address
            contact.facebook = facebook
            contact.twitter = twitter
            contact.instagram = instagram
            contact.linkedin = linkedin
            contact.save()
        else:
            contact = ContactPageDetails.objects.create(email=email,phone=contact_number,address=address,facebook=facebook,twitter=twitter,instagram=instagram,linkedin=linkedin)
            contact.save()
            messages.success(request, 'Information updated successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        messages.success(request, 'Message sent successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    
    
    contact = ContactPageDetails.objects.first()
    return render(request,'dashboard/contact-page.html',{'title':'Contact Page','contact':contact})



import csv
from django.http import HttpResponse
import csv


def export(request):
    user_type = request.GET.get('type', None)
    
    # Filter users based on the type (if provided)
    if user_type == 'material_provider':
        users = User.objects.filter(type='Material Provider')
    elif user_type == 'service_provider':
        users = User.objects.filter(type='Service Provider')
    elif user_type == 'home_owner':
        users = User.objects.filter(type='Home Owner')
    else:
        users = User.objects.filter(type__in=['Community User','Home Owner'])
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user_type}_users.csv"'

    writer = csv.writer(response)

    # Helper function to handle null or blank values
    def handle_na(value):
        if not value:
            return "N/A"
        return value
    
    # Write header row
    if user_type == 'material_provider':
        writer.writerow([
            'Account Type','UID', 'Username', 'Email', 'Brand Name', 'Category Path', 'Contact Person Name',
            'Contact Number', 'Designation', 'Address', 'Country', 'State', 'City', 'Zip Code',
            'Category Brand Name', 'Category Contact Person Name', 'Category Contact Number',
            'Category Designation', 'Bio', 'Payment Status', 'Is Verified', 'Is Active',
            'Facebook', 'Website', 'Instagram', 'LinkedIn'
        ])

        # Write data rows
        for user in users:
            for profile in user.profile.all():
                writer.writerow([
                    user.type,
                    handle_na(user.uid),
                    handle_na(user.username),
                    handle_na(user.email),
                    handle_na(user.brand_name),
                    handle_na(profile.category.get_category_hierarchy() if profile.category else None),
                    handle_na(profile.contact_person),
                    handle_na(profile.contact_number),
                    handle_na(profile.designation),
                    handle_na(user.address),
                    handle_na(user.country),
                    handle_na(user.state),
                    handle_na(user.city),
                    handle_na(user.zip_code),
                    handle_na(profile.brand_name),
                    handle_na(profile.contact_person),
                    handle_na(profile.contact_number),
                    handle_na(profile.designation),
                    handle_na(profile.bio),
                    handle_na(profile.payment_status),
                    handle_na(profile.is_active),
                    handle_na(user.is_active),
                    handle_na(profile.social_links.get('facebook', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('website', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('instagram', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('linkedin', "N/A") if profile.social_links else "N/A"),
                ])
        
    elif user_type == 'service_provider':
        writer.writerow([
            'Account Type','UID', 'Username', 'Email', 'First Name','Last Name' ,'Category Path',
            'Contact Number', 'Firm Name', 'Address', 'Country', 'State', 'City', 'Zip Code',
             'Bio', 'Payment Status', 'Is Verified', 'Is Active',
            'Facebook', 'Website', 'Instagram', 'LinkedIn'
        ])
    
          # Write data rows
        for user in users:
            for profile in user.profile.all():
                writer.writerow([
                    user.type,
                    handle_na(user.uid),
                    handle_na(user.username),
                    handle_na(user.email),
                    handle_na(user.first_name),
                    handle_na(user.last_name),
                    handle_na(profile.category.get_category_hierarchy() if profile.category else None),

                    handle_na(user.mobile),
                    handle_na(user.firm_name),
                    handle_na(user.address),
                    handle_na(user.country),
                    handle_na(user.state),
                    handle_na(user.city),
                    handle_na(user.zip_code),
                 
                    handle_na(profile.bio),
                    handle_na(profile.payment_status),
                    handle_na(profile.is_active),
                    handle_na(user.is_active),
                    handle_na(profile.social_links.get('facebook', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('website', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('instagram', "N/A") if profile.social_links else "N/A"),
                    handle_na(profile.social_links.get('linkedin', "N/A") if profile.social_links else "N/A"),
                ])
        
    else:
        writer.writerow([
            'Account Type','UID', 'Username', 'Email', 'First Name','Last Name', 
            'mobile',
            'Payment Status', 'Is Verified', 'Is Active',
        ])

        # Write data rows
        for user in users:
            for profile in user.profile.all():
                writer.writerow([
                    user.type,
                    handle_na(user.uid),
                    handle_na(user.username),
                    handle_na(user.email),
                    handle_na(user.first_name),
                    handle_na(user.last_name),
                    handle_na(user.mobile),
                    handle_na(user.payment_status),
                    handle_na(user.is_active),
                ])    
    
    return response


# def detail_analytics(request,id):
#     user = User.objects.get(uid=id)
#     logs = get_all_user_activity_logs(user)
#     print(logs)

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension
from django.shortcuts import render
from collections import Counter

# Your Google Analytics Measurement ID (should be numeric property ID)
PROPERTY_ID = '456257370'  # Replace with your actual numeric property ID

def initialize_analyticsreporting():
    """Initializes a Google Analytics Data API client."""
    
    credentials = service_account.Credentials.from_service_account_file(
        '/home/ubuntu/zar-django/ga-credential.json',
        scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    
    # Build the service
    client = BetaAnalyticsDataClient(credentials=credentials)
    return client

def get_report(client):
    """Queries the Google Analytics Data API."""
    
    request = RunReportRequest(
        property=f'properties/{PROPERTY_ID}',
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        metrics=[Metric(name="sessions"), Metric(name="totalUsers"), Metric(name="screenPageViews")],
        dimensions=[Dimension(name="date")]
    )
    
    response = client.run_report(request)
    return response

def parse_response(response):
    """Parses and formats the Google Analytics Data API response."""
    
    formatted_data = []
    for row in response.rows:
        formatted_data.append({
            'date': row.dimension_values[0].value,
            'sessions': row.metric_values[0].value,
            'users': row.metric_values[1].value,
            'pageviews': row.metric_values[2].value,
        })
    return formatted_data

def detail_analytics(request, id):
    # Initialize Google Analytics
    user = User.objects.get(uid=id)
    # client = initialize_analyticsreporting()
    
    # # Get the report data
    # response = get_report(client)
    
    # # Parse the response to get relevant data
    # analytics_data = parse_response(response)
    data = get_all_user_activity_logs(user)
    # Extract the page_visited values
    page_visits = [item['page_visited'] for item in data]

    # Use Counter to get unique page visits with their counts
    page_count = Counter(page_visits)

    # Output the result
    for page, count in page_count.items():
        print(f"{page}: {count}")
    # Render the dashboard template
    return render(request, 'dashboard/detail_analytics.html', {'title': 'Detailed Analytics', 'user': user, 'log': page_count})


# views.py
@login_required(login_url='login')
def terms_view(request):
    # Handle GET request to display sections and the form
    sections = TermsAndConditionsSection.objects.all().order_by('order')

    # Check if there's an 'edit' parameter in the URL
    section_to_edit = None
    edit_section_id = request.GET.get('edit')
    if edit_section_id:
        section_to_edit = get_object_or_404(TermsAndConditionsSection, id=edit_section_id)

    if request.method == 'POST':
        # Handling creating or updating terms sections
        title = request.POST.get('title')
        content = request.POST.get('content')  # Quill editor content is captured here
        order = request.POST.get('order')
        is_enabled = request.POST.get('is_enabled') == 'on'

        section_id = request.POST.get('section_id')
        if section_id:
            # If section ID exists, update the section
            section = get_object_or_404(TermsAndConditionsSection, id=section_id)
            section.title = title
            section.content = content
            section.order = order
            section.is_enabled = is_enabled
            section.save()
        else:
            # Create new section
            TermsAndConditionsSection.objects.create(
                title=title, content=content, order=order, is_enabled=is_enabled
            )

        return redirect('terms')  # Adjust URL as necessary

    # Render the template with context data
    return render(request, 'dashboard/terms.html', {
        'sections': sections,
        'section_to_edit': section_to_edit,
        'page': 'Manage Terms and Conditions'
    })

# View for managing Privacy Policy
@login_required(login_url='login')
def privacy_policy_view(request):
    # Handle GET request to display sections and the form
    sections = PrivacyPolicySection.objects.all().order_by('order')

    # Check if there's an 'edit' parameter in the URL for editing a specific section
    section_to_edit = None
    edit_section_id = request.GET.get('edit')
    if edit_section_id:
        section_to_edit = get_object_or_404(PrivacyPolicySection, id=edit_section_id)

    if request.method == 'POST':
        # Handling creating or updating privacy policy sections
        title = request.POST.get('title')
        content = request.POST.get('content')  # Quill editor content is captured here
        order = request.POST.get('order')
        is_enabled = request.POST.get('is_enabled') == 'on'

        section_id = request.POST.get('section_id')
        if section_id:
            # If section ID exists, update the section
            section = get_object_or_404(PrivacyPolicySection, id=section_id)
            section.title = title
            section.content = content
            section.order = order
            section.is_enabled = is_enabled
            section.save()
        else:
            # Create new section
            PrivacyPolicySection.objects.create(
                title=title, content=content, order=order, is_enabled=is_enabled
            )

        return redirect('manage_privacy_policy')

    # Render the template with context data
    return render(request, 'dashboard/manage_privacy_policy.html', {
        'sections': sections,
        'section_to_edit': section_to_edit,
        'page': 'Manage Privacy Policy'
    })

# View for managing FAQ
@login_required(login_url='login')
def faq_view(request):
    # Handle GET request to display sections and the form
    sections = FAQSection.objects.all().order_by('order')

    # Check if there's an 'edit' parameter in the URL for editing a specific section
    section_to_edit = None
    edit_section_id = request.GET.get('edit')
    if edit_section_id:
        section_to_edit = get_object_or_404(FAQSection, id=edit_section_id)

    if request.method == 'POST':
        # Handling creating or updating FAQ entries
        question = request.POST.get('question')
        answer = request.POST.get('answer')  # Quill editor content is captured here
        order = request.POST.get('order')
        is_enabled = request.POST.get('is_enabled') == 'on'

        faq_id = request.POST.get('faq_id')
        if faq_id:
            # If FAQ ID exists, update the FAQ entry
            faq = get_object_or_404(FAQSection, id=faq_id)
            faq.question = question
            faq.answer = answer
            faq.order = order
            faq.is_enabled = is_enabled
            faq.save()
        else:
            # Create new FAQ entry
            FAQSection.objects.create(
                question=question, answer=answer, order=order, is_enabled=is_enabled
            )

        return redirect('manage_faq')

    # Render the template with context data
    return render(request, 'dashboard/manage_faq.html', {
        'sections': sections,
        'section_to_edit': section_to_edit,
        'page': 'Manage FAQs'
    })

from django.apps import apps
def delete_section(request, model_name, section_id):
    # Dictionary to map model names to their respective redirect URLs
    redirect_map = {
        'TermsAndConditionsSection': 'terms',
        'PrivacyPolicySection': 'privacy_policy',
        'FAQSection': 'faq',
    }

    try:
        # Dynamically get the model class from 'main_app' based on model_name
        model = apps.get_model('main_app', model_name)
    except LookupError:
        # Handle the case where the model name is not found
        return redirect('terms')  # Redirect to 'terms' by default if model is invalid

    # Fetch the section and delete it
    section = get_object_or_404(model, id=section_id)
    section.delete()

    # Get the appropriate redirect URL from the redirect_map, default to 'terms'
    redirect_url = redirect_map.get(model_name, 'terms')

    # Redirect to the specific page (terms, privacy_policy, or faq) after deletion
    return redirect(redirect_url)


def delete_faq(request, id):
    section = get_object_or_404(FAQSection, id=id)
    section.delete()
    return redirect('manage_faq')

def delete_privacy(request, id):
    section = get_object_or_404(PrivacyPolicySection, id=id)
    section.delete()
    return redirect('manage_privacy_policy')



from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_custom_email(request):
    if request.method == "POST":
        recipient_emails = request.POST.get('recipient_email')
        subject = request.POST.get('subject')
        custom_message = request.POST.get('message')
        recipient_names = request.POST.get('names')

        # Split the recipient emails by commas to send to multiple addresses
        recipient_list = [email.strip() for email in recipient_emails.split(',')]
        name_list = [name.strip() for name in recipient_names.split(',')]

        # Ensure that the number of names matches the number of emails
        if len(name_list) != len(recipient_list):
            # Handle error: names and emails don't match in number
            return render(request, 'dashboard/send_email.html', {'error': 'Number of names and emails do not match'})

        # Save the email data to the CustomEmail model
        custom_email = CustomEmail(
            recipient_email=recipient_emails,
            name=recipient_names,
            subject=subject,
            message=custom_message,
            created_at=timezone.now(),
        )
        custom_email.save()

        # Send emails individually to each recipient
        for name, email in zip(name_list, recipient_list):
            # Render the email template with the dynamic data
            email_html_message = render_to_string('email_templates/custom_email_template.html', {
                'name': name,
                'custom_message': custom_message,
            })

            # Send the email
            send_mail(
                subject,
                '',  # Plain text version (optional)
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=email_html_message,
            )

        return redirect('send_email')  # Redirect to a success page after sending the email

    return render(request, 'dashboard/send_email.html')


def email_list(request):
    # Retrieve all emails from the database
    emails = CustomEmail.objects.all().order_by('-created_at')
    return render(request, 'dashboard/email_list.html', {'emails': emails})

def view_email(request):
    # Get the email ID from the query parameters (e.g., /view-email?id=<id>)
    email_id = request.GET.get('id')
    
    # Get the specific email entry or 404 if not found
    email_entry = get_object_or_404(CustomEmail, id=email_id)
    
    return render(request, 'dashboard/view_email.html', {'email': email_entry})

