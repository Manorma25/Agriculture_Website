from django.shortcuts import render, redirect
from AgroTech.models import*
import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import itertools
import statsmodels.api as sm
from django.contrib.auth import login as auth_login, logout as auth_logout
from social_django.models import UserSocialAuth

def signup(request):
    if request.method=="POST":
        nm=request.POST.get('r_name')
        em=request.POST.get('r_email')
        pw=request.POST.get('r_password')
        c_pw=request.POST.get('r_cpassword')
        if pw==c_pw:
            if user_register.objects.filter(email=em).exists():
                return render(request,'signup.html',{'err':"Email id already exists"})
            else:
                otp=random.randrange(100000,999999)
                subject="OTP"
                message="Welcome! Your otp is : "+str(otp)
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[em]
                send_mail(subject,message,email_from,recipient_list)
                msg="Your otp has been sent to your respective email account"
                return render(request,'otp.html',{'msg':msg,'name':nm,'email':em,'password':pw,'org_otp':otp})
        else:
            return render(request,'signup.html',{'err':"Password and Confirm Password does not match"})    
    else:
        return render(request,'signup.html')
    
def otp(request):
    if request.method=="POST":
        n=request.POST.get('r_name')
        e=request.POST.get('r_email')
        p=request.POST.get('r_password')
        org=request.POST.get('org_otp')
        enter=request.POST.get('enter_otp')

        if org==enter:
            x=user_register()
            x.name=n
            x.email=e
            x.password=p
            x.save()
            return redirect("/ThankYou")
        
        else:
            return render(request,'otp.html',{'name':n,'email':e,'password':p,'org_opt':org,'err':"OTP doesn't match"}) 

    else :
        return render(request,'otp.html')       

def signin(request):
    if request.method=="POST":
        e=request.POST.get('l_email')
        p=request.POST.get('l_password')
        user=user_register.objects.filter(email=e, password=p)
        if len(user)>0:
            request.session['em']=e
            return redirect("/dash")
        else:
            return render(request,'login.html',{'msg':"User does not exist"})
    else:
      return render(request,'login.html')
    

def signin_google(request):
    if request.method == "POST":
        e = request.POST.get('l_email')
        p = request.POST.get('l_password')

        # Check if the user exists in the database
        try:
            user = user_register.objects.get(email=e)
            if user.password == p:
                # Set session key if the credentials match
                request.session['em'] = e
                return redirect("/dash")  # Redirect to dashboard
            else:
                return render(request, 'google_login.html', {'msg': "Incorrect password"})
        except user_register.DoesNotExist:
            return render(request, 'google_login.html', {'msg': "User does not exist"})
    else:
        return render(request, 'google_login.html')

def google_login(request):
    return redirect('social:begin', backend='google-oauth2')   

def logout(request):
    auth_logout(request)
    return redirect('Home')

def index(request):
    x=Blog.objects.all()
    return render(request,'index.html',{'data':x}) 

def base(request):
    return render(request,'base.html')

def contact(request):
    if request.method=="POST":
        print("enter if")
        x=contact_model()
        x.name=request.POST.get('c_name')
        x.phone=request.POST.get('c_number')
        x.email=request.POST.get('c_email')
        x.subject=request.POST.get('c_subject')
        x.message=request.POST.get('c_message')
        x.save()
        return render(request,'thanku.html')
    
    else:
        print("else section")
        return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def news(request):
    return render(request,'news.html')

def faq(request):
    return render(request,'faq.html')

def forgot(request):
    if(request.method=='POST'):
        e=request.POST.get('f_email')
        user=user_register.objects.filter(email=e)
        if(len(user)>0):
            pw=user[0].password
            subject="Password"
            message="Welcome! Your password is : "+str(pw)
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[e]
            send_mail(subject,message,email_from,recipient_list)
            res="Your password has been sent to your respective email account"
            return render(request,'forgot_password.html',{'msg':res})
        else:
            rest="This Email Id is not registered"
            return render(request,'forgot_password.html',{'err':rest})
    else:
       return render(request,'forgot_password.html')

def cont(request):
    return render(request,'cont.html')

def thanku(request):
    return render(request,'thanku.html')

def thanku_reg(request):
    return render(request,'thanku_reg.html')

# def sidebar(request):
#     if not request.session.has_key('em'):
#         return redirect('/Signin') 
#     user=user_register.objects.get(email=request.session['em'])
#     return render (request,'sidebar.html',{'user':user})

from django.shortcuts import render, redirect, get_object_or_404
from social_django.models import UserSocialAuth


def side(request):
    return render(request,'side.html')
        
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .models import user_register  # Import your model

from django.shortcuts import get_object_or_404

"""For simple user and edit"""

# def user_profile(request):
#     if not request.session.has_key('em'):
#         return redirect('Signin')  # Redirect to login if not authenticated
#     user=user_register.objects.get(email=request.session['em'])
#     return render(request,'user_profile.html',{'user':user})

# def edit_profile(request):
#    if not request.session.has_key('em'):
#         return redirect('Signin')  # Redirect to login if not authenticated
#    user=user_register.objects.get(email=request.session['em'])
#    if request.method=="POST":
#         user.name=request.POST.get('name')
#         user.dob=request.POST.get('date')
#         user.phone=request.POST.get('phone')
#         user.pincode=request.POST.get('pincode')
#         user.address=request.POST.get('address')
#         user.gender=request.POST.get('gender')
#         user.country=request.POST.get('country')
#         if 'profile' in request.FILES:
#             user.profileimg=request.FILES['profile']
#         user.save()
#         return redirect('/User Profile')

#    return render(request, 'edit_profile.html',{'user':user})

# def changePassword(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('Signin_g')  # Redirect to login if not authenticated

#     # Check if the user logged in via Google
#     if UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').exists():
#         # Redirect or show a message for Google-authenticated users
#         return render(request, 'error.html', {'message': 'Password change is not available for Google login users.'})

#     # Proceed with password change for non-Google users
#     if request.method=='POST':
#         re=user_register.objects.get(email=request.session['em'])
#         op=request.POST.get('o_password')
#         np=request.POST.get('n_password')
#         cp=request.POST.get('c_password')
        
#         if(np==cp):
#             pa=re.password
#             if(op==pa):
#                 re.password=np
#                 re.save()
#                 res="Password Changed"
#                 return render(request,'change_password.html',{'msg':res})
#             else:
#                 res="Invalid current Password"
#                 return render(request,'change_password.html',{'err':res})
#         else:
#             res="Confirm password and new password don't match" 
#             return render(request,'change_password.html',{'err':res})

#     else:
#         return render(request,'change_password.html') 

