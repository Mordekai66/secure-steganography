"""
Utility functions and constants for the steganography application
"""

# Application constants
APP_NAME = "SecureSteg"
APP_VERSION = "1.0"
SUPPORTED_FORMATS = ['.png']
MAX_MESSAGE_LENGTH = 10000  # Maximum characters that can be encoded

def calculate_capacity(image_width, image_height):
    """
    Calculate maximum message capacity for an image
    
    Args:
        image_width (int): Image width in pixels
        image_height (int): Image height in pixels
    
    Returns:
        dict: Capacity information
    """
    total_pixels = image_width * image_height
    total_bits = total_pixels * 3  # 3 channels per pixel
    available_bits = total_bits - 32  # Reserve 32 bits for length info
    
    max_chars = available_bits // 8
    
    return {
        'max_bits': available_bits,
        'max_chars': max_chars,
        'pixels_used': total_pixels
    }

def format_file_size(bytes_size):
    """
    Format file size in human-readable format
    
    Args:
        bytes_size (int): Size in bytes
    
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def sanitize_filename(filename):
    """
    Sanitize filename to remove potentially dangerous characters
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    sanitized = filename
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')
    return sanitized

def validate_message_length(message, max_capacity):
    """
    Validate if message fits within image capacity
    
    Args:
        message (str): Message to validate
        max_capacity (int): Maximum allowed characters
    
    Returns:
        tuple: (is_valid, message_length, max_capacity)
    """
    message_length = len(message)
    is_valid = message_length <= max_capacity
    
    return is_valid, message_length, max_capacity