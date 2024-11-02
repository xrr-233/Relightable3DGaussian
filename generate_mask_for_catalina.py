import os
import cv2
from PIL import Image
from tqdm import tqdm

dataset_path = "data/municipal-r3dg"
image_dir = os.path.join(dataset_path, 'images')
all_imgs = os.listdir(image_dir)

img = Image.open(os.path.join(image_dir, all_imgs[0]))
W = img.width
H = img.height
print(W, H)

def generate_mask():
    os.makedirs(os.path.join(dataset_path, 'masks'), exist_ok=True)
    mask_dir = os.path.join(dataset_path, 'masks')
    for img_name in all_imgs:
        img = Image.new('L', (W, H), 255)
        img.save(os.path.join(mask_dir, img_name))

def crop_and_resize(aspect_ratio_width, aspect_ratio_height):
    os.makedirs(os.path.join(dataset_path, 'resized_images'), exist_ok=True)
    resized_dir = os.path.join(dataset_path, 'resized_images')
    for img_name in tqdm(all_imgs):
        image = Image.open(os.path.join(image_dir, img_name))
        target_aspect_ratio = aspect_ratio_width / aspect_ratio_height
        current_aspect_ratio = W / H

        # Determine dimensions for cropping
        if current_aspect_ratio > target_aspect_ratio:
            # Current image is wider than target ratio, adjust width
            new_width = int(target_aspect_ratio * H)
            new_height = H
        else:
            # Current image is taller than target ratio, adjust height
            new_width = W
            new_height = int(W / target_aspect_ratio)

        # Calculate coordinates for cropping to keep the crop in center
        left = (W - new_width) / 2
        top = (H - new_height) / 2
        right = (W + new_width) / 2
        bottom = (H + new_height) / 2

        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))
        resized_image = cropped_image.resize((aspect_ratio_width, aspect_ratio_height))

        # Save the cropped image
        resized_image.save(os.path.join(resized_dir, img_name))


def convert2jpg():
    os.makedirs(os.path.join(dataset_path, 'images_rgb'), exist_ok=True)
    resized_dir = os.path.join(dataset_path, 'images_rgb')
    for img_name in all_imgs:
        img = cv2.imread(os.path.join(image_dir, img_name), 1)  # 1是以彩色图方式去读
        jpg_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(os.path.join(resized_dir, img_name), jpg_img)

if __name__ == '__main__':
    crop_and_resize(1600, 1200)
    # generate_mask()
    # convert2jpg()