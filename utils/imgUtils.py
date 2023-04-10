#!/usr/bin/python3
import utils.constant as ct
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

class imgUtils:
    def __init__(self, base_path, file_name_list, gray_threshold, signature_color):
        self.file_name_list = file_name_list
        self.absolute_path = os.path.abspath(base_path)
        self.gray_threshold = gray_threshold
        self.signature_color = signature_color

    def process(self):
        for i in range(len(self.file_name_list)):
            self.image_name = self.file_name_list[i]
            self.image_name_without_extenstion = os.path.splitext(self.image_name)[0]
            path_to_image = self.absolute_path + '/' + self.image_name
            img = cv2.imread(path_to_image)
            img = self.denoise(img)
            img = self.grayscale(img)
            self.getImageInfo(img)
            img = self.binarize(img, self.gray_threshold)
            img = self.denoise(img)
            img = self.toGIF(img)
            path_to_gif = self.absolute_path + '/' + self.image_name_without_extenstion + '.gif'
            img.save(path_to_gif, 'gif')
            print("GIF is save to: ", path_to_gif)

    def toGIF(self, bin_img):
        indices = np.where(bin_img == 0)
        # Convert the indices to pixel coordinates
        black_pixel_coords = np.transpose(indices)
        black_pixel_coords = np.fliplr(black_pixel_coords)
        # Create a new image with a transparent background
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Fill in the pixels with black color
        for coord in black_pixel_coords:
            draw.point(coord, fill=self.signature_color)
        return img     

    def denoise(self, img):
        return cv2.bilateralFilter(img, 10, 75, 75)
            
    def grayscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def binarize(self, img, threshold):
        ret, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return binary_img

    def getImageInfo(self, img):
        self.average_gray = cv2.mean(img)[0]
        self.height, self.width = img.shape[:2]

    def view(self, img):
        cv2.imshow('Input Image', img)
        cv2.waitKey(2000)

