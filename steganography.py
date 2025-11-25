"""
Core steganography functions for encoding and decoding messages in images
"""
from PIL import Image
import numpy as np

def encode_message(input_path, message, output_path):
    """
    Encode a secret message into an image using LSB steganography
    
    Args:
        input_path (str): Path to source PNG image
        message (str): Secret message to hide
        output_path (str): Path to save encoded image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open and convert image to RGB mode
        image = Image.open(input_path)
        image = image.convert('RGB')
        
        # Convert image to numpy array for efficient processing
        img_array = np.array(image)
        height, width, channels = img_array.shape
        
        # Convert message to binary
        binary_message = string_to_binary(message)
        message_length = len(binary_message)
        
        # Check if message fits in image
        max_capacity = height * width * 3  # 3 channels per pixel
        if message_length > max_capacity:
            raise ValueError(f"Message too long. Maximum capacity: {max_capacity//8} characters")
        
        # Flatten the image array for easier processing
        flat_array = img_array.reshape(-1)
        
        # Encode message length in first 32 pixels (32 bits for length)
        length_binary = format(message_length, '032b')
        for i in range(32):
            if i < len(flat_array):
                flat_array[i] = (flat_array[i] & ~1) | int(length_binary[i])
        
        # Encode the actual message
        for i in range(message_length):
            pixel_index = 32 + i  # Start after length info
            if pixel_index < len(flat_array):
                flat_array[pixel_index] = (flat_array[pixel_index] & ~1) | int(binary_message[i])
        
        # Reshape back to original dimensions
        encoded_array = flat_array.reshape(height, width, channels)
        
        # Create new image and save
        encoded_image = Image.fromarray(encoded_array.astype('uint8'), 'RGB')
        encoded_image.save(output_path, 'PNG')
        
        return True
        
    except Exception as e:
        print(f"Encoding error: {e}")
        return False

def decode_message(image_path):
    """
    Decode a hidden message from an image
    
    Args:
        image_path (str): Path to encoded PNG image
    
    Returns:
        str: Decoded message or empty string if no message found
    """
    try:
        # Open image
        image = Image.open(image_path)
        image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image)
        flat_array = img_array.reshape(-1)
        
        # Extract message length from first 32 pixels
        length_binary = ''
        for i in range(32):
            if i < len(flat_array):
                length_binary += str(flat_array[i] & 1)
        
        message_length = int(length_binary, 2)
        
        # If length is 0 or unreasonable, assume no message
        if message_length == 0 or message_length > len(flat_array) - 32:
            return ""
        
        # Extract the message bits
        message_binary = ''
        for i in range(message_length):
            pixel_index = 32 + i
            if pixel_index < len(flat_array):
                message_binary += str(flat_array[pixel_index] & 1)
        
        # Convert binary to string
        decoded_message = binary_to_string(message_binary)
        
        return decoded_message
        
    except Exception as e:
        print(f"Decoding error: {e}")
        return ""

def string_to_binary(text):
    """
    Convert string to binary representation
    
    Args:
        text (str): Input text string
    
    Returns:
        str: Binary string representation
    """
    binary_string = ''
    for char in text:
        # Convert each character to 8-bit binary
        binary_char = format(ord(char), '08b')
        binary_string += binary_char
    return binary_string

def binary_to_string(binary_string):
    """
    Convert binary string back to text
    
    Args:
        binary_string (str): Binary string representation
    
    Returns:
        str: Original text string
    """
    text = ''
    # Process 8 bits at a time
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text