"""
File handling utilities for image operations
"""
import os
from PIL import Image

def validate_png(file_path):
    """
    Validate if file is a valid PNG image
    
    Args:
        file_path (str): Path to file to validate
    
    Returns:
        bool: True if valid PNG, False otherwise
    """
    try:
        # Check file extension
        if not file_path.lower().endswith('.png'):
            return False
        
        # Check if file exists and is readable
        if not os.path.isfile(file_path):
            return False
        
        # Try to open as image to verify it's a valid PNG
        with Image.open(file_path) as img:
            return img.format == 'PNG'
            
    except Exception:
        return False

def load_image(file_path):
    """
    Load image from file path
    
    Args:
        file_path (str): Path to image file
    
    Returns:
        PIL.Image.Image: Loaded image object or None if failed
    """
    try:
        image = Image.open(file_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def save_image(image, file_path):
    """
    Save image to file path
    
    Args:
        image (PIL.Image.Image): Image to save
        file_path (str): Destination file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        image.save(file_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def get_image_info(file_path):
    """
    Get basic information about an image
    
    Args:
        file_path (str): Path to image file
    
    Returns:
        dict: Image information or None if failed
    """
    try:
        with Image.open(file_path) as img:
            return {
                'format': img.format,
                'size': img.size,
                'mode': img.mode,
                'width': img.width,
                'height': img.height
            }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None