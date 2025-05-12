from PIL import Image
import os

def process_image(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Convert image to RGBA if it isn't already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get the alpha data
        data = img.getdata()
        
        # Create a new image with transparent background
        new_data = []
        for item in data:
            # If pixel is white or near white, make it transparent
            if item[0] > 250 and item[1] > 250 and item[2] > 250:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        # Create new image with transparent background
        img.putdata(new_data)
        
        # Get the bounding box of non-transparent pixels
        bbox = img.getbbox()
        
        if bbox:
            # Crop to content
            img = img.crop(bbox)
            
            # Save back to JPG with white background
            # Create a white background layer
            background = Image.new('RGB', img.size, (255, 255, 255))
            # Paste the image on the white background using alpha channel
            background.paste(img, (0, 0), img)
            
            # Save with high quality
            background.save(image_path, 'JPEG', quality=95)
            print(f"Processed: {image_path}")

def main():
    # Path to the rugs folder
    rugs_folder = r"C:\Users\islam\Documents\OW\screens\rugs"
    
    # Process all jpg files in the folder
    for filename in os.listdir(rugs_folder):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(rugs_folder, filename)
            try:
                process_image(image_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()