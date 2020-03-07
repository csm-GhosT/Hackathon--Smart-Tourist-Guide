from django.shortcuts import render
from . import forms
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,HttpResponseRedirect
import glob
import os
from PIL import Image
import argparse
from firstapp.models import user_data,searched_history,monument_reviews,information
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.shortcuts import render_to_response
from VisionAPIDemo.mydemo import VisionAi
from django.db import transaction
from MainApi import awsText



# Create your views here.
def adminlogin_as_view(request):
    if(request.method=='POST'):
        admin_uname =request.POST.get('uname')
        admins_pass =request.POST.get('pass')
        if(admin_uname =='system'):
            if(admins_pass=='root'):
                request.session['admin_logged'] = 'logged'
                # query =monument_reviews.objects.raw('SELECT DISTINCT monument_name FROM firstapp_searched_history')
                query =searched_history.objects.values('monument_name').distinct()

                # print(query)
                return render(request,'firstapp/admin-firstpage.html',{'data':query,})
            else:
                request.session['admin_logged']=False
                return render(request,'firstapp/login1.html',{'login_failed':True})
        else:
            request.session['admin_logged']=False
            return render(request,'firstapp/login1.html',{'login_failed':True})

    return render(request,'firstapp/login1.html')

def adminfirstpage_as_view(request):
    if(request.session.get('admin_logged')!='logged'):
        # print('success',request.session.get('admin_logged'))
        return HttpResponse("Error")
    query =searched_history.objects.values('monument_name').distinct()

    # print(query)
    return render(request,'firstapp/admin-firstpage.html',{'data':query,})


def adminpending_as_view(request):

    return render(request,'firstapp/admin-pending.html')

def adminapproved_as_view(request):
    return render(request,'firstapp/admin-approved.html')

def adminfeedback_as_view(request):


    return render(request,'firstapp/admin-feedback.html')

def admin_search_req(request):
    if(request.method=='POST'):
        list =request.POST['monument_list']
        # print("list",list)

    query =searched_history.objects.values('monument_name').distinct()
    print(query)
    # answers_list = list(query)
    # print(answers_list  )

    return render(request,'firstapp/admin-firstpage.html',{'data':query})




def get_list(query):
    lst =[]
    for q in query:
        lst.append((q['monument_name'].replace(" ", "_")))
    print("lst:",lst)
    return lst

def index(request):
    emptyMedia()
    return render(request,'firstapp/start.html')

def login_as_view(request):
    return render(request,'firstapp/login.html')

def signup_as_view(request):
    return render(request,'firstapp/signup.html')

def get_started(request):
    return render(request, 'firstapp/formpage1.html', {'form':form})

