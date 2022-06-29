import os
import cv2


os.makedirs('scans', exist_ok=True)

for folder in (os.listdir('ppe')): # [train, test]
        for img_name in [i for i in os.listdir(f'ppe/{folder}') if i.endswith('.jpg')]:
            print()
            img_path = f'ppe/{folder1}/{folder2}/{img_name}'
            img_save_path = f'ppe_resized/{folder1}/{folder2}/{img_name}'
            image = cv2.imread(img_path)
            #resized = cv2.resize(image, resize_shape)
            cv2.imwrite(img_save_path, image)