def changePassword(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated and 'em' not in request.session:
        return redirect('Signin_g')  # Redirect to the login page

    # Check if the user logged in via Google
    if request.user.is_authenticated:
        if UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').exists():
            return render(request, 'error.html', {'message': 'Password change is not available for Google login users.'})

    if request.method == 'POST':
        try:
            # Get user based on session email
            email = request.session.get('em') if 'em' in request.session else request.user.email
            re = user_register.objects.get(email=email)

            op = request.POST.get('o_password')
            np = request.POST.get('n_password')
            cp = request.POST.get('c_password')

            if np == cp:
                if op == re.password:
                    re.password = np
                    re.save()
                    res = "Password Changed"
                    return render(request, 'change_password.html', {'msg': res})
                else:
                    res = "Invalid current Password"
                    return render(request, 'change_password.html', {'err': res})
            else:
                res = "Confirm password and new password don't match"
                return render(request, 'change_password.html', {'err': res})
        except user_register.DoesNotExist:
            return redirect('Signin_g')  # Redirect if the user is not found
    else:
        return render(request, 'change_password.html')

    
"""google related"""

"""User profile"""
def user_profile(request):
    if not (request.user.is_authenticated or request.session.has_key('em')):
        return redirect('Signin_g')

    user_data = None

    if request.user.is_authenticated:
        try:
            user_social = UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').first()
            
            if user_social:
                user, created = user_register.objects.get_or_create(
                    email=request.user.email,
                    defaults={'name': request.user.get_full_name() or request.user.username}
                )

                if created:
                    user.save()

                user_data = {
                    'username': user.name,
                    'email': user.email,
                    'phone':user.phone,
                    'pincode':user.pincode,
                    'address':user.address,
                    'gender':user.gender,
                    'country':user.country,
                     'dob':user.dob,
                     'profileimg':user.profileimg,
                }
            else:
                return redirect('Signin')
        except UserSocialAuth.DoesNotExist:
            return redirect('Signin_g')

    else:
        try:
            user = get_object_or_404(user_register, email=request.session['em'])
            user_data = {
                 'username': user.name,
                    'email': user.email,
                    'phone':user.phone,
                    'pincode':user.pincode,
                    'address':user.address,
                    'gender':user.gender,
                    'country':user.country,
                    'dob':user.dob,
                    'profileimg':user.profileimg,
            }
        except user_register.DoesNotExist:
            return redirect('Signup')

    return render(request, 'user_profile.html', {'user': user_data})

"""edit profile"""
def edit_profile(request):
    # Check if the user is authenticated either through Google or session
    if not (request.user.is_authenticated or request.session.has_key('em')):
        return redirect('Signin_g')  # Redirect to login if not authenticated
    
    # If the user is authenticated via Google, use request.user
    if request.user.is_authenticated:
        user = user_register.objects.get(email=request.user.email)
    else:
        # If the user is authenticated via session, use the email from the session
        user = user_register.objects.get(email=request.session['em'])

    # Handle profile update if the request method is POST
    if request.method=="POST":
        user.name=request.POST.get('name')
        user.dob=request.POST.get('date')
        user.phone=request.POST.get('phone')
        user.pincode=request.POST.get('pincode')
        user.address=request.POST.get('address')
        user.gender=request.POST.get('gender')
        user.country=request.POST.get('country')
        if 'profile' in request.FILES:
            user.profileimg=request.FILES['profile']
        user.save()
        return redirect('/User Profile')

    # Render the edit profile page with the user's current data
    return render(request, 'edit_profile.html',{'user':user})

"""dashboard"""

def dashboard(request):
    # Check if the user is authenticated via Google or if the session has the 'em' key
    if not (request.user.is_authenticated or request.session.get('em')):
        return redirect('Signin_g')

    user_data = None

    # Google OAuth authenticated user
    if request.user.is_authenticated:
        try:
            user_social = UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').first()
            if user_social:
                # Retrieve or create user data in user_register
                user, created = user_register.objects.get_or_create(
                    email=request.user.email,
                    defaults={'name': request.user.get_full_name() or request.user.username}  # Use default profile image if available
                )

                if created:
                    user.save()

                user_data = {
                    'name': user.name,
                    'email': user.email,
                    'profileimg': user.profileimg,
                }
            else:
                return redirect('Signin_g')
        except UserSocialAuth.DoesNotExist:
            return redirect('Signin_g')

    # Session-based authenticated user
    elif 'em' in request.session:
        email = request.session.get('em')
        try:
            user = get_object_or_404(user_register, email=email)
            user_data = {
                'name': user.name,
                'email': user.email,
                'profileimg': user.profileimg,
            }
        except user_register.DoesNotExist:
            return redirect('Signin_g')

    return render(request, "dashboard.html", {"user": user_data})

"""sidebar"""

def sidebar(request):
    user_data = None

    # Check Google OAuth authentication
    if request.user.is_authenticated:
        try:
            user_social = UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').first()
            if user_social:
                user, created = user_register.objects.get_or_create(
                    email=request.user.email,
                    defaults={'name': request.user.get_full_name() or request.user.username}
                )
                if created:
                    user.save()

                user_data = {
                    'name': user.name,
                    'email': user.email,
                    'profileimg': user.profileimg,
                }
            else:
                return redirect('Signin_g')
        except UserSocialAuth.DoesNotExist:
            return redirect('Signin_g')

    # Check session-based authentication
    elif request.session.get('em'):
        email = request.session.get('em')
        try:
            user = get_object_or_404(user_register, email=email)
            user_data = {
                'name': user.name,
                'email': user.email,
                'profileimg': user.profileimg,
            }
        except user_register.DoesNotExist:
            return redirect('Signin_g')

    if not user_data:
        return redirect('Signin_g')

    return render(request, 'sidebar.html', {'user': user_data})


"""change password"""  
# def changePassword(request):
#     if not (request.user.is_authenticated or request.session.has_key('em')):
#         return redirect('Signin')
#     if request.method=='POST':
#         re=user_register.objects.get(email=request.session['em'])
#         op=request.POST.get('o_password')
#         np=request.POST.get('n_password')
#         cp=request.POST.get('c_password')
        
#         if(np==cp):
#             pa=re.password
#             if(op==pa):
#                 re.password=np
#                 re.save()
#                 res="Password Changed"
#                 return render(request,'change_password.html',{'msg':res})
#             else:
#                 res="Invalid current Password"
#                 return render(request,'change_password.html',{'err':res})
#         else:
#             res="Confirm password and new password don't match" 
#             return render(request,'change_password.html',{'err':res})

#     else:
#         return render(request,'change_password.html')

# def dashboard(request):
#     if not request.session.has_key('em'):
#         return redirect('/Signin') 
#     user=user_register.objects.get(email=request.session['em'])
#     return render (request,"dashboard.html",{"user":user})


from django.shortcuts import redirect, render
from .models import user_register  # Adjust the import as needed

from django.shortcuts import redirect, render, get_object_or_404
from .models import user_register
from social_django.models import UserSocialAuth  # Import if using Google OAuth


def university(request):
    universities = indian_agriculture_university.objects.all()
    return render(request, 'university.html', {'data': universities})

def technologies(request):
    x=latest_technology.objects.all()
    return render(request,'technologies.html',{'data':x}) 

def schemes(request):
    x=farmers_scheme.objects.all()
    return render(request,'schemes.html',{'data':x}) 

from .models import Blog
def blog_view(request):
    x=Blog.objects.all()
    return render(request,'blogs.html',{'data':x}) 

def blog_detail(request,blog_id):
    x=get_object_or_404(Blog, id=blog_id)
    return render(request,'blog_detail.html',{'data':x})

def scheme_details(request, scheme_id):
    x = get_object_or_404(farmers_scheme, id=scheme_id)
    return render(request, 'schemes_details.html', {'scheme': x})

def call_center(request):
    return render(request,'call_center.html')

from django.shortcuts import render
from .models import AgricultureData, State

def state(request):
    states = State.objects.all()
    #return render(request, 'state_list.html', {'states': states})
    return render(request,'state.html', {'states': states})


# def state(request):
#     states = State.objects.all()
#     user_data = None
#     # Check Google OAuth authentication
#     if request.user.is_authenticated:
#         try:
#             user_social = UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').first()
#             if user_social:
#                 user, created = user_register.objects.get_or_create(
#                     email=request.user.email,
#                     defaults={'name': request.user.get_full_name() or request.user.username}
#                 )
#                 if created:
#                     user.save()

#                 user_data = {
#                     'name': user.name,
#                     'email': user.email,
#                     'profileimg': user.profileimg,
#                 }
#             else:
#                 return redirect('Signin')
#         except UserSocialAuth.DoesNotExist:
#             return redirect('Signin')

#     # Check session-based authentication
#     elif request.session.get('em'):
#         email = request.session.get('em')
#         try:
#             user = get_object_or_404(user_register, email=email)
#             user_data = {
#                 'name': user.name,
#                 'email': user.email,
#                 'profileimg': user.profileimg,
#             }
#         except user_register.DoesNotExist:
#             return redirect('Signin')

#     if not user_data:
#         return redirect('Signin')

#     return render(request, 'state.html', {'user': user_data,'states':states})

def month(request, state_id):
    # Get the selected state using the state_id
    selected_state = get_object_or_404(State, id=state_id)
    context = {
        'state_name': selected_state.name,  # Pass the state's name to the template
        'state_id': state_id,
        'months': [
            'January', 'February', 'March', 'April', 'May', 
            'June', 'July', 'August', 'September', 'October', 
            'November', 'December'
        ],
    }
    return render(request, 'month.html', context)

def crops(request, state_id, month):
    data = AgricultureData.objects.filter(state_id=state_id, month=month).first()
    context = {
        'state_name': data.state.name if data else '',
        'month': data.month if data else '',
        'crop_images': data.crop_images if data else '',
        'fruit_images':data.fruit_images if data else '',
        'vegetable_images':data.vegetable_images if data else '',
        'flower_images': data.flower_images if data else '',
        'crops': [crop.strip() for crop in data.crops.split(',')] if data and data.crops else [],
        'fruits': [fruit.strip() for fruit in data.fruits.split(',')] if data and data.fruits else [],
        'vegetables': [vegetable.strip() for vegetable in data.vegetables.split(',')] if data and data.vegetables else [],
        'flowers': [flower.strip() for flower in data.flowers.split(',')] if data and data.flowers else [],
        'error': None if data else 'No data available for this state and month.'
    }
    return render(request, 'crop.html', context)

def i(request):
    return render(request,'i.html')

def fertilizers(request):
    return render(request, 'fertilizers.html')

def fertilizer_ques(request):
    return render(request, 'fertilizers_questions.html')

def avg_nitrogen_by_decade_area_chart(request):
    if request.method=="POST":
        country_name=request.POST.get("country1")
        df=pd.read_csv("nitrogen.csv")
        df=df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare":"Nitrogen (kilograms per hectare)"})
        country_data = df[df['Entity'] == country_name]

        country_data['Decade'] = (country_data['Year'] // 10) * 10

        avg_nitrogen_decade = country_data.groupby('Decade')['Nitrogen (kilograms per hectare)'].mean().reset_index()

        fig = px.area(
            avg_nitrogen_decade,
            x='Decade',
            y='Nitrogen (kilograms per hectare)',
            title=f'<b>Average Nitrogen Usage by Decade in {country_name}</b>',
            labels={'Nitrogen (kilograms per hectare)': 'Avg Nitrogen (kg/hectare)', 'Decade': 'Decade'},
            template='plotly_white'
        )

        fig.update_layout(
            width=1200,
            height=600,
            title_x=0.5,
            xaxis_title='<b>Decade</b>',
            yaxis_title='<b>Avg Nitrogen (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            hovermode="x"
        )
        fig.update_traces(
            line=dict(color='#4baf47', width=2),
            fillcolor='rgba(75, 175, 71, 0.4)',
            mode='lines+markers',
            marker=dict(size=6, color='#eec044', line=dict(width=1, color='black'))
        )

        #fig.show()
        graph=fig.to_html()
        return render(request,'fertilizer_graph.html',{"graph":graph})

    else:
        df=pd.read_csv("nitrogen.csv")
        df=df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare":"Nitrogen (kilograms per hectare)"})
        result=df["Entity"].drop_duplicates().tolist()
        return render(request,'nitrogendecade.html',{"data":result})
    
def fert_graph(request):
    return render(request, 'fertilizer_graph.html')

def nitrogen_usage(request):
     if request.method=="POST":
        country_name=request.POST.get("country1")
        df=pd.read_csv("nitrogen.csv")
        df=df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare":"Nitrogen (kilograms per hectare)"})
        country_data = df[df['Entity'] == country_name]
        fig = px.line(
        country_data,
        x='Year',
        y='Nitrogen (kilograms per hectare)',
        title=f'<b>Nitrogen Usage in {country_name} Over Time</b>',
        labels={'Nitrogen (kilograms per hectare)': 'Nitrogen (kg/hectare)'},
        template='plotly_white',
    )
        fig.update_traces(
            line=dict(color='#4baf47', width=2),
            marker=dict(size=6, color='#eec044', line=dict(width=1, color='red'))
        )

        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Year</b>',
            yaxis_title='<b>Nitrogen (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            hovermode='x',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
        )

        graph=fig.to_html()
        return render(request,'fertilizer_graph.html',{"graph":graph})
     else:
        df=pd.read_csv("nitrogen.csv")
        df=df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare":"Nitrogen (kilograms per hectare)"})
        result=df["Entity"].drop_duplicates().tolist()
        return render(request,'nitrogen1.html',{"data":result})
     
def nitrogen_compare(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": "Nitrogen (kilograms per hectare)"})
    country_list = df['Entity'].drop_duplicates().tolist()

    if request.method == "POST":
        countries = request.POST.getlist('country1[]')  
        # if len(countries) < 2 or len(countries) > 10:
        #     error_message = "Please select 2 or more countries for comparison."
        #     return render(request, 'nitrogen2.html', {"error": error_message})

        country_data = df[df['Entity'].isin(countries)]

        fig = px.line(
            country_data,
            x='Year',
            y='Nitrogen (kilograms per hectare)',
            color='Entity',
            title=f'<b>Comparison of Nitrogen Usage Between {", ".join(countries)}</b>',
            labels={'Nitrogen (kilograms per hectare)': 'Nitrogen (kg/hectare)'},
            template='plotly_white'
        )

        fig.update_traces(
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=6)
        )

        # Update layout
        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Year</b>',
            yaxis_title='<b>Nitrogen (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
        )

        graph = fig.to_html()

        return render(request, 'fertilizer_graph.html', {"graph": graph})

    else:

        df = pd.read_csv("nitrogen.csv")
        df = df.rename(columns={"Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": "Nitrogen (kilograms per hectare)"})
        country_list = df['Entity'].drop_duplicates().tolist()
        return render(request, 'nitrogen2.html', {"countries": country_list})


def top_n_nitrogen_usage(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={
        "Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": 
        "Nitrogen (kilograms per hectare)"
    })

    years = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        year = int(request.POST.get('year'))
        n = int(request.POST.get('n'))
        year_data = df[df['Year'] == year]
        top_n = year_data.nlargest(n, 'Nitrogen (kilograms per hectare)')
        fig = px.bar(
            top_n,
            x='Entity',
            y='Nitrogen (kilograms per hectare)',
            title=f'<b>Nitrogen Usage of Top {n} cointries in {year}</b>',
            labels={'Nitrogen (kilograms per hectare)': 'Nitrogen (kg/hectare)'},
            template='plotly_white',
            text='Nitrogen (kilograms per hectare)',
            color='Nitrogen (kilograms per hectare)',
            color_continuous_scale=px.colors.sequential.Tealgrn
        )

        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Country</b>',
            yaxis_title='<b>Nitrogen (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            coloraxis_showscale=False
        )

        fig.update_traces(
            texttemplate='%{text:.2f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Nitrogen Usage: %{y:.2f} kg/hectare<extra></extra>'
        )
        graph = fig.to_html()

        return render(request, 'fertilizer_graph.html', {"graph": graph, "year": year, "n": n})

    else:
        return render(request, 'nitrogen3.html', {"years": years})
    

    
