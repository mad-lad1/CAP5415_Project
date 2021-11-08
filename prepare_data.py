import os
import cv2

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = cv2.imread(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
    return images
cities = ['aachen', 'bochum', 'bremen', 'cologne', 'darmstadt', 'dusseldorf', 'erfurt', 'hamburg', 
          'hanover', 'jena', 'krefeld', 'monchengladbach', 'strasbourg', 'stuttgart', 'tubingen', 'ulm',
          'weimar', 'zurich']
root_folder = '../dataset/leftImg8bit/train/'
folders = [os.path.join(root_folder, x) for x in cities]
all_images = [img for folder in folders for img in load_images_from_folder(folder)]
print(len(all_images))