import email
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BillData
from django.shortcuts import HttpResponse,redirect,render
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
from auth_app.models import Billswift
from pathlib import Path
import mimetypes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.

import re

def is_valid_email(email):
    return bool(re.match(r'^\S+@\S+\.\S+$', email))

def is_valid_password(password):
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@,$,_,-])', password))


def Create_Account(request):
    try:
        if request.method == "POST":
            uname = request.POST.get('username')
            email = request.POST.get('email')
            passw = request.POST.get('password')
            print(uname,email,passw)
        
        try:


            if not is_valid_email(email):
                print(is_valid_email(email),"email>>>>")
                messages.error(request, 'Invalid email address.')
                return render(request, 'signup.html')

            if not is_valid_password(passw):
                print(is_valid_password(passw),"password>>>")
                messages.error(request, 'Invalid password. Password must meet the criteria.')
                return render(request, 'signup.html')
            
            if User.objects.filter(username=uname).first():
                messages.success(request,'username is taken')

            if User.objects.filter(email=email).first():
                messages.success(request,'email is taken')
            
            else:
                user = User(username=uname,email=email)
                user.set_password(passw)
                user.save()
                messages.success(request,'Account created !!')


        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
  
    return render(request,'signup.html')


def login_handle(request):


    try:

        if request.method == "POST":
            global username
            username = request.POST.get('username')
            password =request.POST.get('password')
            print(username,password)
            if username=='garvit' and password=='Garv@123':
                # bill_data = BillData.objects.all()
                # return render(request, 'display_bills.html', {'bill_data': bill_data})
                # return render(request,'managerpage.html')
                return redirect('display_bills')
            if not username or not password:
                messages.success(request,'Boths fields are required !')

            user_obj = User.objects.filter(username=username).first()
            user = authenticate(username=username,password=password)

            if user_obj is None:
                messages.success(request,'User Not found !')
            print(user_obj)

            if user is not None:
                login(request,user)
                # return render(request,'index.html')
                return redirect('/index_login/')
            
            if user is None:
                messages.success(request,'Wrong Password !!')
            
            

        
    except Exception as e:
        print(e)

    return render(request,'login.html')
    


@login_required(login_url='/')
def logouthandle(request):

    try:

        logout(request)
    
    except Exception as e:
        print(e)

    return redirect("/")


def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')
    