def country_production_growth_rate(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={
        "Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": 
        "Nitrogen (kilograms per hectare)"
    })

    years1 = df['Year'].drop_duplicates().sort_values().tolist()
    countries = df['Entity'].drop_duplicates().tolist()
    years2 = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":

        start_year = int(request.POST.get('year1'))
        end_year = int(request.POST.get('year2'))
        country = request.POST.get("country1")

        df_filtered = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]

        df_filtered['Growth Rate (%)'] = df_filtered["Nitrogen (kilograms per hectare)"].pct_change() * 100

        fig = px.line(df_filtered,
                      x="Year",
                      y="Growth Rate (%)",
                      title=f"Nitrogen Usage Growth Rate for {country} ({start_year}-{end_year})",
                      labels={"Growth Rate (%)": "Growth Rate (%)"},
                      markers=True,
                      color_discrete_sequence=["#1f77b4"])

        positive_growth = df_filtered[df_filtered['Growth Rate (%)'] > 0]
        fig.add_scatter(x=positive_growth["Year"], y=positive_growth["Growth Rate (%)"],
                    mode="markers",
                    marker=dict(size=8, color="#2ca02c"),
                    name="Positive Growth")

        negative_growth = df_filtered[df_filtered['Growth Rate (%)'] < 0]
        fig.add_scatter(x=negative_growth["Year"], y=negative_growth["Growth Rate (%)"],
                    mode="markers",
                    marker=dict(size=8, color="#d62728"),
                    name="Negative Growth")

        fig.add_hline(y=0, line_dash="dash", line_color="black")

        # Customize layout
        fig.update_layout(
            width=1200,
            height=600,
            title=dict(font_size=22, x=0.5),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="#f9f9f9",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#e5e5e5")
        )

        # Customize hover template
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")

        graph_html = fig.to_html()

        return render(request, 'fertilizer_graph.html', {"graph": graph_html})

    else:
        return render(request, 'nitrogen5.html', {"years1": years1, "countries": countries, "years2": years2})
    
def nitrogen_usage2(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={
        "Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": 
        "Nitrogen (kilograms per hectare)"
    })
    years = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        y = int(request.POST.get('year'))
        year_data = df[df['Year'] == y]
        fig = px.choropleth(year_data,
                            locations="Code",
                            color="Nitrogen (kilograms per hectare)",
                            hover_name="Entity",
                            color_continuous_scale="viridis",
                            title=f'Global Nitrogen Usage in {y}',
                            labels={'Nutrient nitrogen N (total)': 'Nitrogen (kg/hectare)'}
                        )
        fig.update_layout(
            width=1200,
            height=600
        )
        fig.update_geos(showcoastlines=True, coastlinecolor="black")
        graph= fig.to_html()
        
        return render(request, "fertilizer_graph.html",{"graph":graph})
    
    else:
        return render(request,"nitrogen6.html",{"years":years})
    
