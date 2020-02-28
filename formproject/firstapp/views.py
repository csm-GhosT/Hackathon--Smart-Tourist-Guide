from django.shortcuts import render
from . import forms
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,HttpResponseRedirect
import glob
import os
from PIL import Image
import argparse
from firstapp.models import user_data,searched_history
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.shortcuts import render_to_response
from VisionAPIDemo.mydemo import VisionAi



# Create your views here.
def index(request):
    emptyMedia()
    return render(request,'firstapp/start.html')

def login_as_view(request):
    return render(request,'firstapp/login.html')

def signup_as_view(request):
    return render(request,'firstapp/signup.html')

def get_started(request):
    return render(request, 'firstapp/formpage1.html', {'form':form})

def form_name_view(request):
    form =forms.FormName()
    # emptyMedia()
    if(request.method=='POST'):
        form=forms.FormName(request.POST)
        try:
            uploaded_file=request.FILES['document']

            # emptyMedia() #delete previous images
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
        except:
            not_found =True
            return render(request, 'firstapp/formpage1.html', {'form':form,'not_found':not_found})

        global uploded_image_name
        uploded_image_name=uploaded_file.name
        # renameImage()
        request.session['uploded_image_name']=uploded_image_name

        print("Image saved")
        print("imge_name:",uploded_image_name)
        print("imge_path:",getImagePath())
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS']='hackathon-the-errors-2-e704edeb01a3.json'
        vi =VisionAi()
        extracted_data =vi.search_vision(getImagePath())
        content =vi.get_summary()
        link=vi.get_wiki_link()
        title =vi.get_title()
        request.session['content']=content
        request.session['links']=link
        request.session['title']=title

        # m =monument_reviews()

        # reviews= monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s',[title])


        print(extracted_data)
        not_found =False
        if(extracted_data =='search_not_found'):
            not_found =True
            return render(request, 'firstapp/formpage1.html', {'form':form,'not_found':not_found})


        return render(request,'firstapp/information.html',{'content':content,
                                                           'impath':"../"+getImagePath(),
                                                           'not_found':not_found,
                                                           'link':link,
                                                           'title':title,
                                                           # 'reviews':reviews,
                                                           })
    return render(request, 'firstapp/formpage1.html', {'form':form})


def emptyMedia():
    files = glob.glob('media/*')
    for f in files:
        os.remove(f)

def getImagePath():
    IMAGES_DIR=".\media"
    # print(IMAGES_DIR)
    # for fileName in os.listdir(IMAGES_DIR):
    #  print(" ")
    im_dir=os.path.join(IMAGES_DIR, uploded_image_name)
    # print(im_dir)
    return im_dir

# def renameImage():
#     os.rename(getImagePath(),"media/img.png")

def jason_to_string(json_data):
    k =json_data.keys()
    lst=[]
    for k in json_data:
         lst.append(k+":"+str(json_data[k]))
    return '\n'.join(lst)

def user_signup(request):
    signup =False
    if(request.method=='POST'):
        name =request.POST.get('name')
        email =request.POST.get('email')
        number=request.POST.get('number')
        password=request.POST.get('pass')
        gender_id =request.POST.get('radio')
        if(gender_id =='1'):
            gender='male'
        elif(gender_id=='2'):
            gender='female'
        elif(gender_id=='3'):
            gender='other'


        try:
            user = User()
            user.username=email
            user.set_password(password)
            user.email_address=email
            user.save()

            db = user_data()
            db.name=name
            db.email=email
            db.phone =number
            db.gender=gender
            db.save()
            # db.password=password
            signup =True
        except IntegrityError:
            print("IntegrityError")
            signup =False
            integrity_error=True
            return render(request,'firstapp/signup.html',{'signup':signup,'integrity_error':integrity_error})

    return render(request,'firstapp/signup.html',{'signup':signup})

def user_login(request):
    if(request.method=='POST'):
        username =request.POST.get('username')
        request.session['uname']=username
        request.session.modified = True
        print(username)
        password=request.POST.get('pass')
        # print(username)
        # print(password)
        user =authenticate(username=username,password=password)
        if(user):
            if(user.is_active):
                login(request,user)
                return HttpResponseRedirect(reverse('form_name'))
            else:
                return HttpResponse("Account not active")
        else:
            return render(request,'firstapp/login.html',{'login_failed':True})
    else:
        return render(request,'firstapp/login.html')
    return render(request,'firstapp/login.html')


def information_as_view(request):
    return render(request,'firstapp/information.html')

# def submit_and_display_review(request):
#     if(request.method=='POST'):
#         review =request.POST.get('tarea')
#         # print(review)
#         global uploded_image_name
#         uploded_image_name=request.session.get('uploded_image_name')
#         content =request.session.get('content')
#         links=request.session.get('links')
#         title=request.session.get('title')
#         # data =user_data()
#         #add in user_reviews
#         username =request.session.get('uname')
#         # print(username)
#         for p in user_data.objects.raw('SELECT * FROM firstapp_user_data WHERE email = %s',[username]):
#             name =p.name
#
#         print('-----------')
#         print(username)
#         print(title)
#         print(review)
#
#         mr =monument_reviews()
#         mr.email=username
#         mr.monument_name=title
#         mr.user_review=review
#         mr.save()
#
#         reviews= monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s',[title])
#
#         return render(request,'firstapp/information.html',{'content':content,
#                                                            'impath':"../"+getImagePath(),
#                                                            'not_found':False,
#                                                            'link':links,
#                                                            'title':title,
#                                                            'reviews':reviews,
#                                                            })
