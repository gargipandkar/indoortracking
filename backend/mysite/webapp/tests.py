from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Floorplan

import os

class ClientTest(TestCase):
    def setUp(self):
        self.client = Client()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imgfilepath = os.path.join(BASE_DIR, "webapp\\static\\images\\testimg.jpg")

    def test_upload_invalidfile(self):
        text_file = SimpleUploadedFile('invalidfile.txt', b'this is some text - not an image')
        form_data = {'title': "Invalid file", 'plan': text_file}

        response = self.client.post(reverse('addplan'), form_data, follow=True)
        self.assertContains(response, 'Upload a valid image.')
        
    def test_upload_image(self):
        with open(self.imgfilepath, 'rb') as f:
            img_file = SimpleUploadedFile('testimg.jpg', f.read())
        form_data = {'title': "Image file", 'plan': img_file}
        
        response = self.client.post(reverse('addplan'), form_data, follow=True)
        self.assertRegex(response.redirect_chain[0][0], r'/')    
        self.assertIsNotNone(Floorplan.objects.get(title="Image file"))
        
    def test_unique_plantitle(self):
        with open(self.imgfilepath, 'rb') as f:
            img_file = SimpleUploadedFile('testimg.jpg', f.read())
        plan_title = "Plan A"
        
        # add a floorplan with above title 
        form_data = {'title': plan_title, 'plan': img_file}
        response = self.client.post(reverse('addplan'), form_data, follow=True)
        self.assertRegex(response.redirect_chain[0][0], r'/')    
        self.assertIsNotNone(Floorplan.objects.get(title=plan_title))
        
        # try to add another floorplan with same title
        form_data = {'title': plan_title, 'plan': img_file}
        response = self.client.post(reverse('addplan'), form_data, follow=True)
        self.assertContains(response, 'Floorplan with this Title already exists.')
        
        
        