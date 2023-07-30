from django.shortcuts import render, redirect,  get_object_or_404
import os
from PIL import Image, ImageDraw, ImageFont
from django.http import FileResponse, HttpResponse, HttpResponseServerError

from .models import certificate_model
from .forms import certificate_form

# Create your views here.
def home_view(request):
	print(request.headers)
	return render(request,'certificate_gen/home.html',{})

def form_view(request):
	print(request.headers)
	return render(request,'certificate_gen/form.html')

def verify_view(request):
	print(request.headers)
	return render(request,'certificate_gen/verify.html',{})


def generate_certificate(title, name, subtitle, date, signature, certificate_num):

    subtitle_1 = ''
    if len(subtitle) > 60:
        subtitle_1 = subtitle[60:]
        subtitle = subtitle[:60]

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

    if subtitle_1 != '':
        field = 'subtitle_1'
        text_x, text_y, font = field_type(field)
        image_width, image_height = image.size
        text_color = (1, 27, 69)
        draw.text((text_x, text_y), subtitle_1, font=font, fill=text_color)


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


    field = 'certificate_num'
    text_x, text_y, font = field_type(field)
    image_width, image_height = image.size
    text_color = (0, 0, 0)
    certificate_num = 'certificate no:'+certificate_num
    draw.text((text_x, text_y), certificate_num, font=font, fill=text_color)


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
		text_x = 1000
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
	    
            new_certificate_model = form.save(commit=False)
            new_certificate_model.save()
            certificate_num = new_certificate_model.certificate_number
            certificate_num = str(certificate_num)

            generated_certificate_file = generate_certificate(title, name, subtitle, date, signature,certificate_num)
            # certificate_file = form.cleaned_data['certificate_file']

            image_io = BytesIO()
            generated_certificate_file.save(image_io, format='JPEG')  # Adjust the format if needed
            name_of_cer = name
            image_file = ContentFile(image_io.getvalue(), name=name_of_cer)

            # Save the form data to the model
            # new_certificate_model = form.save(commit=False)
            file_name = name+'.jpg'
            new_certificate_model.certificate_file.save(file_name, image_file, save=True)
            certificate = new_certificate_model

            new_certificate_model.save()
            return render(request,'certificate_gen/generated.html',{'certificate':certificate})
        else:
            form = certificate_form(request.POST)
            print(form.errors)
            
    return redirect('form_view')

def verify_cer(request):
	if request.method == 'POST':
		certificate_id = request.POST.get('certificate_id')
		certificate = get_object_or_404(certificate_model,certificate_number=certificate_id)
	else:
		return render('home_view')
	return render(request,'certificate_gen/verified.html',{'certificate':certificate})

def download_image(request,certificate_number):
    certificate = get_object_or_404(certificate_model, certificate_number=certificate_number)

    if certificate.certificate_file:
        response = FileResponse(certificate.certificate_file, as_attachment=True)
        return response

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Image as plat_iamge
from reportlab.lib.pagesizes import letter
from PIL import Image as PILImage

def download_pdf(request,certificate_number):
    certificate = get_object_or_404(certificate_model,certificate_number = certificate_number)
    image_file = certificate.certificate_file
    
    try:
        with PILImage.open(image_file.path) as img:
            image_format = img.format

        # Ensure the image is in a format supported by ReportLab (e.g., JPEG or PNG)
        supported_image_formats = ['JPEG', 'PNG']
        if image_format not in supported_image_formats:
            return HttpResponse("Image format not supported for PDF conversion.", status=400)

        # Create a PDF buffer
        pdf_buffer = BytesIO()

        # Create a ReportLab document
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

        # Get the image dimensions
        image_width, image_height = img.size

        # Adjust image size to fit within the PDF page
        max_width, max_height = letter  # Dimensions of the letter-sized PDF page
        if image_width > max_width or image_height > max_height:
            aspect_ratio = image_width / image_height
            if image_width > max_width:
                image_width = max_width
                image_height = int(max_width / aspect_ratio)
            if image_height > max_height:
                image_height = max_height
                image_width = int(max_height * aspect_ratio)

        # Convert the image to a PDF page and add it to the document
        pdf_page = []
        pdf_page.append(Image(image_file.path, width=image_width, height=image_height))
        doc.build(pdf_page)

        # Set response headers for PDF download
        response = FileResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="image_to_pdf.pdf"'

        return response

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error generating PDF: {e}")
        return HttpResponseServerError("Failed to generate the PDF.")