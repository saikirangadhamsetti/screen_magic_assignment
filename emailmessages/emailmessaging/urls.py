from django.urls import path
from .views import uploadingfile,textfile
urlpatterns=[
    path("upload_csv/",uploadingfile),
    path("textfile/",textfile),
]
