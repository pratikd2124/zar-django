# main_app/views.py
from django.shortcuts import render, redirect
from home.models import Category,PagesData
from .models import User,Community,ProfileGallery, SupportTickets
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from .forms import HomeOwnerForm, ServiceProviderForm, MaterialProviderForm

def home(request):
    category = Category.objects.filter(parent=None)
    return render(request, 'client/index.html',{'title':'Home','category':category})  

def get_nav_list(nav):
    nav_list = []
    for i in  nav:
        try:
            category = Category.objects.get(name=i.strip(' '))
        except:
            category = Category.objects.get(name=i.strip(' '),parent__name=nav[nav.index(i)-1].strip(' '))
        nav_list.append({'get_category_hierarchy':category.get_category_hierarchy(),'id':category.id,'name':category.name})
        
    return nav_list

@login_required(login_url='login')
def category_view(request,category_path):
    id = request.GET.get('id')
    
    category = Category.objects.get(id=id)
        
    next_categories = Category.objects.filter(parent=category)
    
    nav = category.get_category_hierarchy().split('/')
    nav_list = get_nav_list(nav)
    
    users = None
    if not next_categories:
        # users = User.objects.filter(category=category).filter(payment_status='Success')
        users = User.objects.filter(category=category)
        
        
    return render(request, 'client/category.html', {'users':users,'category': category, 'nav_list':nav_list ,'title':category.name,'next_categories':next_categories})


def validate(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logined in.')
        return redirect('home')
    if request.method == 'POST':
        otp0 = request.POST.get('otp0')
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp5 = request.POST.get('otp5')
        otp = otp0 + otp1 + otp2 + otp3 + otp4 + otp5
        email = request.POST.get('email')
        print(otp,email)
        if User.objects.filter(email=request.POST.get('email')).exists():
            user = User.objects.get(email=email)
        
        
        
            if str(user.code) == str(otp):
                user.is_active = True
                user.save()
                request.session['email'] = user.email
                request.session['type'] = 'Existing'
                return redirect('register')
            else:
                return redirect('validate')
        else:
            if Community.objects.filter(code=otp).exists():
                
                community = Community.objects.get(code =otp)
                user = User.objects.create(email=email,community=community,username=email)
                user.save()
                request.session['email'] = email 
                request.session['type'] = 'New'   
            return redirect('register')
    return render(request,'client/validate.html')

def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logined in.')
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.get(email=email)
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.mobile = mobile
            user.is_active = True
            user.payment_status = 'Success'
            user.set_password(password)
            if request.session['type'] == 'New':
                user.type = 'Community User'
            user.save()
            return redirect('login')
        else:
            return redirect('register')
    try:
        print(request.session['email'],"!!!!!")
        user = User.objects.get(email=request.session['email'])
    except Exception as e:
        print(e)
        user = None
    return render(request,'client/register.html',{'user':user})


def signout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logined in.')
        return redirect('home')
    
    logout(request)
    return redirect('login')

def signin(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logined in.')
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, username=email, password=password)
        print(user,"!!!")
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                messages.success(request, 'Login successful')
                return redirect('dashboard')
            else:
            
            
                messages.success(request, 'Login successful')
                return redirect('splash')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request,'client/login.html')




def profile(request):
    return render(request, 'client/home-owner-profile.html')










def splash(request):
    return render(request,'client/splash.html')



