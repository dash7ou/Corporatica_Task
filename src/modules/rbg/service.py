import os
from PIL import Image, ImageOps
import numpy as np
# import matplotlib.pyplot as plt
import cv2

class ImageService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def get_image_path(self, filename):
        return os.path.join(self.upload_folder, filename)

    def generate_histogram(self, filename):
        image_path = self.get_image_path(filename)
        if not os.path.exists(image_path):
            return {'error': 'Image not found'}

        image = Image.open(image_path)
        histogram = image.histogram()

        # Convert to RGB format
        r, g, b = histogram[0:256], histogram[256:512], histogram[512:768]
        
        # Example to return histogram (as lists)
        return {
            'red': r,
            'green': g,
            'blue': b
        }

    def generate_segmentation_mask(self, filename, params):
        image_path = self.get_image_path(filename)
        if not os.path.exists(image_path):
            return {'error': 'Image not found'}

        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Example segmentation using thresholding
        _, mask = cv2.threshold(gray, params.get('threshold', 128), 255, cv2.THRESH_BINARY)

        # Save the mask as an image (optional)
        mask_filename = f'mask_{filename}'
        mask_path = os.path.join(self.upload_folder, mask_filename)
        cv2.imwrite(mask_path, mask)

        return {'segmentation_mask': "/static/rgb_image/" + mask_filename}

    def manipulate_image(self, filename, manipulation_params):
        image_path = self.get_image_path(filename)
        if not os.path.exists(image_path):
            return {'error': 'Image not found'}

        image = Image.open(image_path)
        action = manipulation_params.get('action')

        if action == 'resize':
            width = manipulation_params.get('width', image.width)
            height = manipulation_params.get('height', image.height)
            image = image.resize((width, height))
        elif action == 'crop':
            left = manipulation_params.get('left', 0)
            top = manipulation_params.get('top', 0)
            right = manipulation_params.get('right', image.width)
            bottom = manipulation_params.get('bottom', image.height)
            image = image.crop((left, top, right, bottom))
        elif action == 'convert':
            format = manipulation_params.get('format', 'JPEG')
            converted_filename = f'{filename.split(".")[0]}.{format.lower()}'
            image.save(os.path.join(self.upload_folder, converted_filename), format)
            return {'converted_image': "/static/rgb_image/" + converted_filename}
        else:
            return {'error': 'Invalid action'}

        manipulated_filename = f'manipulated_{filename}'
        image.save(os.path.join(self.upload_folder, manipulated_filename))
        return {'manipulated_image': "/static/rgb_image/" + manipulated_filename}