def avg_nitrogen_usage(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={
        "Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": 
        "Nitrogen (kilograms per hectare)"
    })
    years = df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get("year1"))
        end_year=int(request.POST.get("year2"))
        filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
        avg_usage = filtered_df.groupby('Entity')['Nitrogen (kilograms per hectare)'].mean().reset_index()
        top10 = avg_usage.nlargest(10, 'Nitrogen (kilograms per hectare)')
        fig = px.scatter(top10, x='Entity', y='Nitrogen (kilograms per hectare)',
                        title='Top 10 Countries by Average Nitrogen Usage',
                        color='Nitrogen (kilograms per hectare)',
                        size='Nitrogen (kilograms per hectare)',
                        color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_layout(
            width=1200,
            height=600
        )
        graph=fig.to_html()
        return render(request,"fertilizer_graph.html",{"graph":graph,"msg":"success"})
    else:
        return render(request,"nitrogen7.html",{"years":years})
    
def compare_nitrogen_usage(request):
    df = pd.read_csv("nitrogen.csv")
    df = df.rename(columns={
        "Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare": 
        "Nitrogen (kilograms per hectare)"
    })
    years = df['Year'].drop_duplicates().sort_values().tolist()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()

    if request.method=="POST":
        year=int(request.POST.get('year'))
        countries=request.POST.getlist('countries[]')
        year_data = df[(df['Year'] == year) & (df['Entity'].isin(countries))]
        fig = px.bar(year_data, x='Entity', y='Nitrogen (kilograms per hectare)',
                    title=f'Nitrogen Usage Comparison in {year}',
                    labels={'Nutrient nitrogen N (total)': 'Nitrogen Usage (kg/ha)'},
                    color='Nitrogen (kilograms per hectare)',
                    color_continuous_scale=px.colors.sequential.Tealgrn)
        
        fig.update_layout(
            width=1200,
            height=600
        )

        graph=fig.to_html()
        return render(request, 'fertilizer_graph.html',{"graph":graph})
    
    else:
        return render(request,"nitrogen8.html",{"years":years,"cont":cont})
    

def potassium_ques(request):
    return render(request, "potassium_ques.html")

def phosphorus_ques(request):
    return render(request, 'phosphorus_ques.html')

def main_crop(request):
    return render(request,"crops_prod.html")

def wheat_ques(request):
    return render(request,'wheat_ques.html')

def rice_ques(request):
    return render(request,"rice_ques.html")

def maize_ques(request):
    return render(request,"maize_ques.html")


def potassium_usage(request):
     if request.method=="POST":
        country_name=request.POST.get("country1")
        df=pd.read_csv("potassium.csv")
        df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
        country_data = df[df['Entity'] == country_name]
        fig = px.line(
        country_data,
        x='Year',
        y='Potassium (kilograms per hectare)',
        title=f'<b>Potassium Usage in {country_name} Over Time</b>',
        labels={'Potassium (kilograms per hectare)': 'Potassium (kg/hectare)'},
        template='plotly_white',
    )

    # Customize the line and markers
        fig.update_traces(
        line=dict(color='#4baf47', width=2),
        marker=dict(size=6, color='#eec044', line=dict(width=1, color='red'))
    )

    # Update layout
        fig.update_layout(
        title_x=0.5,
        xaxis_title='<b>Year</b>',
        yaxis_title='<b>Potassium (kg/hectare)</b>',
        font=dict(family="Arial", size=14, color="black"),
        hovermode='x',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        width=1200,
        height=600,
    )

        graph=fig.to_html()
        return render(request,'potash_graph.html',{"graph":graph})
     else:
        df=pd.read_csv("potassium.csv")
        df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
        result=df["Entity"].drop_duplicates().tolist()
        return render(request,'potash1.html',{"data":result})
     
def potash2(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})

    country_list = df['Entity'].drop_duplicates().tolist()
    if request.method == "POST":
        countries = request.POST.getlist('country1[]')  
        country_data = df[df['Entity'].isin(countries)]
        fig = px.line(
        country_data,
        x='Year',
        y='Potassium (kilograms per hectare)',
        color='Entity',
        title=f'<b>Comparison of Potassium Usage Between {" and ".join(countries)}</b>',
        labels={'Potassium (kilograms per hectare)': 'Potassium (kg/hectare)'},
        template='plotly_white'
    )

        fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

        fig.update_layout(
        title_x=0.5,
        xaxis_title='<b>Year</b>',
        yaxis_title='<b>Potassium (kg/hectare)</b>',
        font=dict(family="Arial", size=14, color="black"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        width=1200,
        height=600,
    )
        graph=fig.to_html()
        return render(request,"potash_graph.html",{"graph":graph})
    else:
        return render(request,"potash2.html",{"country_list":country_list})


def potash3(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        year = int(request.POST.get('year'))
        n = int(request.POST.get('n'))
        year_data = df[df['Year'] == year]

        top_n = year_data.nlargest(n, 'Potassium (kilograms per hectare)')
        fig = px.bar(
            top_n,
            x='Entity',
            y='Potassium (kilograms per hectare)',
            title=f'<b>Top {n} Countries by Potassium Usage in {year}</b>',
            labels={'Potassium (kilograms per hectare)': 'Potassium (kg/hectare)'},
            template='plotly_white',
            text='Potassium (kilograms per hectare)',
            color='Potassium (kilograms per hectare)',
            color_continuous_scale=px.colors.sequential.Tealgrn
        )

        # Update layout
        fig.update_layout(
            title_x=0.5,
            xaxis_title='<b>Country</b>',
            yaxis_title='<b>Potassium (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            coloraxis_showscale=False,
            width=1200,
            height=600,
        )

        fig.update_traces(
            texttemplate='%{text:.2f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Potassium Usage: %{y:.2f} kg/hectare<extra></extra>'
        )
        graph=fig.to_html()
        return render(request, 'potash_graph.html', {"graph": graph, "year": year, "n": n})

    else:
        return render(request, 'potash3.html', {"years": years})


def potash4(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    result=df["Entity"].drop_duplicates().tolist()
    if request.method=="POST":
        country_name=request.POST.get("country1")
        country_data = df[df['Entity'] == country_name]

        country_data['Decade'] = (country_data['Year'] // 10) * 10
  
        avg_potash_decade = country_data.groupby('Decade')['Potassium (kilograms per hectare)'].mean().reset_index()

        fig = px.area(
        avg_potash_decade,
        x='Decade',
        y='Potassium (kilograms per hectare)',
        title=f'<b>Average Potassium Usage by Decade in {country_name}</b>',
        labels={'Potassium (kilograms per hectare)': 'Avg Potassium (kg/hectare)', 'Decade': 'Decade'},
        template='plotly_white'
    )

        fig.update_layout(
        title_x=0.5,
        xaxis_title='<b>Decade</b>',
        yaxis_title='<b>Avg Potassium (kg/hectare)</b>',
        font=dict(family="Arial", size=14, color="black"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        hovermode="x",
        width=1200,
        height=600,
    )
        fig.update_traces(
        line=dict(color='#4baf47', width=2),
        fillcolor='rgba(75, 175, 71, 0.4)',
        mode='lines+markers',
        marker=dict(size=6, color='#eec044', line=dict(width=1, color='black'))
    )


        #fig.show()
        graph=fig.to_html()
        return render(request,'potash_graph.html',{"graph":graph})

    else:
        return render(request, 'potash4.html', {"result": result})

def potash5(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    years1 = df['Year'].drop_duplicates().sort_values().tolist()
    countries = df['Entity'].drop_duplicates().tolist()
    years2 = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":

        start_year = int(request.POST.get('year1'))
        end_year = int(request.POST.get('year2'))
        country = request.POST.get("country1")
        df1 = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]

        df1['Growth Rate (%)'] = df1["Potassium (kilograms per hectare)"].pct_change() * 100

        # Create a smoothed line plot for growth rate with markers
        fig = px.line(df1,
                        x="Year",
                        y="Growth Rate (%)",
                        title=f"Potassium Usage Growth Rate for {country} ({start_year}-{end_year})",
                        labels={"Growth Rate (%)": "Growth Rate (%)"},
                        markers=True,
                        color_discrete_sequence=["#1f77b4"])  # Custom color

        # Highlight years where the growth rate is positive or negative
        fig.add_scatter(x=df1["Year"], y=df1["Growth Rate (%)"],
                        mode="markers",
                        marker=dict(size=8, color=["#2ca02c" if x > 0 else "#d62728" for x in df1["Growth Rate (%)"]]),
                        name="Positive/Negative Growth")

        # Add horizontal reference line at 0% growth rate
        fig.add_hline(y=0, line_dash="dash", line_color="black")

        # Customize layout
        fig.update_layout(
            title=dict(font_size=22, x=0.5),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",  # A clean template for better contrast
            hovermode="x unified",    # Show a unified hover label
            plot_bgcolor="#f9f9f9",   # Light background
            xaxis=dict(showgrid=False),  # Remove vertical gridlines
            yaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
            width=1200,
            height=600 ,
        )

        # Customize hover labels
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")
        graph=fig.to_html()
        return render(request,'potash_graph.html',{"graph":graph})

    else:
        return render(request, 'potash5.html', {"years1":years1,"countries":countries,"years2":years2})



def potash6(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        year = int(request.POST.get('year'))
        year_data = df[df['Year'] == year]
        fig = px.choropleth(year_data,
                            locations="Code",
                            color="Potassium (kilograms per hectare)",
                            hover_name="Entity",
                            color_continuous_scale="viridis",
                            title=f'Global Potassium Usage in {year}',
                            labels={'Nutrient Potassium N (total)': 'Potassium (kg/hectare)'}
                        )
        fig.update_geos(showcoastlines=True, coastlinecolor="black", projection_type="natural earth")
        fig.update_layout(
            width=1200,
            height=600,
        )
        graph=fig.to_html()
        return render(request,"potash_graph.html",{"graph":graph})
    else:
      return render(request,"potash6.html",{"years":years})

def potash7(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get("year1"))
        end_year=int(request.POST.get("year2"))
        filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
        avg_usage = filtered_df.groupby('Entity')['Potassium (kilograms per hectare)'].mean().reset_index()
        top10 = avg_usage.nlargest(10, 'Potassium (kilograms per hectare)')
        fig = px.scatter(top10, x='Entity', y='Potassium (kilograms per hectare)',
                        title='Top 10 Countries by Average Potassium Usage',
                        color='Potassium (kilograms per hectare)',
                        size='Potassium (kilograms per hectare)',
                        color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_layou(
            width=1200,
            height=600
        )
        graph=fig.to_html()
        return render(request,"potash_graph.html",{"graph":graph})
    else:
        return render(request,"potash7.html",{"years":years})

def potash8(request):
    df=pd.read_csv("potassium.csv")
    df=df.rename(columns={"Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare":"Potassium (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()

    if request.method=="POST":
        year=int(request.POST.get('year'))
        countries=request.POST.getlist('countries[]')
        year_data = df[(df['Year'] == year) & (df['Entity'].isin(countries))]
        fig = px.bar(year_data, x='Entity', y='Potassium (kilograms per hectare)',
                 title=f'Potassium Usage Comparison in {year}',
                 labels={'Nutrient Potassium N (total)': 'Potassium Usage (kg/ha)'},
                 color='Potassium (kilograms per hectare)',
                color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_layout(
            width=1200,
            height=600
        )
        graph=fig.to_html()
        return render(request,"potash_graph.html",{"graph":graph})
    return render(request,"potash8.html",{"years":years,"cont":cont})


def phos1(request):
    if request.method=="POST":
        country_name=request.POST.get("country1")
        df=pd.read_csv("phosphorus.csv")
        df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
        country_data = df[df['Entity'] == country_name]
        fig = px.line(
            country_data,
            x='Year',
            y='Phosphate (kilograms per hectare)',
            title=f'<b>Phosphate Usage in {country_name} Over Time</b>',
            labels={'Phospahte (kilograms per hectare)': 'Potassium (kg/hectare)'},
            template='plotly_white',
        )

        # Customize the line and markers
        fig.update_traces(
            line=dict(color='#4baf47', width=2),
            marker=dict(size=6, color='#eec044', line=dict(width=1, color='red'))
        )

        # Update layout
        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Year</b>',
            yaxis_title='<b>Phospahte (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            hovermode='x',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
        )
        graph=fig.to_html()
        return render(request,'phos_graph.html',{"graph":graph})
    else:
      df=pd.read_csv("phosphorus.csv")
      df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
      result=df["Entity"].drop_duplicates().tolist()
      return render(request,'phos1.html',{"data":result})

def phos2(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    country_list = df['Entity'].drop_duplicates().tolist()
    if request.method == "POST":
        countries= request.POST.getlist('country1[]')  
        country_data = df[df['Entity'].isin(countries)]

        fig = px.line(
            country_data,
            x='Year',
            y='Phosphate (kilograms per hectare)',
            color='Entity',
            title=f'<b>Comparison of Phosphate Usage Between {" and ".join(countries)}</b>',
            labels={'Phosphate (kilograms per hectare)': 'Phosphate (kg/hectare)'},
            template='plotly_white'
        )

        fig.update_traces(
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=6)
        )

        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Year</b>',
            yaxis_title='<b>Phosphate (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
        )

        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph})
    else:
      return render(request, "phos2.html",{"country_list":country_list})

def phos3(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        year = int(request.POST.get('year'))
        n = int(request.POST.get('n'))
        year_data = df[df['Year'] == year]
        top_n = year_data.nlargest(n, 'Phosphate (kilograms per hectare)')
        fig = px.bar(
            top_n,
            x='Entity',
            y='Phosphate (kilograms per hectare)',
            title=f'<b>Top {n} Countries by Phosphate Usage in {year}</b>',
            labels={'Phosphate (kilograms per hectare)': 'Phosphate (kg/hectare)'},
            template='plotly_white',
            text='Phosphate (kilograms per hectare)',
            color='Phosphate (kilograms per hectare)',
            color_continuous_scale=px.colors.sequential.Tealgrn
        )

        # Update layout
        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Country</b>',
            yaxis_title='<b>Phosphate (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            coloraxis_showscale=False
        )

        fig.update_traces(
            texttemplate='%{text:.2f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Phosphate Usage: %{y:.2f} kg/hectare<extra></extra>'
        )

        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph})
    else:
      return render(request,"phos3.html",{"years":years})

def phos4(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    result=df["Entity"].drop_duplicates().tolist()
    if request.method=="POST":
        country_name=request.POST.get("country1")
        country_data = df[df['Entity'] == country_name]

        country_data['Decade'] = (country_data['Year'] // 10) * 10

        avg_potash_decade = country_data.groupby('Decade')['Phosphate (kilograms per hectare)'].mean().reset_index()

        fig = px.area(
            avg_potash_decade,
            x='Decade',
            y='Phosphate (kilograms per hectare)',
            title=f'<b>Average Phosphorus Usage by Decade in {country_name}</b>',
            labels={'Phosphorus (kilograms per hectare)': 'Avg Phosphorus (kg/hectare)', 'Decade': 'Decade'},
            template='plotly_white'
        )

        fig.update_layout(
            height=600,
            width=1200,
            title_x=0.5,
            xaxis_title='<b>Decade</b>',
            yaxis_title='<b>Avg Phosphorus (kg/hectare)</b>',
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            hovermode="x"
        )
        fig.update_traces(
            line=dict(color='#4baf47', width=2),
            fillcolor='rgba(75, 175, 71, 0.4)',
            mode='lines+markers',
            marker=dict(size=6, color='#eec044', line=dict(width=1, color='black'))
        )

        graph=fig.to_html()
        return render (request,"phos_graph.html",{"graph":graph})
    else:
     return render(request, "phos4.html",{"result":result})

def phos5(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    years1 = df['Year'].drop_duplicates().sort_values().tolist()
    countries = df['Entity'].drop_duplicates().tolist()
    years2 = df['Year'].drop_duplicates().sort_values().tolist()

    if request.method == "POST":
        start_year = int(request.POST.get('year1'))
        end_year = int(request.POST.get('year2'))
        country = request.POST.get("country1")
        df1 = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]
        df1['Growth Rate (%)'] = df1["Phosphate (kilograms per hectare)"].pct_change() * 100

        # Create a smoothed line plot for growth rate with markers
        fig = px.line(df1,
                    x="Year",
                    y="Growth Rate (%)",
                    title=f"Phosphate Usage Growth Rate for {country} ({start_year}-{end_year})",
                    labels={"Growth Rate (%)": "Growth Rate (%)"},
                    markers=True,
                    color_discrete_sequence=["#1f77b4"])  # Custom color

        # Highlight years where the growth rate is positive or negative
        fig.add_scatter(x=df1["Year"], y=df1["Growth Rate (%)"],
                        mode="markers",
                        marker=dict(size=8, color=["#2ca02c" if x > 0 else "#d62728" for x in df1["Growth Rate (%)"]]),
                        name="Positive/Negative Growth")

        # Add horizontal reference line at 0% growth rate
        fig.add_hline(y=0, line_dash="dash", line_color="black")

        # Customize layout
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",  # A clean template for better contrast
            hovermode="x unified",    # Show a unified hover label
            plot_bgcolor="#f9f9f9",   # Light background
            xaxis=dict(showgrid=False),  # Remove vertical gridlines
            yaxis=dict(showgrid=True, gridcolor="#e5e5e5")  # Light horizontal gridlines
        )
        # Customize hover labels
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")
        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph})
    else:
       return render(request, "phos5.html",{"years1":years1,"years2":years2,"countries":countries})

def phos6(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()
    if request.method == "POST":
        year = int(request.POST.get('year'))
        year_data = df[df['Year'] == year]
        fig = px.choropleth(year_data,
                            locations="Code",
                            color="Phosphate (kilograms per hectare)",
                            hover_name="Entity",
                            color_continuous_scale="viridis",
                            title=f'Global Phosphate Usage in {year}',
                            labels={'Nutrient Phosphate N (total)': 'Phosphate (kg/hectare)'}
                        )
        fig.update_layout(
            height=600,
            width=1200,
        )
        fig.update_geos(showcoastlines=True, coastlinecolor="black", projection_type="natural earth")
        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph}) 
    else:
      return render(request, "phos6.html",{"years":years})

def phos7(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get("year1"))
        end_year=int(request.POST.get("year2"))
        filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
        avg_usage = filtered_df.groupby('Entity')['Phosphate (kilograms per hectare)'].mean().reset_index()
        top10 = avg_usage.nlargest(10, 'Phosphate (kilograms per hectare)')
        fig = px.scatter(top10, x='Entity', y='Phosphate (kilograms per hectare)',
                        title='Top 10 Countries by Average Phosphate Usage',
                        color='Phosphate (kilograms per hectare)',
                        size='Phosphate (kilograms per hectare)',
                        color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_layout(
            height=600,
            width=1200,
        )
       
        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph}) 
    else:
      return render(request, "phos7.html",{"years":years})


def phos8(request):
    df=pd.read_csv("phosphorus.csv")
    df=df.rename(columns={"Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare":"Phosphate (kilograms per hectare)"})
    years = df['Year'].drop_duplicates().sort_values().tolist()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        countries=request.POST.getlist('countries[]')
        year_data = df[(df['Year'] == year) & (df['Entity'].isin(countries))]
        fig = px.bar(year_data, x='Entity', y='Phosphate (kilograms per hectare)',
                 title=f'Phosphate Usage Comparison in {year}',
                 labels={'Nutrient phosphate N (total)': 'Phosphate Usage (kg/ha)'},
                 color='Phosphate (kilograms per hectare)',
                color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_layout(
            height=600,
            width=1200,)
        graph=fig.to_html()
        return render(request,"phos_graph.html",{"graph":graph}) 
    else:
      return render(request, "phos8.html",{"years":years,"cont":cont})
    

def wheat_call():
    df=pd.read_csv("wheat-production.csv")
    df.columns = ['Entity','Code','Year', 'Production']
    return df

def wheat1(request):
    df=wheat_call()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        n= request.POST.get('country')
        df1 = df[df["Entity"] == n]

        fig = px.area(
            df1,
            x="Year",
            y="Production",
            title=f"Wheat Production in {n}",
            labels={
                "Year": "Year",
                "Production": "Wheat Production"
            },
            color_discrete_sequence=["#eec044"],  # Line color
            line_shape="linear",
        )
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Wheat Production in {n}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47"),
            ),
            xaxis_title="Year",
            yaxis_title="Wheat Production (tonnes)",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            showlegend=False
        )

        # Enable markers and customize their appearance
        fig.update_traces(
            mode="lines+markers",  # This enables both lines and markers
            line_color="#eec044",  # Line color
            fill='tozeroy',  # Fill the area under the line
            fillcolor="rgba(75, 175, 71, 0.5)",  # Fill color with transparency (#4baf47 with alpha)
            marker=dict(
                color="#eec044",  # Inside color of the marker
                line=dict(color="#4baf47", width=2)  # Border color and width of the marker
            ),
            opacity=0.8,
            text="Production",
            texttemplate='%{text:.2s}',
            textposition='top center'  # Display text at the top center of the area
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, gridcolor='gray')
        graph=fig.to_html
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat1.html",{"cont":cont})