def index_login(request):
    if request.method == "POST":
        user = request.user
        email=user.email
        file = request.FILES["file"]
        Billswift(user=user, file=file).save()
        # Get all uploaded files
        uploaded_files = Billswift.objects.filter(user=request.user)
        print(uploaded_files)
        url = uploaded_files.last()
        global url_link
        url_link = url.file
        url_link = 'media/' + str(url_link)

        import cv2
        import re
        import nltk
        from paddleocr import PaddleOCR, draw_ocr

        l1 = []
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        image = cv2.imread(url_link, 0)
        result = ocr.ocr(url_link, cls=True)
        for i in range(len(result[0])):
            l1.append(result[0][i][1][0])

        l2 = []
        for i in l1:
            if i.isdigit():
                l2.append(int(i))

        price = max(l2)
        for i in l1:
            text = " ".join(l1)
        match = re.findall(r'\d+[/.-]\d+[/.-]\d+', text)
        date_on_bill = " "
        date_on_bill = date_on_bill.join(match)
        if date_on_bill != " ":
            print(date_on_bill)
        else:
            match = re.findall(r'^(0[1-9]|[1-2][0-9]|3[0-1])-(jan|feb|mar|apr|May|jun|jul|aug|sep|oct|nov|dec)-\d{2}$',
                               text)
            date_on_bill = " "
            date_on_bill = date_on_bill.join(match)
        print(date_on_bill)
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        new_words = tokenizer.tokenize(text)
        print(new_words)
        global title
        title = l1[0]
        print(title)
        entertainment = ['happy', 'restaurant', 'food', 'kitchen', 'hotel', 'room', 'park', 'movie', 'cinema',
                         'popcorn', 'combo meal', 'delicacies']
        home_utility = ['internet', 'telephone', 'elecricity', 'meter', 'wifi', 'broadband', 'consumer', 'reading',
                        'gas', 'postpaid', 'prepaid']
        grocery = ['bigbasket', 'milk', 'atta', 'sugar', 'suflower', 'oil', 'bread', 'vegetabe', 'fruit', 'salt',
                   'paneer','confectioners','mart']
        investment = ['endowment', 'grant', 'loan', 'applicant', 'income', 'expenditure', 'profit', 'interest',
                      'expense', 'finance', 'property', 'money']
        transport = ['cab', 'ola', 'uber', 'autorickshaw', 'railway', 'air', 'emirates', 'aerofloat', 'taxi',
                     'booking','highway', 'depot', 'rsrtc','petrol','vehicle']
        shopping = ['iphone', 'laptop', 'saree', 'max', 'pantaloons', 'westside', 'vedic', 'makeup', 'lipstick',
                    'cosmetics', 'mac', 'facewash', 'heels', 'crocs', 'footwear', 'purse','bazar']
        e = False
        inv = False
        g = False
        s = False
        t = False
        h = False
        for word in new_words:
            if word.lower() in entertainment:
                e = True
                break
            elif word.lower() in investment:
                inv = True
                break
            elif word.lower() in grocery:
                g = True
                break
            elif word.lower() in shopping:
                s = True
                break
            elif word.lower() in transport:
                t = True
                break
            elif word.lower() in home_utility:
                h = True
                break
        global category
        if e:
            category = 'Entertainment'
        elif inv:
            category = 'Investment'
        elif g:
            category = 'Grocery'
        elif s:
            category = 'Shopping'
        elif t:
            category = 'Transport'
        elif h:
            category = 'Home Utility'
        from datetime import datetime
        date_of_upload = datetime.today().date()
        date_of_upload = date_of_upload.strftime("%d/%m/%y")
        data = {'Title': title, 'date_on_bill': date_on_bill, 'Price': price, 'Category': category,'date_of_upload': date_of_upload}
        global status
        status="Pending"
        bill_data = BillData(
            date_of_upload=date_of_upload,
            email=email,
            date_on_bill=date_on_bill,
            title=title,
            category=category,
            price=price,
            status=status,
            view_bill=url.file
        )

# Save the instance to the database
        bill_data.save()
        # Pass the uploaded files and the data of the newly uploaded file to the template
        # return render(request, 'userupload.html', {'uploaded_files': uploaded_files, 'data': data})
    bill_data = BillData.objects.all().order_by('-date_of_upload')
    username=request.user.username
    usmail = request.user.email
    return render(request, 'userupload.html', {'bill_data': bill_data,'username':username,'usmail':usmail})
    # return render(request, 'userupload.html')

def delete_bill(request):
    if request.method == 'POST':
        # Get the bill ID from the POST request
        bill_id = request.POST.get('bill_id')

        # Try to get the bill object
        bill = BillData.objects.get(id=bill_id)
            # Delete the bill
        bill.delete()
            # Return a success message
        

    # Redirect back to the page where the request originated
        return redirect('/')

def Home(request):
    return render(request,'Home.html')

def view_image(request):
    image_path = Path('static/wallpaper.png').resolve()

    with open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(),content_type=mimetypes.guess_type(image_path)[0])
    # bill = get_object_or_404(Bill, id=bill_id)
    # with open(bill.bill_image.path, 'rb') as image_file:
    #     response = HttpResponse(image_file.read(), content_type=mimetypes.guess_type(bill.bill_image.path)[0])
    return response
def view_bill_image(request, bill_id):
    bill = get_object_or_404(BillData, id=bill_id)
    with open(bill.view_bill.path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type=mimetypes.guess_type(bill.view_bill.path)[0])
    return response
