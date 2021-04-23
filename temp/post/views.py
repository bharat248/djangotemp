from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import locate
import cv2
import os
# Create your views here.
model_loaded = False
if model_loaded == False:
    locate.load_model()
    model_loaded = True
folder_path = 'Z:\\djangotemp\\temp\\media\\'
file = open(folder_path + "data.txt", "w")
file.write("Number Plate ------- " + "Date - time of arrival \n")
file.close()

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        global model_loaded
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            img_name = request.data.get('title')
            img = cv2.imread('Z:\djangotemp\\temp\\media\\' + img_name)
            os.remove('Z:\djangotemp\\temp\\media\\' + img_name)
            locate.run_locate(img)
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