def wheat2(request):
    df=wheat_call()
    country=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        countries=request.POST.getlist('country')
        df1 = df[df["Entity"].isin(countries)]
        fig = px.line(df1,
                  x="Year",
                  y="Production",
                  color="Entity",
                  labels={
                      "Year": "Year",
                      "Production": "Wheat Production (tonnes)"
                  },
                  color_discrete_sequence=px.colors.qualitative.Plotly  # Custom color palette
                 )

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Comparison of Wheat Production: {', '.join(countries)}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Year",
            yaxis_title="Production",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            legend=dict(
                title="Countries",
                font=dict(size=14),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="Black",
                borderwidth=1
            )
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(size=6, symbol='circle'),
            line=dict(width=2, dash='solid'),
            opacity=0.9
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')

        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat2.html",{"country":country})
    
def wheat3(request):
    df=wheat_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        n=int(request.POST.get('n'))
        df1 = df[df["Year"] == year].nlargest(n, "Production")
        rgba_color=["#4baf47","#eec044"]
        fig = px.bar(df1,
                    x="Entity",
                    y="Production",
                    color="Entity",
                    title=f"Top {n} Wheat Producing Countries in {year}",
                    text="Production",
                    color_discrete_sequence=rgba_color)

        fig.update_traces(opacity=0.8)
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Top {n} Wheat Producing Countries in {year}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Country",
            yaxis_title="Wheat Production (tonnes)",
            font=dict(family="Arial", size=14, color="black"),
            paper_bgcolor="white",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat3.html",{"years":years})
    
def wheat4(request):
    df=wheat_call()
    df=df.dropna()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        country=request.POST.get('country')
        df1 = df[df["Entity"] == country].copy()
        df1['Decade'] = (df1['Year'] // 10) * 10
        avg_production = df1.groupby("Decade")["Production"].mean().reset_index()
        max_decade = avg_production.loc[avg_production['Production'].idxmax()]
        
        fig = px.area(
            avg_production,
            x="Decade",
            y="Production",
            title=f"Average Wheat Production by Decade in {country}",
            labels={"Production": "Average Production (tonnes)"},
            color_discrete_sequence=["#4baf47"],
            line_shape="spline",
            markers=True
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(
                size=8, 
                symbol='circle', 
                line=dict(width=2, color='#eec044'),  # Border color
                color='#4baf47'  # Fill color for the markers
            ),
            fill='tozeroy',
            opacity=0.8,
            line=dict(width=2)
        )

        fig.update_layout(
            height=600,
            width=1200,
            xaxis_title="Decade",
            yaxis_title="Average Production (tonnes)",
            title=dict(
                text=f"Average Wheat Production by Decade in {country}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)),
                ticktext=[f"{int(decade)}s" for decade in range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)],
                showgrid=False  # Remove x-axis grid lines
            ),
            yaxis=dict(
                titlefont_size=14,
                tickfont_size=12,
                showgrid=False,  # Remove y-axis grid lines
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            legend_title="",
            template="plotly_white"
        )

        fig.add_vline(
            x=max_decade['Decade'],
            line=dict(color="white", width=2, dash="dash"),
            annotation_text=f"Max: {max_decade['Production']:.2f} tonnes",
            annotation_position="top right",
            annotation_font=dict(size=12, color="red")
        )

        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat4.html",{"countries":countries})
    
def wheat5(request):
    df=wheat_call()
    df.rename(columns={"Wheat | 00000015 || Production | 005510 || tonnes": "Wheat Production (Tonnes)"}, inplace=True)
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df1 = df[df["Year"] == year].copy()
        df1['Log_Wheat_Production'] = np.log1p(df1['Production'])
        min_value = df1['Log_Wheat_Production'].min()
        max_value = df1['Log_Wheat_Production'].max()

        fig = px.choropleth(
            df1,
            locations="Entity",
            locationmode="country names",
            color="Log_Wheat_Production",
            color_continuous_scale="Viridis",
            range_color=[min_value, max_value],
            labels={"Log_Wheat_Production": "Log of Production (tonnes)"},
            title=f"Global Wheat Production in {year}"
        )

        fig.update_layout(
            height=550,
            width=1000,
            geo=dict(
                showcoastlines=True,
                coastlinecolor="RebeccaPurple",
                showland=True,
                landcolor="white",
                showocean=True,
                oceancolor="lightblue",
                showlakes=True,
                lakecolor="lightblue",
                showrivers=True,
                rivercolor="blue",
                projection_type="natural earth",
            ),
            coloraxis_colorbar=dict(
                title="Production (tonnes)",
                tickvals=[min_value, (min_value + max_value) / 2, max_value],
                ticktext=[
                    f"{int(np.expm1(min_value)):,}",
                    f"{int(np.expm1((min_value + max_value) / 2)):,}",
                    f"{int(np.expm1(max_value)):,}"
                ],
            ),
            title=dict(
                text=f"Global Wheat Production in {year}",
                x=0.4,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            margin=dict(t=50, b=0, l=0, r=0),
            paper_bgcolor="white",
            plot_bgcolor="white",
            template="plotly_white"
        )

        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat5.html",{"years":years})
    
def wheat6(request):
    df=wheat_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        top_n=int(request.POST.get('top_n'))
        df1 = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
        country_year_prod = df1.groupby(["Entity", "Year"])["Production"].sum().reset_index()
        total_production = country_year_prod.groupby("Entity")["Production"].sum().reset_index()

        top_countries = total_production.nlargest(top_n, "Production")["Entity"].tolist()

        top_countries_data = country_year_prod[country_year_prod["Entity"].isin(top_countries)]
        fig = px.area(top_countries_data,
                    x="Year",
                    y="Production",
                    color="Entity",
                    title=f"Top {top_n} Wheat Producing Countries Over Time ({start_year}-{end_year})",
                    labels={"Production": "Production (Tonnes)"},
                    color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Wheat Production (Tonnes)",
            template="ggplot2",
            plot_bgcolor="white",  # Set plot background to white
            paper_bgcolor="white",
        )
        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat6.html",{"years":years})

    
def wheat7(request):
    df=wheat_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        country=request.POST.get('country')
        df1 = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]
        df1['Growth Rate (%)'] = df1["Production"].pct_change() * 100
        fig = px.line(df1,
                    x="Year",
                    y="Growth Rate (%)",
                    title=f"Wheat Production Growth Rate for {country} ({start_year}-{end_year})",
                    labels={"Growth Rate (%)": "Growth Rate (%)"},
                    markers=True,
                    color_discrete_sequence=["#eec044"])


        fig.add_scatter(x=df1["Year"], y=df1["Growth Rate (%)"],
                        mode="markers",
                        marker=dict(size=8, color=["#2ca02c" if x > 0 else "#d62728" for x in df1["Growth Rate (%)"]]),
                        name="Positive/Negative Growth")

        # Add horizontal reference line at 0% growth rate
        fig.add_hline(y=0, line_dash="dash", line_color="black")

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="#fff",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, gridcolor="#e5e5e5")
        )

        # Customize hover labels
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")
        graph=fig.to_html()
        return render(request,"crop_graph.html",{"graph":graph})
    else:
      return render(request,"wheat7.html",{"years":years,"countries":countries})


# def rice_graph(request):
#     return render(request,"rice_graph.html")  

def rice_call():
    data=pd.read_csv("rice1.csv")
    df = data.iloc[:, [1,2,4]]
    df.columns = ['Entity', 'Year', 'Production']
    return df
    

def rice1(request):
    df=rice_call()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        n= request.POST.get('country')
        df1 = df[df["Entity"] == n]

        fig = px.area(
            df1,
            x="Year",
            y="Production",
            title=f"Wheat Production in {n}",
            labels={
                "Year": "Year",
                "Production": "Rice Production"
            },
            color_discrete_sequence=["#eec044"],  # Line color
            line_shape="linear",
        )
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Rice Production in {n}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47"),
            ),
            xaxis_title="Year",
            yaxis_title="Rice Production (tonnes)",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            showlegend=False
        )

        # Enable markers and customize their appearance
        fig.update_traces(
            mode="lines+markers",  # This enables both lines and markers
            line_color="#eec044",  # Line color
            fill='tozeroy',  # Fill the area under the line
            fillcolor="rgba(75, 175, 71, 0.5)",  # Fill color with transparency (#4baf47 with alpha)
            marker=dict(
                color="#eec044",  # Inside color of the marker
                line=dict(color="#4baf47", width=2)  # Border color and width of the marker
            ),
            opacity=0.8,
            text="Production",
            texttemplate='%{text:.2s}',
            textposition='top center'  # Display text at the top center of the area
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, gridcolor='gray')
        graph=fig.to_html
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice1.html",{"cont":cont})
        
def rice2(request):
    df=rice_call()
    country=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        countries=request.POST.getlist('country')
        df1 = df[df["Entity"].isin(countries)]
        fig = px.line(df1,
                  x="Year",
                  y="Production",
                  color="Entity",
                  title=f"Comparison of Wheat Production: {', '.join(countries)}",
                  labels={
                      "Year": "Year",
                      "Production": "Rice Production (tonnes)"
                  },
                  color_discrete_sequence=px.colors.qualitative.Plotly  # Custom color palette
                 )

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Comparison of Rice Production: {', '.join(countries)}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Year",
            yaxis_title="Production",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            legend=dict(
                title="Countries",
                font=dict(size=14),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="Black",
                borderwidth=1
            )
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(size=6, symbol='circle'),
            line=dict(width=2, dash='solid'),
            opacity=0.9
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')

        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice2.html",{"country":country})


def rice3(request):
    df=rice_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        n=int(request.POST.get('n'))
        df1 = df[df["Year"] == year].nlargest(n, "Production")
        rgba_color=["#4baf47","#eec044"]
        fig = px.bar(df1,
                    x="Entity",
                    y="Production",
                    color="Entity",
                    title=f"Top {n} Rice Producing Countries in {year}",
                    text="Production",
                    color_discrete_sequence=rgba_color)

        fig.update_traces(opacity=0.8)
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Top {n} Rice Producing Countries in {year}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Country",
            yaxis_title="Rice Production (tonnes)",
            font=dict(family="Arial", size=14, color="black"),
            paper_bgcolor="white",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice3.html",{"years":years})
   