# def view_bill_image(request):
#     image_path = Path('{}'.format(url_link)).resolve()

#     with open(image_path, 'rb') as image_file:
#         response = HttpResponse(image_file.read(),content_type=mimetypes.guess_type(image_path)[0])

#     return response

def display_bills(request):
    # Retrieve all records from the BillData table
    bill_data = BillData.objects.all()

    # Pass the retrieved records to the template
    return render(request, 'display_bills.html', {'bill_data': bill_data})

def filter_bills(request):
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    
    if status and category:
        filtered_bills = Bill.objects.filter(status=status, category=category)
    elif status:
        filtered_bills = Bill.objects.filter(status=status)
    elif category:
        filtered_bills = Bill.objects.filter(category=category)
    else:
        filtered_bills = Bill.objects.all()
    
    return render(request, 'display_bills.html', {'bill_data': filtered_bills})
def approve_bill(request, bill_id):
    bill = get_object_or_404(BillData, id=bill_id)
    # Perform actions to approve the bill (e.g., update status in the database)
    bill.status = 'Approved'
    bill.save()
    # subject = 'Your bill has been approved'
    # message = f'Your bill of {bill.title}with ID {bill_id} has been approved.'
    # from_email = 'garvitm0601@gmail.com'  # Replace with your email
    # to_email = bill.email
    # send_mail(subject, message, from_email, [to_email])
    message = (
    "Hey !!,\n\n"
    "We are pleased to inform you that your bill has been approved.\n\n"
    "Bill Details:\n"
    f"Title: {bill.title}\n"
    f"Category: {bill.category}\n"
    f"Price: {bill.price}\n\n"
    "Thank you for your submission.\n\n"
    "Best regards,\n"
    "BillSwift\n"
    "Senior Manager"
)
    # send_email("Bill has been approved",bill.email,f"Your bill of {bill.title} has been approved by the manager")
    send_email("Bill has been approved",bill.email,message)
    return redirect('display_bills')

def reject_bill(request, bill_id):
    bill = get_object_or_404(BillData, id=bill_id)
    # Perform actions to reject the bill (e.g., update status in the database)
    bill.status = 'Rejected'
    bill.save()
    message = (
    "Hey !!,\n\n"
    "We regret to inform you that your bill has been rejected.\n"

    "Bill Details:\n"
   f"Title: {bill.title}\n"
   f"Price: {bill.price}\n"
   f"Category: {bill.category}\n\n"
   "If you have any questions or concerns, please don't hesitate to contact us.\n"

   "Thank you for your understanding.\n\n"
   "Best regards,\n"
   "BillSwift"
   "Senior Manager"
)
    # send_email("Bill has been Rejected",bill.email,f"Sorry !! Your bill of {bill.title} has been Rejected by the manager. Feel free to contact support team to know more.")
    send_email("Bill has been Rejected",bill.email,message)
    return redirect('display_bills')

def send_email(subject, recipient, body):
    email_sender = 'garvitmathur2003@gmail.com'
    email_password = 'rgma omii tjfs axcn'

    # Create a MIMEText object to represent the email body
    email_body = MIMEText(body, 'plain')

    # Create a MIMEMultipart object to represent the email message
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = recipient
    message['Subject'] = subject

    # Attach the email body to the message
    message.attach(email_body)
    # Connect to the SMTP server
    # server = smtplib.SMTP('64.233.184.108')
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()  # Start TLS encryption
        server.login(email_sender, email_password)  # Login to the email server
        server.sendmail(email_sender, recipient, message.as_string())
   
from django.http import JsonResponse

def upload_bill(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Process the uploaded file as needed
        file_name = uploaded_file.name  # Get the file name
        # Do other processing if needed
        return JsonResponse({'file_name': file_name})  # Return the file name in the response
    else:
        # Handle the case when no file is uploaded
        return JsonResponse({'error': 'No file uploaded'}, status=400)
