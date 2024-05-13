from django.shortcuts import render

# Create your views here.

from .models import Message

def contact(request):
    if 'username' in request.POST:
        uname = request.POST['username']
        umail = request.POST['email']
        usub = request.POST['subject']
        ucontent = request.POST['content']
        
        obj = Message.objects.create(name = uname,email = umail,subject=usub,content=ucontent)

        obj.save()
        
        #SQL語法
        #insert into contact(name,email,subject,content)
        #標準的python:values('Bill','bill@gmail.com','學python','去哪裡學')
        
    return render(request,'contact.html')