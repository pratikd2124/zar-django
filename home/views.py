from django.shortcuts import render, redirect, get_object_or_404
from main_app.models import Community, User, SupportTickets,ProfileGallery,ConnectImpress,ProfileInfo
from .models import Category,PagesData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from main_app.funtions import Send_Code_email, Send_Welcome_email, Send_Payment_email
from django.db.models import Count

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
        
    
    print(member_type)
        
    return render(request,'dashboard/all-users.html',{'title':'User List','users':users,'member_type':member_type})




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
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    providers = User.objects.order_by('-id').filter(type='Service Provider')[:2]
    categories = Category.objects.order_by('-id').all()
    
    
        
    return render(request,'dashboard/service-provider.html',{'title':'Service Provider','providers':providers,'categories':categories})









@login_required(login_url='login')
def all_category(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
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
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    brands = User.objects.order_by('-id').filter(type='Material Provider')
    categories = Category.objects.order_by('-id').all()
    
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


@login_required(login_url='login')
def send_passcode(request):
    if not  request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    if request.method =='POST':
        uid =request.POST.get('user_id')
        profile_id = request.POST.get('profile_id')
        user = User.objects.get(uid=uid)
        profile = ProfileInfo.objects.get(id=profile_id)
        if request.GET.get('type')=='send_code':
            Send_Code_email(user.code,user.email)
            
            profile.payment_status = 'Code Sent'
            user.save()
            return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
        
        payment_link = request.POST.get('link')
        if request.GET.get('type')=='send_payment_link':
            Send_Payment_email(payment_link,user.email)
            
        user.code = user.generate_unique_code()
        profile.payment_status = 'In Progress'
        user.save()
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
    
    if request.GET.get('type') == 'delete':
        brand.delete()
        messages.success(request, 'Brand deleted successfully.')
        return redirect('brand_list')
    
    
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        contact_person_name = request.POST.get('contact_person_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        firm_address = request.POST.get('firm_address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        categories = request.POST.get('selected_categories')
        bio = request.POST.get('bio')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        linkedin = request.POST.get('linkedin')
        
        profilepic = request.FILES.get('profilepic')
        brandlogo = request.FILES.get('brandlogo')
        profileDoc = request.FILES.get('profileDocInput')

        brand.brand_name = brand_name
        brand.contact_person = contact_person_name
        brand.mobile = mobile
        brand.email = email
        brand.designation = designation
        brand.firm_address = firm_address
        brand.country =country
        brand.state = state
        brand.city = city
        brand.zip_code = pincode
        
        if categories:
            
            brand.category.clear()
            for category in categories.split(','):
                brand.category.add( Category.objects.get(id=category))
        brand.bio = bio
        brand.social_links = {
            'facebook': facebook,
            'instagram': instagram,
            'linkedin': linkedin
        }
        if profilepic:
            brand.profile_pic = profilepic
        
        if brandlogo:
            brand.brand_logo = brandlogo
        
        if profileDoc:
            brand.profile_doc = profileDoc
        
        brand.save()
        messages.success(request, 'Brand updated successfully.')
        return redirect('brand_list')
        
        
        
        
        
        

    
    
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
                    user.verified = True
                else:
                    user.verified = False
                
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
        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.email = email
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