from django.shortcuts import render
from django.shortcuts import render, redirect
import os
from PIL import Image, ImageDraw, ImageFont

from .models import certificate_model
from .forms import certificate_form

# Create your views here.
def home_view(request):
	print(request.headers)
	return render(request,'certificate_gen/home.html',{})

def form_view(request):
	print(request.headers)
	return render(request,'certificate_gen/form.html')

def generate_certificate(title, name, subtitle, date, signature):
    # title = 'Participation'
    # name = 'John Jacob'
    # subtitle = 'for attending the webinar on Machine Learning and Data Science' 
    # subtitle_1 ='conducted by IEEE on october 13th 2020'
    # date = '06-01-2023'
    # signature = 'signature'
    # certificate_num = 'AB00023'

    image_path = os.path.join('static','images', 'certificate.jpg')

    image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    image_width, image_height = image.size
 
    field = 'title'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (0, 0, 0)
    draw.text((text_x, text_y), title, font=font, fill=text_color)

    field = 'name'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (0,0, 0)
    draw.text((text_x, text_y), name, font=font, fill=text_color)
    
    field = 'subtitle'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (1, 27, 69)
    draw.text((text_x, text_y), subtitle, font=font, fill=text_color)

    # field = 'subtitle_1'
    # text_x, text_y, font = field_type(field)
    # text_width, text_height = draw.textsize(subtitle_1, font=font)
    # image_width, image_height = image.size
    # text_color = (1, 27, 69)
    # draw.text((text_x, text_y), subtitle_1, font=font, fill=text_color)


    field = 'date'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (0, 0, 0)
    draw.text((text_x, text_y), date, font=font, fill=text_color)


    field = 'signature'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (0, 0, 0)
    draw.text((text_x, text_y), signature, font=font, fill=text_color)


    # field = 'certificate_num'
    # text_x, text_y, font = field_type(field)
    # text_width, text_height = draw.textsize(certificate_num, font=font)
    # image_width, image_height = image.size
    # text_color = (0, 0, 0)
    # draw.text((text_x, text_y), certificate_num, font=font, fill=text_color)


    certificate_folder = os.path.join('static', 'certificates')
    if not os.path.exists(certificate_folder):
        os.makedirs(certificate_folder)

    certificate_name = "temp.jpg"

    certificate_path = os.path.join(certificate_folder, certificate_name)
    image.save(certificate_path)

    return image

def field_type(field):
	if field == 'title':
		font = ImageFont.truetype('arial.ttf', size=50)
		text_x = 515
		text_y = 300
		text_color = (235, 64, 52)
		return text_x,text_y, font

	
	elif field == 'name':
		text_x = 560
		text_y = 500
		font_path = os.path.join('static','fonts','Bartleen_Script.otf')
		font = ImageFont.truetype(font_path, size=30)
		return text_x,text_y, font

	elif field == 'subtitle':
		text_x = 250
		text_y = 600
		font_path = os.path.join('static','fonts','Rosegold.otf')
		font = ImageFont.truetype(font_path, size=30)
		return text_x,text_y, font

	elif field == 'subtitle_1':
		text_x = 410
		text_y = 650
		font_path = os.path.join('static','fonts','Rosegold.otf')
		font = ImageFont.truetype(font_path, size=30)
		return text_x,text_y, font

	elif field == 'date':
		text_x = 220
		text_y = 760
		font_path = os.path.join('static','fonts','arial.ttf')
		font = ImageFont.truetype(font_path, size=20)
		return text_x,text_y, font

	elif field =='signature':
		text_x = 920
		text_y = 760
		font_path = os.path.join('static','fonts','Find_Cartoon.ttf')
		font = ImageFont.truetype(font_path, size=20)
		return text_x,text_y, font

	elif field =='certificate_num':
		text_x = 1150
		text_y = 900
		font_path = os.path.join('static','fonts','Find_Cartoon.ttf')
		font = ImageFont.truetype(font_path, size=20)
		return text_x,text_y, font

from django.core.files.base import ContentFile
from io import BytesIO

def form_handle(request):
    if request.method == 'POST':
        form = certificate_form(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            name = form.cleaned_data['name']
            subtitle = form.cleaned_data['subtitle']
            date = str(form.cleaned_data['date'])
            signature = form.cleaned_data['signature']
            generated_certificate_file = generate_certificate(title, name, subtitle, date, signature)
            # certificate_file = form.cleaned_data['certificate_file']

            image_io = BytesIO()
            generated_certificate_file.save(image_io, format='JPEG')  # Adjust the format if needed
            image_file = ContentFile(image_io.getvalue(), name='certificate.jpg')

            # Save the form data to the model
            new_certificate_model = form.save(commit=False)
            file_name = name+'.jpg'
            new_certificate_model.certificate_file.save(file_name, image_file, save=True)

            new_certificate_model.save()
            return redirect('home_view')
        else:
            form = certificate_form(request.POST)
            print(form.errors)
            
    return redirect('form_view')