from PIL import Image
import os

def convert_jpg_to_pdf(image_path, output_pdf):
    """Converts a single JPG image to a PDF"""
    img = Image.open(image_path)
    img.convert("RGB").save(output_pdf)
    print(f"Converted {image_path} to {output_pdf}")

def merge_jpgs_to_pdf(image_paths, output_pdf):
    """Merges multiple JPG images into a single PDF"""
    images = [Image.open(img).convert("RGB") for img in image_paths]

    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"Merged {len(image_paths)} images into {output_pdf}")

# Example Usage:
# Convert a single image
# convert_jpg_to_pdf("image1.jpg", "output.pdf")

# Merge multiple images into a PDF
merge_jpgs_to_pdf(["C:/Users/nites/OneDrive/Desktop/ukvisa/Sarla Jain Pan card/0.jpg"],
                   # "C:/Users/nites/OneDrive/Desktop/ukvisa/House Sale Deed/1.jpg",
                   # "C:/Users/nites/OneDrive/Desktop/ukvisa/House Sale Deed/2.jpg",
                   # "C:/Users/nites/OneDrive/Desktop/ukvisa/House Sale Deed/3.jpg"],
                  "C:/Users/nites/OneDrive/Desktop/ukvisa/All/SarlaJainPanCard.pdf")
