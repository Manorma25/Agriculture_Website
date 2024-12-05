"""
URL configuration for Agriculture_Website project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from AgroTech import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('Signup',views.signup,name="Signup"),
    path('Signin',views.signin,name="Signin"),
    
    path('',views.index,name="Home"),
    path('base',views.base),
    path('Contact Us',views.contact,name="Contact Us"),
    path('About',views.about,name="About"),
    path('News',views.news,name="News"),
    path('Services',views.services,name="Services"),

    path('FAQ',views.faq,name="FAQ"),
    path('Forgot',views.forgot,name="Forgot"),
    path('Cont',views.cont,name="Cont"),
    path('Check',views.otp,name="Check"),
    path('Thanku',views.thanku,name="Thanku"),
    path('ThankYou',views.thanku_reg,name="ThankYou"),
    path('Sidebar',views.sidebar,name="Sidebar"),
    path('User Profile',views.user_profile,name="User Profile"),
    path('Change Password',views.changePassword,name="Change Password"),
    path('Side',views.side,name="Side"),
    path('Edit Profile',views.edit_profile,name="Edit Profile"),
    path('Logout',views.logout,name="Logout"),
    path('University',views.university,name="University"),
    path('Latest Technologies',views.technologies,name="Latest Technologies"),
    path('Schemes',views.schemes,name="Schemes"),
    path('Scheme Details/<int:scheme_id>/',views.scheme_details,name="Scheme Details"),
    path('Call Center',views.call_center,name="Call Center"),
    path('State',views.state,name="State"),
    path('month/<int:state_id>/', views.month, name='month'),
    path('crops/<int:state_id>/<str:month>/',views.crops,name="Crop"),
    path('i',views.i),
    path("nitrogend",views.avg_nitrogen_by_decade_area_chart,name="nd"),
    path("nitrogen1", views.nitrogen_usage, name="nitrogen1"),
    path("nitrogen2", views.nitrogen_compare, name="nitrogen2"),
    path("nitrogen3", views.top_n_nitrogen_usage, name="nitrogen3"),
    path("nitrogen5",views.country_production_growth_rate,name="nitrogen5"),
    path("nitrogen6",views.nitrogen_usage2,name="nitrogen6"),
    path("nitrogen7",views.avg_nitrogen_usage,name="nitrogen7"),
    path("nitrogen8",views.compare_nitrogen_usage,name="nitrogen8"),
    path('fertilizers', views.fertilizers, name="fertilizers" ),
    path('fertilizer_ques', views.fertilizer_ques, name="fertilizer_ques"),
    path('fertilizer_graph',views.fert_graph,name="fertilizer_graph"),

    path('potassium_ques',views.potassium_ques,name="potassium_ques"),
    #path('potash_graph',views.potash_graph,name="potash_graph"),
    path('potash1',views.potassium_usage,name="potash1"),
    path('potash2',views.potash2,name="potash2"),
    path('potash3',views.potash3,name="potash3"),
    path('potash4',views.potash4,name="potash4"),
    path('potash5',views.potash5,name="potash5"),
    path('potash6',views.potash6,name="potash6"),
    path('potash7',views.potash7,name="potash7"),
    path('potash8',views.potash8,name="potash8"),

    #path('phos_graph',views.phos_graph,name="phos_graph"),
    path('phos1',views.phos1,name="phos1"),
    path('phos2',views.phos2,name="phos2"),
    path('phos3',views.phos3,name="phos3"),
    path('phos4',views.phos4,name="phos4"),
    path('phos5',views.phos5,name="phos5"),
    path('phos6',views.phos6,name="phos6"),
    path('phos7',views.phos7,name="phos7"),
    path('phos8',views.phos8,name="phos8"),
    path('phosphorus_ques',views.phosphorus_ques,name="phosphorus_ques"),

    path('Crop2',views.main_crop,name="Crop2"),

    path('wheat_ques',views.wheat_ques,name="wheat_ques"),
    #path('wheat_graph',views.wheat_graph, name="wheat_graph"),
    path('wheat1',views.wheat1,name="wheat1"),
    path('wheat2',views.wheat2,name="wheat2"),
    path('wheat3',views.wheat3,name="wheat3"),
    path('wheat4',views.wheat4,name="wheat4"),
    path('wheat5',views.wheat5,name="wheat5"),
    path('wheat6',views.wheat6,name="wheat6"),
    path('wheat7',views.wheat7,name="wheat7"),

    path('rice_ques',views.rice_ques,name="rice_ques"),
    #path('rice_graph',views.rice_graph,name="rice_graph"),
    path('rice1',views.rice1,name="rice1"),
    path('rice2',views.rice2,name="rice2"),
    path('rice3',views.rice3,name="rice3"),
    path('rice4',views.rice4,name="rice4"),
    path('rice5',views.rice5,name="rice5"),
    path('rice6',views.rice6,name="rice6"),
    path('rice7',views.rice7,name="rice7"),
    path('maize_ques',views.maize_ques,name="maize_ques"),
    #path('maize_graph',views.maize_graph,name="maize_graph"),
    path('maize1',views.maize1, name="maize1"),
    path('maize2',views.maize2, name="maize2"),
    path('maize3',views.maize3, name="maize3"),
    path('maize4',views.maize4, name="maize4"),
    path('maize5',views.maize5, name="maize5"),
    path('maize6',views.maize6, name="maize6"),
    path('maize7',views.maize7, name="maize7"),
    path('dash',views.dashboard, name="dash"),

    path('pred_main',views.pred_main, name="pred_main"),
    path('nitrogen_pred', views.nitrogen_pred, name="nitrogen_pred"),
    path('potash_pred', views.potash_pred, name="potash_pred"),
    path('wheat_pred', views.wheat_pred, name="wheat_pred"),
    path('rice_pred', views.rice_pred, name="rice_pred"),
    path('maize_pred', views.maize_pred, name="maize_pred"),
    path('phos_pred', views.phos_pred, name="phos_pred"),
    path('pred',views.pred,name="pred"),
    path('crop_pred',views.crop_pred,name="crop_pred"),
    path('fertilizer_pred',views.fertilizer_pred,name="fertilizer_pred"),
    path('plant', views.plant, name='plant'),
    path('result',views.result,name="result"),
    path('plant_eda',views.plant_eda,name="plant_eda"),
    path('plant_eda1',views.plant_eda1,name="plant_eda1"),
    path('plant_eda2',views.plant_eda2,name="plant_eda2"),
    path('plant_eda3',views.plant_eda3,name="plant_eda3"),
    path('plant_eda4',views.plant_eda4,name="plant_eda4"),
    path('plant_eda5',views.plant_eda5,name="plant_eda5"),
    path('chatbot',views.chatbot,name="chatbot"),
    path('Blogs',views.blog_view,name="Blogs"),
    path('blog_detail/<int:blog_id>/',views.blog_detail,name="blog_detail"),

    path('Signin_g',views.signin_google,name="Signin_g"),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("google-login/", views.google_login, name="google_login"),

 

    
  

    
]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
