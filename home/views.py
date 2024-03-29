from django.shortcuts import render
from tkinter import E
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from rest_framework.parsers import MultiPartParser

#For qr code genrator
import qrcode
from PIL import Image
from io import BytesIO
import base64
from rest_framework.decorators import api_view

# Create your views here.
def home(request):
    return render(request, 'home.html')


def download(request, uid):
    return render(request, 'download.html', context = {'uid': uid})

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self , request):
        try:
            data = request.data
            serializer = FileListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                base_url = "http://127.0.0.1:8000/download/"
                folder = serializer.data['folder']
                full_url = base_url + folder
                context = {}
                qr_image = qrcode.make(full_url, box_size=15)
                qr_image_pil = qr_image.get_image()
                stream = BytesIO()
                qr_image_pil.save(stream, format='PNG')
                qr_image_data = stream.getvalue()
                qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
                context['qr_image_base64'] = qr_image_base64
                context['variable'] = full_url
                # print(full_url)
                return Response({
                    'status': 200,
                    'message': 'files uploaded successfully',
                    'data': serializer.data,
                    'context': context
                })
            
            return Response({
                'status' : 400,
                'message' : 'somethign went wrong',
                'data'  : serializer.errors
            })
        except Exception as e:
            print(e)