def rice4(request):
    df=rice_call()
    df=df.dropna()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        country=request.POST.get('country')
        df1 = df[df["Entity"] == country].copy()
        df1['Decade'] = (df1['Year'] // 10) * 10
        avg_production = df1.groupby("Decade")["Production"].mean().reset_index()
        max_decade = avg_production.loc[avg_production['Production'].idxmax()]
        
        fig = px.area(
            avg_production,
            x="Decade",
            y="Production",
            title=f"Average Rice Production by Decade in {country}",
            labels={"Rice Production (Tonnes)": "Average Production (tonnes)"},
            color_discrete_sequence=["#4baf47"],
            line_shape="spline",
            markers=True
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(
                size=8, 
                symbol='circle', 
                line=dict(width=2, color='#eec044'),  # Border color
                color='#4baf47'  # Fill color for the markers
            ),
            fill='tozeroy',
            opacity=0.8,
            line=dict(width=2)
        )

        fig.update_layout(
            height=600,
            width=1200,
            xaxis_title="Decade",
            yaxis_title="Average Production (tonnes)",
            title=dict(
                text=f"Average Rice Production by Decade in {country}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)),
                ticktext=[f"{int(decade)}s" for decade in range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)],
                showgrid=False  # Remove x-axis grid lines
            ),
            yaxis=dict(
                titlefont_size=14,
                tickfont_size=12,
                showgrid=False,  # Remove y-axis grid lines
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            legend_title="",
            template="plotly_white"
        )

        fig.add_vline(
            x=max_decade['Decade'],
            line=dict(color="white", width=2, dash="dash"),
            annotation_text=f"Max: {max_decade['Production']:.2f} tonnes",
            annotation_position="top right",
            annotation_font=dict(size=12, color="red")
        )

        fig.update_layout(transition_duration=500)

        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice4.html",{"countries":countries})


def rice5(request):
    df=rice_call()
    df.rename(columns={"Wheat | 00000015 || Production | 005510 || tonnes": "Wheat Production (Tonnes)"}, inplace=True)
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df1 = df[df["Year"] == year].copy()
        df1['Log_Rice_Production'] = np.log1p(df1['Production'])
        min_value = df1['Log_Rice_Production'].min()
        max_value = df1['Log_Rice_Production'].max()

        fig = px.choropleth(
            df1,
            locations="Entity",
            locationmode="country names",
            color="Log_Rice_Production",
            color_continuous_scale="Viridis",
            range_color=[min_value, max_value],
            labels={"Log_Rice_Production": "Log of Production (tonnes)"},
            title=f"Global Rice Production in {year}"
        )

        fig.update_layout(
            height=550,
            width=1000,
            geo=dict(
                showcoastlines=True,
                coastlinecolor="RebeccaPurple",
                showland=True,
                landcolor="white",
                showocean=True,
                oceancolor="lightblue",
                showlakes=True,
                lakecolor="lightblue",
                showrivers=True,
                rivercolor="blue",
                projection_type="natural earth",
            ),
            coloraxis_colorbar=dict(
                title="Production (tonnes)",
                tickvals=[min_value, (min_value + max_value) / 2, max_value],
                ticktext=[
                    f"{int(np.expm1(min_value)):,}",
                    f"{int(np.expm1((min_value + max_value) / 2)):,}",
                    f"{int(np.expm1(max_value)):,}"
                ],
            ),
            title=dict(
                text=f"Global Rice Production in {year}",
                x=0.4,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            margin=dict(t=50, b=0, l=0, r=0),
            paper_bgcolor="white",
            plot_bgcolor="white",
            template="plotly_white"
        )

        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice5.html",{"years":years})
   
def rice6(request):
    df=rice_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        top_n=int(request.POST.get('top_n'))
        df1 = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
        country_year_prod = df1.groupby(["Entity", "Year"])["Production"].sum().reset_index()
        total_production = country_year_prod.groupby("Entity")["Production"].sum().reset_index()

        top_countries = total_production.nlargest(top_n, "Production")["Entity"].tolist()

        top_countries_data = country_year_prod[country_year_prod["Entity"].isin(top_countries)]
        fig = px.area(top_countries_data,
                    x="Year",
                    y="Production",
                    color="Entity",
                    title=f"Top {top_n} Rice Producing Countries Over Time ({start_year}-{end_year})",
                    labels={"Production": "Production (Tonnes)"},
                    color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Rice Production (Tonnes)",
            template="ggplot2",
            plot_bgcolor="white",  # Set plot background to white
            paper_bgcolor="white",
        )
        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice6.html",{"years":years})


def rice7(request):
    df=rice_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        country=request.POST.get('country')
        df1 = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]
        df1['Growth Rate (%)'] = df1["Production"].pct_change() * 100
        fig = px.line(df1,
                    x="Year",
                    y="Growth Rate (%)",
                    title=f"Rice Production Growth Rate for {country} ({start_year}-{end_year})",
                    labels={"Growth Rate (%)": "Growth Rate (%)"},
                    markers=True,
                    color_discrete_sequence=["#eec044"])


        fig.add_scatter(x=df1["Year"], y=df1["Growth Rate (%)"],
                        mode="markers",
                        marker=dict(size=8, color=["#2ca02c" if x > 0 else "#d62728" for x in df1["Growth Rate (%)"]]),
                        name="Positive/Negative Growth")

        # Add horizontal reference line at 0% growth rate
        fig.add_hline(y=0, line_dash="dash", line_color="black")

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="#fff",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, gridcolor="#e5e5e5")
        )

        # Customize hover labels
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")
        graph=fig.to_html()
        return render(request,"rice_graph.html",{"graph":graph})
    else:
      return render(request,"rice7.html",{"years":years,"countries":countries})


def maize_call():
    data=pd.read_csv("global-food.csv")
    df=data.iloc[:,[1,2,4]]
    df.columns=["Entity","Year","Production"]
    return df

def maize1(request):
    df=maize_call()
    cont=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        n= request.POST.get('country')
        df1 = df[df["Entity"] == n]

        fig = px.area(
            df1,
            x="Year",
            y="Production",
            title=f"Maize Production in {n}",
            labels={
                "Year": "Year",
                "Production": "Maize Production"
            },
            color_discrete_sequence=["#eec044"],  # Line color
            line_shape="linear",
        )
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Maize Production in {n}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47"),
            ),
            xaxis_title="Year",
            yaxis_title="Maize Production (tonnes)",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            showlegend=False
        )

        # Enable markers and customize their appearance
        fig.update_traces(
            mode="lines+markers",  # This enables both lines and markers
            line_color="#eec044",  # Line color
            fill='tozeroy',  # Fill the area under the line
            fillcolor="rgba(75, 175, 71, 0.5)",  # Fill color with transparency (#4baf47 with alpha)
            marker=dict(
                color="#eec044",  # Inside color of the marker
                line=dict(color="#4baf47", width=2)  # Border color and width of the marker
            ),
            opacity=0.8,
            text="Production",
            texttemplate='%{text:.2s}',
            textposition='top center'  # Display text at the top center of the area
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, gridcolor='gray')
        graph=fig.to_html
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize1.html",{"cont":cont})
    

def maize2(request):
    df=maize_call()
    country=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        countries=request.POST.getlist('country')
        df1 = df[df["Entity"].isin(countries)]
        fig = px.line(df1,
                  x="Year",
                  y="Production",
                  color="Entity",
                  title=f"Comparison of Maize Production: {', '.join(countries)}",
                  labels={
                      "Year": "Year",
                      "Production": "Maize Production (tonnes)"
                  },
                  color_discrete_sequence=px.colors.qualitative.Plotly  # Custom color palette
                 )

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Comparison of Maize Production: {', '.join(countries)}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Year",
            yaxis_title="Production",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            legend=dict(
                title="Countries",
                font=dict(size=14),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="Black",
                borderwidth=1
            )
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(size=6, symbol='circle'),
            line=dict(width=2, dash='solid'),
            opacity=0.9
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')

        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize2.html",{"country":country})
    

def maize3(request):
    df=maize_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        n=int(request.POST.get('n'))
        df1 = df[df["Year"] == year].nlargest(n, "Production")
        rgba_color=["#4baf47","#eec044"]
        fig = px.bar(df1,
                    x="Entity",
                    y="Production",
                    color="Entity",
                    title=f"Top {n} Maize Producing Countries in {year}",
                    text="Production",
                    color_discrete_sequence=rgba_color)

        fig.update_traces(opacity=0.8)
        fig.update_layout(
            height=600,
            width=1200,
            title=dict(
                text=f"Top {n} Maize Producing Countries in {year}",
                x=0.5,
                xanchor='center',
                font=dict(size=24, color="#4baf47")
            ),
            xaxis_title="Country",
            yaxis_title="Maize Production (tonnes)",
            font=dict(family="Arial", size=14, color="black"),
            paper_bgcolor="white",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize3.html",{"years":years})
   
def maize4(request):
    df=maize_call()
    df=df.dropna()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        country=request.POST.get('country')
        df1 = df[df["Entity"] == country].copy()
        df1['Decade'] = (df1['Year'] // 10) * 10
        avg_production = df1.groupby("Decade")["Production"].mean().reset_index()
        max_decade = avg_production.loc[avg_production['Production'].idxmax()]
        
        fig = px.area(
            avg_production,
            x="Decade",
            y="Production",
            title=f"Average Maize Production by Decade in {country}",
            labels={"Production": "Average Production (tonnes)"},
            color_discrete_sequence=["#4baf47"],
            line_shape="spline",
            markers=True
        )

        fig.update_traces(
            mode='lines+markers',
            marker=dict(
                size=8, 
                symbol='circle', 
                line=dict(width=2, color='#eec044'),  # Border color
                color='#4baf47'  # Fill color for the markers
            ),
            fill='tozeroy',
            opacity=0.8,
            line=dict(width=2)
        )

        fig.update_layout(
            height=600,
            width=1200,
            xaxis_title="Decade",
            yaxis_title="Average Production (tonnes)",
            title=dict(
                text=f"Average Maize Production by Decade in {country}",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)),
                ticktext=[f"{int(decade)}s" for decade in range(min(avg_production['Decade']), max(avg_production['Decade']) + 1, 10)],
                showgrid=False  # Remove x-axis grid lines
            ),
            yaxis=dict(
                titlefont_size=14,
                tickfont_size=12,
                showgrid=False,  # Remove y-axis grid lines
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="white",
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="lightyellow",
                font_size=14,
                font_family="Arial"
            ),
            legend_title="",
            template="plotly_white"
        )

        fig.add_vline(
            x=max_decade['Decade'],
            line=dict(color="white", width=2, dash="dash"),
            annotation_text=f"Max: {max_decade['Production']:.2f} tonnes",
            annotation_position="top right",
            annotation_font=dict(size=12, color="red")
        )

        fig.update_layout(transition_duration=500)

        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize4.html",{"countries":countries})
  

def maize5(request):
    df=maize_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df1 = df[df["Year"] == year].copy()
        df1['Log_Maize_Production'] = np.log1p(df1['Production'])
        min_value = df1['Log_Maize_Production'].min()
        max_value = df1['Log_Maize_Production'].max()
        fig = px.choropleth(
            df1,
            locations="Entity",
            locationmode="country names",
            color="Log_Maize_Production",
            color_continuous_scale="Viridis",
            range_color=[min_value, max_value],
            labels={"Log_Maize_Production": "Log of Production (tonnes)"},
            title=f"Global Maize Production in {year}"
        )
        fig.update_layout(
            height=550,
            width=1000,
            geo=dict(
                showcoastlines=True,
                coastlinecolor="RebeccaPurple",
                showland=True,
                landcolor="white",
                showocean=True,
                oceancolor="lightblue",
                showlakes=True,
                lakecolor="lightblue",
                showrivers=True,
                rivercolor="blue",
                projection_type="natural earth",
            ),
            coloraxis_colorbar=dict(
                title="Production (tonnes)",
                tickvals=[min_value, (min_value + max_value) / 2, max_value],
                ticktext=[
                    f"{int(np.expm1(min_value)):,}",
                    f"{int(np.expm1((min_value + max_value) / 2)):,}",
                    f"{int(np.expm1(max_value)):,}"
                ],
            ),
            title=dict(
                text=f"Global Maize Production in {year}",
                x=0.4,
                xanchor='center',
                font=dict(size=22, color="#4baf47")
            ),
            margin=dict(t=50, b=0, l=0, r=0),
            paper_bgcolor="white",
            plot_bgcolor="white",
            template="plotly_white"
        )

        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize5.html",{"years":years})
   

def maize6(request):
    df=rice_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        top_n=int(request.POST.get('top_n'))
        df1 = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
        country_year_prod = df1.groupby(["Entity", "Year"])["Production"].sum().reset_index()
        total_production = country_year_prod.groupby("Entity")["Production"].sum().reset_index()

        top_countries = total_production.nlargest(top_n, "Production")["Entity"].tolist()

        top_countries_data = country_year_prod[country_year_prod["Entity"].isin(top_countries)]
        fig = px.area(top_countries_data,
                    x="Year",
                    y="Production",
                    color="Entity",
                    title=f"Top {top_n} Maize Producing Countries Over Time ({start_year}-{end_year})",
                    labels={"Production": "Production (Tonnes)"},
                    color_discrete_sequence=px.colors.qualitative.Set1)

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Maize Production (Tonnes)",
            template="ggplot2",
            plot_bgcolor="white",  # Set plot background to white
            paper_bgcolor="white",
        )
        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize6.html",{"years":years})
  

