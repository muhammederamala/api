from django.urls import path

from .views import (

	generate_certificate, form_view, form_handle,

	)


urlpatterns = [

	path('generate_certificate',generate_certificate,name="generate_certificate"),
	path('form_view',form_view,name="form_view"),
	path('form_handle',form_handle,name='form_handle'),

]

