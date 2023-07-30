from django.urls import path

from .views import (

	generate_certificate, form_view, form_handle, verify_view, verify_cer,download_image,download_pdf

	)


urlpatterns = [

	path('generate_certificate',generate_certificate,name="generate_certificate"),
	path('form_view',form_view,name="form_view"),
	path('form_handle',form_handle,name='form_handle'),
    path('verify_view',verify_view,name='verify_view'),
    path('verify_cer',verify_cer,name='verify_cer'),
    path('download_image/<str:certificate_number>/',download_image,name='download_image'),
    path('download_pdf/<str:certificate_number>/',download_pdf,name='download_pdf'),

]

