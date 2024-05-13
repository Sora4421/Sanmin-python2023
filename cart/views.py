from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponseRedirect
from cart import models
from pig.models import Goods
import os #綠界1
from django.utils.html import format_html

basedir = os.path.dirname(__file__)
file = os.path.join(basedir,'ecpay_payment_sdk.py')#綠界2


import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file#綠界3
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

cartlist = list()
customname = ''
customphone = ''
customaddress = ''
customemail = ''
orderTotal = ''
goodsTitle = list()

def cart(request):
    global cartlist
    goodslist = cartlist
    total = 0
    for unit in cartlist:
        total += int(unit[3])
        if total >= 10000:
            grandtotal = total
        else:
            grandtotal = total + 109
    if len(goodslist) == 0:
            empty = 1
    else:
            empty = 0
    return render(request,'cart.html',locals())

def addtocart(request,ctype = None,pigid = None):
    global cartlist #全域
    if ctype == 'add':
        pig = Goods.objects.filter(id = pigid).count()
        if pig > 0:
            pig = Goods.objects.get(id = pigid)
            flag = True
            #unit1是商品價格
            for unit in cartlist: #有此商品更改數量
                if pig.name == unit[0]: #0=商品名稱
                    unit[2] = str(int(unit[2])+1) #2=商品數量
                    unit[3] = str(int(unit[3])+pig.price) #3是商品總價
                    flag = False
                    break
            if flag: #沒有此商品新增商品
                templist = list()
                templist.append(pig.name)
                templist.append(str(pig.price))
                templist.append('1')
                templist.append(str(pig.price))
                cartlist.append(templist)
                
            request.session['cartlist'] = cartlist
            return redirect('/cart/')
        else:
            return redirect('/pig/')
                
    elif ctype == 'update':
        n = 0
        for unit in cartlist:
            amount = request.POST.get('qty'+str(n),'1')
            if len(amount) == 0:
                amount = '1'
            if int(amount) <= 0:
                amount = '1'
            unit[2] = amount
            unit[3] = str(int(unit[1]) * int(unit[2]))
            n += 1
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
        
        
    elif ctype == 'delete':
        del cartlist[int(pigid)]
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
#刪除使用的是索引值位置
        
    elif ctype == 'empty':
        cartlist.clear()
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
def cartorder(request):
    if 'cusEmail' in request.session:
        global cartlist,customname,customphone,customemail,customaddress
        total = 0
        goodslist = cartlist
        for unit in cartlist:
            total += int(unit[3])
        
        if total >= 10000:
            shipping = 0
        else:
            shipping = 109
        grandtotal = total + shipping
        name = customname
        phone = customphone
        email = customemail
        address = customaddress
        
        return render(request,'cartorder.html',locals())
        
    else:
        return redirect('/login')
        
def cartok(request):
    if 'cusEmail' in request.session:
        if 'cuName' in request.POST:
            global cartlist,customname,customphone,customemail,customaddress,orderTotal,goodsTitle
            total = 0
            
            for unit in cartlist:
                total += int(unit[3])
            if total >= 10000:
                shipping =0
            else:
                shipping = 109
                
            grandtotal = total + shipping
            orderTotal = grandtotal
            
            customname = request.POST.get('cuName','')
            customphone = request.POST.get('cuPhone','')
            customaddress = request.POST.get('cuAddress','')
            customemail = request.POST.get('cuEmail','')
            payType = request.POST.get('paytype')
            
            #寫進資料庫
            unitorder = models.OrderModel.objects.create(subtota = total,
                                                         shipping = shipping,
                                                         grandtotal = grandtotal,
                                                         customname = customname,
                                                         customephone = customphone,
                                                         customeemail = customemail,
                                                         customeaddress = customaddress,
                                                         paytype = payType)
            
            for unit in cartlist:
                goodsTitle.append(unit[0])
                total = int(unit[1])*int(unit[2])
                unitdetail = models.DetailModel.objects.create(dorder = unitorder,
                                                               pname = unit[0],
                                                               unitprice = unit[1],
                                                               quantity = unit[2],
                                                               dtotal = total)
                
            orderid = unitorder.id
            name = customname
            email = customemail
            cartlist.clear()
            request.session['cartlist'] = cartlist
            
            if payType == '信用卡':
                return HttpResponseRedirect('/creditcard',locals())
            else:
                return render(request,'cartok.html',locals())
        else:
            return redirect('/pig')
        
    
    
    else:
        return redirect('/login')
                
                
                
            

def cartordercheck(request):
    if 'orderid' in request.GET and 'customemail' in request.GET and 'cusEmail' in request.session:
        orderid = request.GET.get('orderid','')
        email = request.GET.get('customemail','')
        if orderid == '' or email == '':
            nosearch = 1
        else:
            order = models.OrderModel.objects.filter(id = orderid,customeemail=email).first()
            if order == None:
                notfound = 1
            else:
                details = models.DetailModel.objects.filter(dorder = order)
    return render(request,'cartordercheck.html',locals())
        

def myOrder(request):
    if 'cusEmail' in request.session:
        email = request.session['cusEmail']
        order = models.OrderModel.objects.filter(customeemail = email)
        return render(request,'myOrder.html',locals())
    else:
        return render(request,'index.html')

def reportBank(request):
    if 'orderid' in request.GET and 'customemail' in request.GET:
        orderid = request.GET.get('orderid','')
        customemail = request.GET.get('customemail','')
        if orderid !='' and customemail !='':
            bank = models.OrderModel.objects.filter(id = orderid,customeemail = customemail,paytype = '轉帳')
            if bank != None:
                return render(request,'bankfive.html',locals())
            else:
                return render(request,'product.html')
        else:
            return render(request,'index.html')
    
    else:
            return render(request,'index.html')
        
        
def bankfive(request):
    if 'orderid' in request.POST:
        orderid = request.POST['orderid']
        email = request.session['cusEmail']
        bank = request.POST['bankfive']
        obj = models.OrderModel.objects.filter(id = orderid,customeemail = email,paytype='轉帳').count()
        
        if obj > 0:
            data = models.OrderModel.objects.get(id=orderid)
            data.bankaccount = bank
            data.save()
            order = models.OrderModel.objects.filter(customeemail = email)
            
            return render(request,'myOrder.html',locals())
        else:
            return render(request,'index.html')
    else:
        return render(request,'index.html')
            




def ECPayCredit(request):#綠界SDK複製過來的CODE
    
    global goodsTitle
    title = ""
    for unit in goodsTitle:
        title += unit + "#"
    
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,
        'TradeDesc': 'Sora公司測試訂單',
        'ItemName': title ,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet',
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet/student-works',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet/student-stories',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }
    
    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html)
        return render(request,'paycredit.html',locals())
        
        
    except Exception as error:
        print('An exception happened: ' + str(error))
    
    