def maize7(request):
    df=maize_call()
    years=df['Year'].drop_duplicates().sort_values().tolist()
    countries=df['Entity'].drop_duplicates().sort_values().tolist()
    if request.method=="POST":
        start_year=int(request.POST.get('year1'))
        end_year=int(request.POST.get('year2'))
        country=request.POST.get('country')
        df1 = df[(df["Entity"] == country) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]
        df1['Growth Rate (%)'] = df1["Production"].pct_change() * 100
        fig = px.line(df1,
                    x="Year",
                    y="Growth Rate (%)",
                    title=f"Maize Production Growth Rate for {country} ({start_year}-{end_year})",
                    labels={"Growth Rate (%)": "Growth Rate (%)"},
                    markers=True,
                    color_discrete_sequence=["#eec044"])


        fig.add_scatter(x=df1["Year"], y=df1["Growth Rate (%)"],
                        mode="markers",
                        marker=dict(size=8, color=["#2ca02c" if x > 0 else "#d62728" for x in df1["Growth Rate (%)"]]),
                        name="Positive/Negative Growth")

        # Add horizontal reference line at 0% growth rate
        fig.add_hline(y=0, line_dash="dash", line_color="black")

        fig.update_layout(
            height=600,
            width=1200,
            title=dict(font_size=22, x=0.5, font=dict(color="#4baf47")),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="#fff",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, gridcolor="#e5e5e5")
        )

        # Customize hover labels
        fig.update_traces(hovertemplate="<b>Year: %{x}</b><br>Growth Rate: %{y:.2f}%")
        graph=fig.to_html()
        return render(request,"maize_graph.html",{"graph":graph})
    else:
      return render(request,"maize7.html",{"years":years,"countries":countries})




        
def remove_countries_with_missing_years(df, start_year=1961, end_year=2022):
    full_years_set = set(range(start_year, end_year + 1))
    countries_to_remove = []
    
    for country in df['Country'].drop_duplicates():
        country_years = set(df[df['Country'] == country]['Year'])
        if full_years_set != country_years:
            countries_to_remove.append(country)
    
    df_cleaned = df[~df['Country'].isin(countries_to_remove)]
    return df_cleaned

def remove_wheat(df, start_year=1961, end_year=2022):
    full_years_set = set(range(start_year, end_year + 1))
    countries_to_remove = []
    
    for country in df['Entity'].drop_duplicates():
        country_years = set(df[df['Entity'] == country]['Year'])
        if full_years_set != country_years:
            countries_to_remove.append(country)
    
    df_cleaned = df[~df['Entity'].isin(countries_to_remove)]
    return df_cleaned

def remove_countries_with_missing_years2(df, start_year=1961, end_year=2021):
    full_years_set = set(range(start_year, end_year + 1))
    countries_to_remove = []
    
    for country in df['Entity'].drop_duplicates():
        country_years = set(df[df['Entity'] == country]['Year'])
        if full_years_set != country_years:
            countries_to_remove.append(country)
    
    df_cleaned = df[~df['Entity'].isin(countries_to_remove)]
    return df_cleaned
     
def wheat_pred(request):
    # Read the CSV file and clean data
    df = pd.read_csv("wheat-production.csv")  
    df_cleaned = remove_wheat(df)
    data = df_cleaned['Entity'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Wheat Production (Tonnes)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Wheat Usage Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("wheat-production.csv", parse_dates=['Year'])
        df_cleaned = remove_wheat(df)
        country = request.POST.get('country')
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Wheat | 00000015 || Production | 005510 || tonnes']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Wheat | 00000015 || Production | 005510 || tonnes'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Wheat | 00000015 || Production | 005510 || tonnes'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Wheat Production (Tonnes)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'nitrogen_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'nitrogen_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })
     

def rice_pred(request):
    # Read the CSV file and clean data
    df = pd.read_csv("rice1.csv")  
    df_cleaned = remove_countries_with_missing_years(df)
    data = df_cleaned['Country'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Wheat Production (Tonnes)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Rice Production Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("rice1.csv", parse_dates=['Year'])
        df_cleaned = remove_countries_with_missing_years(df)
        country = request.POST.get('country')
        production = df[df['Country'] == country]
        production = production.loc[:, ['Year', 'Production (t)']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Production (t)'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Production (t)'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Rice Production (Tonnes)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'nitrogen_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'nitrogen_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })
     
     
def maize_pred(request): 
    # Read the CSV file and clean data
    df = pd.read_csv("global-food.csv")  
    df_cleaned = remove_countries_with_missing_years(df)
    data = df_cleaned['Country'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Wheat Production (Tonnes)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Maize Production Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("global-food.csv", parse_dates=['Year'])
        df_cleaned = remove_countries_with_missing_years(df)
        country = request.POST.get('country')
        production = df[df['Country'] == country]
        production = production.loc[:, ['Year', 'Production (t)']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Production (t)'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Production (t)'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Maize Production (Tonnes)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'nitrogen_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'nitrogen_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })

def phos_pred(request):
    # Read the CSV file and clean data
    df = pd.read_csv("phosphorus.csv")  
    df_cleaned = remove_countries_with_missing_years2(df)
    data = df_cleaned['Entity'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Phosphate Use (Kg/Ha)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Phosphate Usage Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("phosphorus.csv", parse_dates=['Year'])
        df_cleaned = remove_countries_with_missing_years2(df)
        country = request.POST.get('country')
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Nutrient phosphate P2O5 (total) | 00003103 || Use per area of cropland | 005159 || Kilograms per hectare'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Phosphate Use (Kg/Ha)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'potash_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'potash_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })

def nitrogen_pred(request):
    # Read the CSV file and clean data
    df = pd.read_csv("nitrogen.csv")  
    df_cleaned = remove_countries_with_missing_years2(df)
    data = df_cleaned['Entity'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Nitrogen Use (Kg/Ha)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Nitrogen Usage Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("nitrogen.csv", parse_dates=['Year'])
        df_cleaned = remove_countries_with_missing_years2(df)
        country = request.POST.get('country')
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Nutrient nitrogen N (total) | 00003102 || Use per area of cropland | 005159 || Kilograms per hectare'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Nitrogen Use (Kg/Ha)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'potash_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'potash_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })
     
def pred(request):
    return render(request,"prediction_main.html")
     
def pred_main(request):
    return render(request, "predict_main.html")

def crop_pred(request):
    return render(request,"crop_pred.html")

def fertilizer_pred(request):
    return render(request,"fertilizer_pred.html")

def potash_pred(request):
    # Read the CSV file and clean data
    df = pd.read_csv("potassium.csv")  
    df_cleaned = remove_countries_with_missing_years2(df)
    data = df_cleaned['Entity'].drop_duplicates().tolist()
    
    # Placeholder graph that shows at the beginning (for both GET and POST requests)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[2020],  # Placeholder x-axis values (e.g., years)
        y=[0],     # Placeholder y-axis values (e.g., potash use)
        mode='lines+markers',
        name='Placeholder Graph',
        line=dict(color='rgba(0,100,80,0.8)', width=2),
        marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
    ))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Potash Use (Kg/Ha)",
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)",  
        height=280,
        width=1000,
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    graph = fig.to_html()  # Convert the graph to HTML

    heading = "Potash Usage Prediction"  # Set the heading

    if request.method == 'POST':
        df = pd.read_csv("potassium.csv", parse_dates=['Year'])
        df_cleaned = remove_countries_with_missing_years2(df)
        country = request.POST.get('country')
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare']]
        production = production.sort_values('Year')
        production = production.set_index('Year')
         
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        min_aic = 99999999
        best_params = None
        best_seasonal_params = None
         
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_params = param
                        best_seasonal_params = param_seasonal
                except:
                    continue

        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_params,
                                        seasonal_order=best_seasonal_params,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit()

        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
         
        # Generate the prediction graph
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=y.index, 
            y=y['Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare'],
            mode='lines+markers', 
            name='Actual',
            line=dict(color='rgba(0,100,80,0.8)', width=2),
            marker=dict(size=8, color='rgba(0,100,80,0.8)', symbol='circle')
        ))

        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index, 
            y=pred_uc.predicted_mean,
            mode='lines+markers', 
            name='Predicted',
            line=dict(color='rgba(255,0,0,0.6)', dash='dot', width=2),
            marker=dict(size=8, color='rgba(255,0,0,0.6)', symbol='diamond')
        ))
        fig.add_trace(go.Scatter(
    x=y.index, 
    y=y['Nutrient potash K2O (total) | 00003104 || Use per area of cropland | 005159 || Kilograms per hectare'],
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,80,0.2)',
    showlegend=False))

        fig.add_trace(go.Scatter(
    x=pred_uc.predicted_mean.index, 
    y=pred_uc.predicted_mean,
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.2)',
    showlegend=False))

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Potash Use (Kg/Ha)",
            plot_bgcolor="rgba(0, 0, 0, 0)",  
            paper_bgcolor="rgba(0, 0, 0, 0)",  
            height=280,
            width=1000,
            font=dict(family="Arial", size=12),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        graph = fig.to_html()  # Update the graph with the prediction

        return render(request, 'potash_pred.html', {
            'graph': graph,
            'data': data,
            'selected_country': country,
            'steps': steps,
            'heading': heading,  # Pass the heading
        })

    # Handle GET request: render the page with the placeholder graph
    else:
        return render(request, 'potash_pred.html', {
            'graph': graph,  # Placeholder graph
            'data': data, 
            'heading': heading,  # Pass the heading
        })
    
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load the trained model
model = load_model('plant_model.keras')

class_labels = {
    0: 'Fungal - Apple Scab',
    1: 'Fungal - Black Rot',
    2: 'Fungal - Cedar Rust',
    3: 'Healthy',
    4: 'Healthy',
    5: 'Fungal - Powdery Mildew',
    6: 'Healthy',
    7: 'Fungal - Gray Leaf Spot',
    8: 'Fungal - Common Rust',
    9: 'Fungal - Northern Leaf Blight',
    10: 'Healthy',
    11: 'Fungal - Black Rot',
    12: 'Fungal - Esca',
    13: 'Fungal - Leaf Blight',
    14: 'Healthy',
    15: 'Bacterial - Citrus Greening',
    16: 'Bacterial - Spot',
    17: 'Healthy',
    18: 'Bacterial - Spot',
    19: 'Healthy',
    20: 'Fungal - Early Blight',
    21: 'Fungal - Late Blight',
    22: 'Healthy',
    23: 'Healthy',
    24: 'Healthy',
    25: 'Fungal - Powdery Mildew',
    26: 'Fungal - Leaf Scorch',
    27: 'Healthy',
    28: 'Bacterial - Spot',
    29: 'Fungal - Early Blight',
    30: 'Fungal - Late Blight',
    31: 'Fungal - Leaf Mold',
    32: 'Fungal - Septoria Leaf Spot',
    33: 'Pest - Spider Mites',
    34: 'Fungal - Target Spot',
    35: 'Viral - Yellow Leaf Curl Virus',
    36: 'Viral - Mosaic Virus',
    37: 'Healthy'
}

