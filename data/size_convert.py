import os
from PIL import Image

def resize_images_in_folder(folder_path, output_folder, size=(320, 320)):
   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'): 
            img_path = os.path.join(folder_path, filename)

            img = Image.open(img_path)

            img_resized = img.resize(size)

            resized_img_path = os.path.join(output_folder, filename)
            img_resized.save(resized_img_path)

            #print(f'Resized {filename} and saved to {output_folder}')

save_folder = '{input_folder_path}'
save_folder_320 = '{output_folder_path}'
resize_images_in_folder(save_folder, save_folder_320)