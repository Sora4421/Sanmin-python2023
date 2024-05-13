from django.shortcuts import render

# Create your views here.


import hashlib
from .models import Customer
from django.http import HttpResponseRedirect,HttpResponse

def login(request):
    msg = ""
    if "email" in request.POST:
        email = request.POST['email']
        pwd = request.POST['password']
        pwd = hashlib.sha3_256(pwd.encode('utf-8')).hexdigest()
        obj = Customer.objects.filter(email=email,password = pwd).count()
        if obj > 0:
            #存在server端
            request.session['cusEmail']=email
            request.session['isAlive']=True
            request.session['lcc']='good'
            
            #cookie-存在本地端
            response = HttpResponseRedirect('/')
            response.set_cookie('UEmail',email,max_age=1200)
            return response
        else:
            msg = "帳號或密碼輸入錯誤，請再試一次。"
            return render(request,'login.html',locals())
    else:
        return render(request,'login.html',locals())
    
def logout(request):
    del request.session['cusEmail'] #指定刪除
    del request.session['isAlive']
    del request.session['lcc']
    
    #request.session.clear() 全部刪除
    response = HttpResponseRedirect('/')
    #response.delete_cookie('UEmail') 可不刪除cookie
    return response
def register(request):
    msg = ""
    if "uEmail" in request.POST:
        uName = request.POST['uName']
        uEmail = request.POST['uEmail']
        pwd = request.POST['password']
        sex =request.POST['sex']
        birthday = request.POST['birthday']
        mobile = request.POST['mobile']
        address = request.POST['address']
        pwd = hashlib.sha3_256(pwd.encode('utf-8')).hexdigest() #密碼加密
        obj = Customer.objects.filter(email = uEmail).count()
        if obj == 0:
            Customer.objects.create(name=uName,
                                    sex=sex,
                                    birthday=birthday,
                                    email=uEmail,
                                    mobile=mobile,
                                    address=address,
                                    password=pwd)
            msg = "註冊成功!"
        else:
            msg = "Email重覆，請更新一個"
    return render(request,'register.html',locals())        
            
#更改密碼
def changepassword(request):
    if 'cusEmail' in request.session and 'lcc' in request.session:
        msg = ''
        if 'oldPwd' in request.POST:
            oldPwd = request.POST['oldPwd']
            newPwd = request.POST['newPwd']
            oldPwd = hashlib.sha3_256(oldPwd.encode('utf-8')).hexdigest()
            newPwd = hashlib.sha3_256(newPwd.encode('utf-8')).hexdigest()
            email = request.session['cusEmail']
            obj = Customer.objects.filter(email = email,password = oldPwd).count()
            if obj > 0:
                user = Customer.objects.get(email=email)
                user.password = newPwd
                user.save()
                msg = '密碼變更成功'
            else:
                msg = '舊密碼輸入錯誤，請再試一次。'
        
        return render(request,'updatepassword.html',locals())
    
    else:
        return HttpResponseRedirect('/login')

        
def updatePensonal(request):
    pass