def scan_recipt_as_view(request):
        print("received call")
        form =forms.FormName()
        # emptyMedia()
        if(request.method=='POST'):
            print("received post")
            form=forms.FormName(request.POST)
            try:
                uploaded_file=request.FILES['document']

                # emptyMedia() #delete previous images
                fs = FileSystemStorage()
                fs.save(uploaded_file.name,uploaded_file)
            except:
                print("image uplod failed")

            username =request.session.get('uname')
            global uploded_image_name
            uploded_image_name=uploaded_file.name

            text=jason_to_string(awsText.main(getImagePath()))
            # print(text)
            print("username:",username)
            return render(request,'firstapp/formpage.html',{'text':text,'impath':"../"+getImagePath(),'uname':username})

        username =request.session.get('uname')
        print("username:",username)
        return render(request,'firstapp/formpage.html',{'uname':username})



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
        username =request.session.get('uname')

        # m =monument_reviews()

        reviews= monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s',[title])
        query =monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s AND email= %s ',[title,username])
        # print(query)
        if(query):
            exists =True
        else:
            exists =False


        print(extracted_data)
        print(exists)
        not_found =False
        if(extracted_data =='search_not_found'):
            not_found =True
            return render(request, 'firstapp/formpage1.html', {'form':form,'not_found':not_found})


        sh =searched_history()
        sh.email =username
        sh.monument_name =title.replace(" ", "_")
        sh.save()


        return render(request,'firstapp/information.html',{'content':content,
                                                           'impath':"../"+getImagePath(),
                                                           'not_found':not_found,
                                                           'link':link,
                                                           'title':title,
                                                           'reviews':reviews,
                                                           'review_exists':exists,
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
        else:
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

def review_handler(request):
    if(request.method=='POST'):
        star_id =request.POST.get('rating')
        star2_id=request.POST.get('rating2')
        star3_id=request.POST.get('rating3')
        star4_id=request.POST.get('rating4')
        star5_id=request.POST.get('rating5')
        ratings_dict =get_ratings(star_id,star2_id,star3_id,star4_id,star5_id)
        # print(ratings_dict)
        q1 =ratings_dict['q1']
        q2=ratings_dict['q2']
        q3=ratings_dict['q3']
        q4=ratings_dict['q4']
        q5=ratings_dict['q5']
        avg =(q5+q4+q3+q2+q1)/5

        global uploded_image_name
        uploded_image_name=request.session.get('uploded_image_name')
        username =request.session.get('uname')
        content =request.session.get('content')
        links=request.session.get('links')
        title=request.session.get('title')
        print("avg:",avg)

        mr=monument_reviews()
        mr.email=username
        mr.monument_name=title
        mr.rating1=q1
        mr.rating2=q2
        mr.rating3=q3
        mr.rating4=q4
        mr.rating5=q5
        mr.total_avg=avg
        mr.save()

        reviews= monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s',[title])
        query =monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s AND email= %s ',[title,username])
        # print(query)
        if(query):
            exists =True
        else:
            exists =False


        return render(request,'firstapp/information.html',{'content':content,
                                                                   'impath':"../"+getImagePath(),
                                                                   'not_found':False,
                                                                   'link':links,
                                                                   'title':title,
                                                                   'reviews':reviews,
                                                                   'review_exists':exists,
                                                                   })



    return render(request,'firstapp/information.html')


def add_extra_info(request):
    if(request.method=='POST'):
        global uploded_image_name
        uploded_image_name=request.session.get('uploded_image_name')
        username =request.session.get('uname')
        content =request.session.get('content')
        links=request.session.get('links')
        title=request.session.get('title')
        # print(query)

        info =request.POST.get('tarea')

        inf=information()
        inf.email =username
        inf.monument_name=title
        inf.information =info
        inf.flag =False
        inf.save()

        info_sumitted =True
        reviews= monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s',[title])
        query =monument_reviews.objects.raw('SELECT * FROM firstapp_monument_reviews WHERE monument_name = %s AND email= %s ',[title,username])
        if(query):
            exists =True
        else:
            exists =False

        return render(request,'firstapp/information.html',{'content':content,
                                                                   'impath':"../"+getImagePath(),
                                                                   'not_found':False,
                                                                   'link':links,
                                                                   'title':title,
                                                                   'reviews':reviews,
                                                                   'review_exists':exists,
                                                                   'info':info_sumitted,
                                                                   })


    return render(request,'firstapp/information.html')



def get_ratings(star_id,star2_id,star3_id,star4_id,star5_id):
    ratings_dict ={}

    # REFACTOR############################################################E
    if(star_id=='1'):
        ratings_dict['q1']=1
    elif(star_id=='2'):
        ratings_dict['q1']=2
    elif(star_id=='3'):
        ratings_dict['q1']=3
    elif(star_id=='4'):
        ratings_dict['q1']=4
    elif(star_id=='5'):
        ratings_dict['q1']=5
    else:
        ratings_dict['q1']=5

    if(star2_id=='1'):
        ratings_dict['q2']=1
    elif(star2_id=='2'):
        ratings_dict['q2']=2
    elif(star2_id=='3'):
        ratings_dict['q2']=3
    elif(star2_id=='4'):
        ratings_dict['q2']=4
    elif(star2_id=='5'):
        ratings_dict['q2']=5

    if(star3_id=='1'):
        ratings_dict['q3']=1
    elif(star3_id=='2'):
        ratings_dict['q3']=2
    elif(star3_id=='3'):
        ratings_dict['q3']=3
    elif(star3_id=='4'):
        ratings_dict['q3']=4
    elif(star3_id=='5'):
        ratings_dict['q3']=5

    if(star4_id=='1'):
        ratings_dict['q4']=1
    elif(star4_id=='2'):
        ratings_dict['q4']=2
    elif(star4_id=='3'):
        ratings_dict['q4']=3
    elif(star4_id=='4'):
        ratings_dict['q4']=4
    elif(star4_id=='5'):
        ratings_dict['q4']=5

    if(star5_id=='1'):
        ratings_dict['q5']=1
    elif(star5_id=='2'):
        ratings_dict['q5']=2
    elif(star5_id=='3'):
        ratings_dict['q5']=3
    elif(star5_id=='4'):
        ratings_dict['q5']=4
    elif(star5_id=='5'):
        ratings_dict['q5']=5

    return ratings_dict;