def become_a_member(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logined in.')
        return redirect('home')
    return render(request, 'client/become-a-member.html')


from .funtions import *

def home_owner_view(request):
    
    if request.method == 'POST':
        # Manually fetching form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        interest = request.POST.get('interest')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create(email=email, mobile=mobile, type='Home Owner')
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.intrest = interest
            user.save()
            messages.info(request, 'Profile is Under Review !')
            Send_Welcome_email(user)
            return redirect('holme')
        

        # Redirect to a success page or wherever after submission
        return redirect('home')
    
    return render(request, 'client/home-owner.html')


def get_root_category(category):
    """Helper function to recursively find the root category."""
    while category.parent:
        category = category.parent
    return category

def get_category_hierarchy(categories, parent_id=None, level=0):
    hierarchy = []
    for category in categories:
        if category['parent_id'] == parent_id:
            # Indent children categories based on level
            hierarchy.append({
                'id': category['id'],
                'name': ('- ' * level) + category['name']
            })
            # Recursively add children
            hierarchy.extend(get_category_hierarchy(categories, category['id'], level + 1))
    return hierarchy

def submit_service_provider(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        firm_name = request.POST.get('firmName')
        firm_address = request.POST.get('firmAddress')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        category = request.POST.get('category')
        bio = request.POST.get('bio')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        linkedin = request.POST.get('linkedin')
        
        profilepic = request.FILES.get('profilepic')
        brandlogo = request.FILES.get('brandlogo')
        profileDoc = request.FILES.get('profileDocInput')

        gallery_images = request.FILES.getlist('gallery_images')

        print(profilepic,brandlogo,profileDoc,gallery_images)
        
        
        user = User.objects.create(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    mobile=mobile,
                    firm_name=firm_name,
                    firm_address=firm_address,
                    country=country,
                    state=state,
                    city=city,
                    zip_code=pincode,
                    bio=bio
                )
        user.type = 'Service Provider'
        if profilepic:
            user.profile_pic = profilepic
        if brandlogo:
            user.brand_logo = brandlogo
        if profileDoc:
            user.profile_doc = profileDoc
        if facebook or instagram or linkedin:
            user.social_links = {
                'facebook': facebook,
                'instagram': instagram,
                'linkedin': linkedin
            }
        user.category = Category.objects.get(id=category)
        user.save()
        for i in gallery_images:
            image= ProfileGallery.objects.create( image=i)
            image.save()

            user.profile_gallery.add(image)
            user.save()
        
        Send_Welcome_email(user)
        messages.success(request, 'Profile is Under Review !')
        return redirect('home')
            
    

    # Get all categories and recursively filter those whose root ancestor is 'Services'
    services_root = Category.objects.get(name__icontains='services')

    # Get all categories and recursively filter those whose root ancestor is 'Services'
    all_categories = Category.objects.all()

    categories = []
    for category in all_categories:
        if get_root_category(category) == services_root:
            categories.append({
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent_id
            })

    # Build the tree hierarchy for the filtered categories
    category_hierarchy = get_category_hierarchy(categories)
    
    return render(request, 'client/service-provider.html',{'categories':category_hierarchy} )

def submit_material_provider(request):
  
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        contact_person_name = request.POST.get('contact_person_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        firm_address = request.POST.get('firmAddress')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        category = request.POST.get('category')
        bio = request.POST.get('bio')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        linkedin = request.POST.get('linkedin')
        
        profilepic = request.FILES.get('profilepic')
        brandlogo = request.FILES.get('brandlogo')
        profileDoc = request.FILES.get('profileDocInput')

        gallery_images = request.FILES.getlist('gallery_images')

        print(profilepic,brandlogo,profileDoc,gallery_images)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('submit_material_provider')
        
        
        user = User.objects.create(
                    username=email,
                    email=email,
                    brand_name=brand_name,
                    contact_person=contact_person_name,
                    mobile=mobile,
                    designation=designation,
                    firm_address=firm_address,
                    country=country,
                    state=state,
                    city=city,
                    zip_code=pincode,
                    bio=bio
                )
        user.type = 'Material Provider'
        # if profilepic:
        #     user.profile_pic = profilepic
        # if brandlogo:
        #     user.brand_logo = brandlogo
        # if profileDoc:
        #     user.profile_doc = profileDoc
        if facebook or instagram or linkedin:
            user.social_links = {
                'facebook': facebook,
                'instagram': instagram,
                'linkedin': linkedin
            }
        user.category = Category.objects.get(id=category)
        user.save()
        # for i in gallery_images:
        #     image= ProfileGallery.objects.create( image=i)
        #     image.save()
        #     user.profile_gallery.add(image)
        #     user.save()
        
        Send_Welcome_email(user)
        messages.success(request, 'Profile is Under Review !')
        return redirect('home')
    # Get all categories and recursively filter those whose root ancestor is 'Services'
    services_root = Category.objects.get(name__icontains='material')

    # Get all categories and recursively filter those whose root ancestor is 'Services'
    all_categories = Category.objects.all()

    categories = []
    for category in all_categories:
        if get_root_category(category) == services_root:
            categories.append({
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent_id
            })

    # Build the tree hierarchy for the filtered categories
    category_hierarchy = get_category_hierarchy(categories)
    return render(request, 'client/material_provider_form.html',{'categories':category_hierarchy,'title':'Material Provider'} )







def success_page(request):
    return render(request, 'client/success_page.html')


@login_required(login_url='login')
def brand_info(request,category_path,uid):
    user = User.objects.get(uid = uid)
    social_links= user.social_links
    images = user.profile_gallery.all()
    nav_list = user.category.get_category_hierarchy().split('/')
    nav_list = get_nav_list(nav_list)

    return render(request, 'client/brand_info.html',{'nav_list':nav_list,'images':images,'user':user,'title':str(user.brand_name ),'social_links':social_links,})


@login_required(login_url='login')
def user_info(request,category_path,uid):
    user = User.objects.get(uid=uid)
    social_links = user.social_links
    print(social_links)
    images = user.profile_gallery.all()
    nav_list = user.category.get_category_hierarchy().split('/')
    nav_list = get_nav_list(nav_list)

    return render(request, 'client/service_user_info.html',{'user':user,'title':str(user.first_name + ' ' + user.last_name),'social_links':social_links,'images':images,'nav_list':nav_list})



from django.http import JsonResponse


def suggestions(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Fetch categories matching the query
        categories = [
                    {'name':category.name,'hierarchy': category.get_category_hierarchy(), 'id': category.id}
                    for category in Category.objects.filter(name__icontains=query)
                ]
        # Fetch brands matching the query
        brands =[{'name':brand.brand_name,'id':brand.uid,'category':brand.category.name} for brand in User.objects.filter(type="Material Provider").filter(
            Q(brand_name__icontains=query) | 
            Q(bio__icontains=query) | 
            Q(contact_person__icontains=query)
        )]

        # Fetch services matching the query
        services = [{'name':service.brand_name,'id':service.uid,'category':service.category.name} for service in User.objects.filter(type="Service Provider").filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(firm_name__icontains=query) | 
            Q(bio__icontains=query)
        )]

        # Prepare the response data
        data = {
            'categories': categories,
            'brands': brands,
            'serviceProviders': services
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request'}, status=400)




def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = SupportTickets.objects.create(phone=phone,name=name,email=email,subject=subject,message=message)
        contact.save()
        messages.success(request, 'Message Sent Successfully !')
        return redirect('home')
    return render(request, 'client/contact-us.html')

def privacy_policy(request):
    content = PagesData.objects.first().privacy_policy
    return render(request, 'client/custom-pages.html',{'title':'Privacy Policy','content':content})

def terms_and_conditions(request):
    content = PagesData.objects.first().terms_and_conditions
    return render(request, 'client/custom-pages.html',{'title':'Terms and Conditions','content':content})

def faq(request):
    content = PagesData.objects.first().faq
    return render(request, 'client/custom-pages.html',{'title':'FAQ','content':content})