def plant(request):
    if request.method == 'POST' and request.FILES['image']:
        # Handle the uploaded image
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(file_path)
        full_path = fs.path(file_path)

        # Preprocess the image for plant disease detection
        img = image.load_img(full_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize for the plant disease model

        # Make prediction with the plant disease model
        predictions = model.predict(img_array)

        # Check if all predictions are below a certain threshold
        if np.max(predictions) < 0.5:  # Adjust threshold as necessary
            predicted_label = "Not a Plant"
        else:
            # Sort predictions by confidence (top-k)
            top_k_indices = np.argsort(predictions[0])[-3:][::-1]  # Get top-3 predictions
            top_k_confidences = predictions[0][top_k_indices]

            # Check if the highest prediction exceeds the confidence threshold
            confidence_threshold = 0.7  # Adjust as necessary
            if top_k_confidences[0] < confidence_threshold:
                predicted_label = "Unknown Image or Not a Plant"
            else:
                # If there is ambiguity between top classes, classify as uncertain
                if top_k_confidences[0] - top_k_confidences[1] < 0.1:  # If top-2 predictions are close
                    predicted_label = "Uncertain - Not a Plant"
                else:
                    # Predict the most confident class label
                    predicted_class = top_k_indices[0]
                    predicted_label = class_labels.get(predicted_class, "Unknown Disease")

        return render(request, 'result.html', {'label': predicted_label, 'image_url': image_url})

    return render(request, 'upload.html')

def result(request, image_url):
    context = {
        'image_url': image_url
    }
    return render(request, 'result.html', context)

# def result(request):
    
#      return render(request, 'result.html')

# def plant_eda(request):
#     return render(request,"plant_eda.html")

def plant_eda(request):
    return render(request,"plant_eda.html")

from django.shortcuts import render
import os
import random
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from matplotlib import pyplot as plt
import io
import urllib, base64

# Define the function to visualize images
def plant_eda1(request):
    # Directory path where your dataset is located
    data_directory = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'
    class_names = [
    "Tomato___Late_blight", "Tomato___healthy", "Grape___healthy", 
    "Orange___Haunglongbing_(Citrus_greening)", "Soybean___healthy", 
    "Squash___Powdery_mildew", "Potato___healthy", 
    "Corn_(maize)___Northern_Leaf_Blight", "Tomato___Early_blight", 
    "Tomato___Septoria_leaf_spot", "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", 
    "Strawberry___Leaf_scorch", "Peach___healthy", "Apple___Apple_scab", 
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Bacterial_spot", 
    "Apple___Black_rot", "Blueberry___healthy", 
    "Cherry_(including_sour)___Powdery_mildew", "Peach___Bacterial_spot", 
    "Apple___Cedar_apple_rust", "Tomato___Target_Spot", 
    "Pepper,_bell___healthy", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", 
    "Potato___Late_blight", "Tomato___Tomato_mosaic_virus", 
    "Strawberry___healthy", "Apple___healthy", "Grape___Black_rot", 
    "Potato___Early_blight", "Cherry_(including_sour)___healthy", 
    "Corn_(maize)___Common_rust_", "Grape___Esca_(Black_Measles)", 
    "Raspberry___healthy", "Tomato___Leaf_Mold", 
    "Tomato___Spider_mites Two-spotted_spider_mite", "Pepper,_bell___Bacterial_spot", 
    "Corn_(maize)___healthy"
]

    # If the form is submitted
    if request.method == 'POST':
        class_index = int(request.POST.get('class_index'))
        class_name = class_names[class_index]

        class_dir = os.path.join(data_directory, class_name)
        if not os.path.exists(class_dir):
            return render(request, 'plant_eda1.html', {'error': f"Directory for class '{class_name}' does not exist."})

        images = os.listdir(class_dir)
        if len(images) == 0:
            return render(request, 'plant_eda1.html', {'error': f"No images found for class '{class_name}'."})

        # Select images
        selected_images = random.sample(images, min(5, len(images)))
        image_data = []

        # Load and process images
        for img_name in selected_images:
            img_path = os.path.join(class_dir, img_name)
            img = load_img(img_path, target_size=(256, 256))
            img_array = img_to_array(img) / 255.0
            
            # Plot the image using matplotlib
            fig, ax = plt.subplots()
            ax.imshow(img_array)
            ax.axis('off')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            image_data.append(uri)
            plt.close()

        return render(request, 'plant_eda1.html', {'class_name': class_name, 'image_data': image_data, 'class_names': class_names})

    # Display form
    return render(request, 'plant_eda1.html', {'class_names': class_names})



import os
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render

def plant_eda2(request):
    # Set paths to train and validation directories
    train_dir = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'  # Update to the correct path
    valid_dir = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\valid'  # Update to the correct path

    # Get class names and counts
    classes = os.listdir(train_dir)
    train_class_counts = {cls: len(os.listdir(os.path.join(train_dir, cls))) for cls in classes}
    valid_class_counts = {cls: len(os.listdir(os.path.join(valid_dir, cls))) for cls in classes}

    # Plot distribution of images in the training set
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=list(train_class_counts.keys()), y=list(train_class_counts.values()), palette="husl")  # Use a colorful palette like "husl"
    plt.xticks(rotation=45, ha='right', fontsize=6)
    plt.title('Training Set: Number of Images per Class')
    plt.gcf().subplots_adjust(bottom=0.3)  # Adjusts the bottom of the plot to ensure full visibility of labels

    # Remove the borders (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add counts inside each bar vertically
    for p in ax.patches:
        # Get the center position for the label
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height() / 2),  # Center vertically
                    ha='center', va='center', color='white', fontsize=7, fontweight='bold', rotation=90)

    plt.tight_layout()  # This    
    # Save plot to a string buffer with a transparent background
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)  # Set transparent=True
    buf.seek(0)
    train_plot_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Plot distribution of images in the validation set
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=list(valid_class_counts.keys()), y=list(valid_class_counts.values()), palette="husl")  # Use the same palette for consistency
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.title('Validation Set: Number of Images per Class')
    plt.gcf().subplots_adjust(bottom=0.3)  # Adjusts the bottom of the plot to ensure full visibility of labels

    # Remove the borders (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add counts inside each bar vertically
    for p in ax.patches:
        # Get the center position for the label
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height() / 2),  # Center vertically
                    ha='center', va='center', color='white', fontsize=7, fontweight='bold', rotation=90)

    plt.tight_layout()  # This  

    # Save plot to a string buffer with a transparent background
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)  # Set transparent=True
    buf.seek(0)
    valid_plot_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Pass both plots to the template
    context = {
        'train_plot': train_plot_string,
        'valid_plot': valid_plot_string
    }

    return render(request, 'plant_eda2.html', context)

import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# def plant_eda2(request):
#     # Set paths to train and validation directories
#     train_dir = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'
#     valid_dir = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\valid'

#     # Get class names and counts
#     classes = os.listdir(train_dir)
#     train_class_counts = {cls: len(os.listdir(os.path.join(train_dir, cls))) for cls in classes}
#     valid_class_counts = {cls: len(os.listdir(os.path.join(valid_dir, cls))) for cls in classes}
#     color_palette = px.colors.qualitative.Set2

#     # Plotly bar plot for Training set
#     train_fig = px.bar(x=list(train_class_counts.keys()), 
#                        y=list(train_class_counts.values()), 
#                        labels={'y': 'Image Count'}, 
#                        title='Training Set: Number of Images per Class',
#                        color=list(train_class_counts.keys()),  # Use class names for color
#         color_discrete_sequence=color_palette )
#     train_fig.update_layout(xaxis_title='',xaxis_tickangle=-40, showlegend=False, plot_bgcolor='rgba(0,0,0,0)',width=1200,height=490,
#                             title_font=dict(size=24, color='rgb(238, 192, 68)'),  # Set title font size and color
#         title_x=0.5,  # Center the title
#         title_y=0.95 )
#     train_html = train_fig.to_html(full_html=False)

#     # Plotly bar plot for Validation set
#     valid_fig = px.bar(x=list(valid_class_counts.keys()), 
#                        y=list(valid_class_counts.values()), 
#                        labels={'y': 'Image Count'}, 
#                        title='Validation Set: Number of Images per Class',
#                        color=list(train_class_counts.keys()),  # Use class names for color
#         color_discrete_sequence=color_palette )
#     valid_fig.update_layout(xaxis_title='',xaxis_tickangle=-40, showlegend=False, plot_bgcolor='rgba(0,0,0,0)',width=1200,height=490,
#                             title_font=dict(size=24, color='rgb(238, 192, 68)'),  # Set title font size and color
#         title_x=0.5,  # Center the title
#         title_y=0.95 )
#     valid_html = valid_fig.to_html(full_html=False)

#     # Pass the HTML strings to the template
#     context = {
#         'train_plot': train_html,
#         'valid_plot': valid_html
#     }

#     return render(request, 'plant_eda2.html', context)

def plant_eda3(request):
    # Set paths to train directory
    train_dir = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'  # Update to the correct path
    classes = os.listdir(train_dir)
    
    num_samples = 3
    sample_images = []
    
    # Limit the display to 5 classes
    for i, class_name in enumerate(classes[:5]):
        class_dir = os.path.join(train_dir, class_name)
        images = os.listdir(class_dir)
        selected_images = random.sample(images, num_samples)
        
        for img_name in selected_images:
            img_path = os.path.join(class_dir, img_name)
            img = image.load_img(img_path, target_size=(256, 256))
            
            # Convert image to base64
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            img_string = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            
            # Append image data and class name to the list
            sample_images.append({
                'class_name': class_name,
                'img_string': img_string
            })

    # Pass the sample images to the template
    return render(request, 'plant_eda3.html', {'sample_images': sample_images})


def plant_eda4(request):
    # Define the list of class directories and the data directory
    class_names = [
        'Tomato___Late_blight', 'Tomato___healthy', 'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)', 'Soybean___healthy',
        'Squash___Powdery_mildew', 'Potato___healthy', 'Corn_(maize)___Northern_Leaf_Blight',
        'Tomato___Early_blight', 'Tomato___Septoria_leaf_spot',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Strawberry___Leaf_scorch',
        'Peach___healthy', 'Apple___Apple_scab', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Bacterial_spot', 'Apple___Black_rot', 'Blueberry___healthy',
        'Cherry_(including_sour)___Powdery_mildew', 'Peach___Bacterial_spot',
        'Apple___Cedar_apple_rust', 'Tomato___Target_Spot', 'Pepper,_bell___healthy',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Potato___Late_blight',
        'Tomato___Tomato_mosaic_virus', 'Strawberry___healthy', 'Apple___healthy',
        'Grape___Black_rot', 'Potato___Early_blight', 'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Common_rust_', 'Grape___Esca_(Black_Measles)',
        'Raspberry___healthy', 'Tomato___Leaf_Mold',
        'Tomato___Spider_mites Two-spotted_spider_mite', 'Pepper,_bell___Bacterial_spot',
        'Corn_(maize)___healthy'
    ]
    
    data_directory = r'plant_dataset\New Plant Diseases Dataset(Augmented)\New Plant Diseases Dataset(Augmented)\train'  # Update this path
    num_classes = len(class_names)
    images_per_row = 4
    num_rows = (num_classes + images_per_row - 1) // images_per_row
    
    sample_images = []
    
    # Loop through each class and select a sample image
    for class_name in class_names:
        class_path = os.path.join(data_directory, class_name)
        image_names = os.listdir(class_path)
        # Select a random image
        img_name = random.choice(image_names)
        
        img_path = os.path.join(class_path, img_name)
        img = load_img(img_path, target_size=(128, 128))
        img_array = img_to_array(img)
        
        # Convert the image to base64
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_string = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        sample_images.append({
            'class_name': class_name[:15],  # Limiting class name length
            'img_string': img_string
        })
    
    # Pass the sample images to the template
    return render(request, 'plant_eda4.html', {'sample_images': sample_images})



import os
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from PIL import Image
from io import BytesIO
from django.shortcuts import render
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# View to analyze image sizes, aspect ratios, and color distributions
def plant_eda5(request):
 

    return render(request, 'plant_eda5.html')

def chatbot(request):
    if not request.session.has_key('em'):
        return redirect('/Signin') 
    user=user_register.objects.get(email=request.session['em'])
    return render (request,"chatbot.html",{"user":user})
    # return render(request,'chatbot.html')

import newsapi
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def news(request):
    newsapi = NewsApiClient(api_key='f4320b784efe46a29853f60a42802b92')

    # Fetch articles from the past 29 days
    json_data = newsapi.get_everything(
        q='Smart agriculture',
        language='en',
        from_param=(datetime.today() - timedelta(days=29)).strftime('%Y-%m-%d'),
        to=datetime.today().strftime('%Y-%m-%d'),
        page_size=24,
        page=2,
        sort_by='relevancy'
    )

    articles = json_data['articles']
    return render(request, 'news.html', {'k': articles})



       





