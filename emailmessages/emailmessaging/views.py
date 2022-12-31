from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Eventsform
import re
import requests
import datetime
from .models import Messages
from django.db.models import Q
from django.core.mail import send_mail
from emailmessages import settings
# Create your views here.
def uploadingfile(request):
    if request.method=="POST":
        try:
            k = request.FILES["csv_file"]
            if not k.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect("/upload_csv/")
            if k.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (k.size/(1000*1000),))
                return HttpResponseRedirect("/upload_csv/")
        except Exception as e:
            messages.info(request,"Unable to upload file. "+repr(e))
        file_data = k.read().decode("utf-8")
        lines = file_data.split("\n") 
        try:
            for line in lines:
                validatorlog=[]
                fields=line.split(",")
                data_dict={}
                data_dict["Message"]=fields[0]
                if(len(data_dict["Message"]) not in range(1,169)):
                    validatorlog.append("Message is too short or too lengthy")

                data_dict["Email"] = fields[1]
                if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", data_dict["Email"]):
                    validatorlog.append("Email is invalid")

                data_dict["Phone"] = int(fields[2])
                if(data_dict["Phone"]//1000000000==7 or data_dict["Phone"]//1000000000==8 or (data_dict["Phone"]//1000000000==9) or (data_dict["Phone"]//1000000000==6) ):
                    pass
                else:
                    validatorlog.append("Phone number is invalid")

                data_dict["Country"] = fields[3]
                if(data_dict["Country"]=="USA" or data_dict["Country"]=="INDIA" ):
                    pass
                else:
                    validatorlog.append("Country is other than INDIA or USA")

                k= fields[4]
                if(k=="" or k=="null" or k==None):
                    now=datetime.datetime.now()
                    date_object = now.strptime("%d-%m-%Y")
                    data_dict["Schedule_date"] =date_object
                else:
                    data_dict["Schedule_date"] = datetime.datetime.strptime(k,'%d-%m-%Y').date()
                if(data_dict["Schedule_date"]<datetime.datetime.now().date()):
                    validatorlog.append("Enter valid date and time")
                if(len(validatorlog)==0):
                    validatorlog.append("MESSAGE SENT SUCCESSFULLY")
                    data_dict["validatorlog"]=str(validatorlog)
                    form=Eventsform(data_dict)
                    if form.is_valid():
                        form.save()
                else:
                    K="Message Send Failed because,"
                    data_dict["validatorlog"]=K+str((validatorlog))
                    m=Messages(Message=data_dict["Message"],Email=data_dict["Email"],Phone=data_dict["Phone"],Country=data_dict["Country"],Schedule_date=data_dict["Schedule_date"],validatorlog=data_dict["validatorlog"])
                    m.save()
            return render(request,"filesaved.html")
        except IndexError as e:
            return render(request,"filesaved.html")
    return render(request,"index.html")


def sendemailandmessages():
    #method for sending emails and messages in the given data
    m=Messages.objects.filter(~Q(validatorlog="['MESSAGE SENT SUCCESSFULLY']"))  #Remove objects containing failed messages
    m.delete()
    query_list = Messages.objects.values_list('Email',"Phone",'Message',"Country","Schedule_date").distinct()#Removing duplicate messages
    responselist=[]
    
    for i in query_list:
        m=i[4]
        if(m==datetime.datetime.now().date()): #Checking whether the given date is today or not if it is today then this method will send sms to number using sms magic api
            send_mail('no subject', i[2], settings.EMAIL_HOST_USER, [i[0]]) #sending email for each person
            url = "https://api.txtbox.in/v1/sms/send"
            payload = "mobile_number=i[1]&sms_text=i[2]&sender_id=market"
            headers = {
                    'apiKey': "9f81fddf27be1aa3e73a0619392cbc0c",
                    'content-type': "application/x-www-form-urlencoded",
                }
            response = requests.request("POST", url, data=payload, headers=headers)
            responselist.append(response)
        else:
            responselist.append("date not yet reached the scheduled date")
    print(responselist)

def textfile(request):
    #creating a text file containing report for every row of csv file.
    k=Messages.objects.values("id","Message","validatorlog","Email","Phone").all() 
    m=[]
    for i in k:
        m.append(i)
    content=str(m)
    filename = "file.txt"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    sendemailandmessages()
    j=Messages.objects.all()
    j.delete()
    return response #response will be in .txt format