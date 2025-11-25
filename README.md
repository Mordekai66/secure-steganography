# SecureSteg - Image Steganography Tool

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

A professional, user-friendly desktop application for hiding and extracting secret messages within PNG images using advanced LSB (Least Significant Bit) steganography techniques.

## 🎯 Project Overview

SecureSteg is a powerful yet simple tool that allows you to securely conceal text messages inside PNG images without visible detection. The hidden messages remain completely invisible to the naked eye while being easily retrievable by authorized users.

## ✨ Features

- **🔒 Secure Encoding**: Hide messages using LSB steganography
- **🔍 Easy Decoding**: Extract hidden messages with one click
- **🎨 Multiple Input Methods**:
  - Drag & Drop support
  - Copy & Paste functionality
  - File browser integration
- **📁 PNG Exclusive**: Optimized for PNG format (lossless compression)
- **💻 Modern GUI**: Professional Tkinter-based interface
- **🚀 High Performance**: Efficient numpy-based processing

## 🛠️ Installation

### Prerequisites
- Python 3.12.0 or higher

### Dependencies Installation
```bash
pip install Pillow numpy tkinterdnd2
````

### Running the Application

```bash
python main.py
```

## 📁 Project Structure

```text
secure-steganography/
├── main.py              # Application entry point
├── gui.py               # Tkinter GUI implementation
├── steganography.py     # Core encoding/decoding logic
├── file_handlers.py     # File input/output operations
└── utils.py             # Utility functions and constants
```

## 🔧 How It Works

### Encoding Process

1. Image Preparation: Convert PNG image to RGB mode and numpy array
2. Message Conversion: Transform text message into binary format
3. Capacity Check: Verify message fits within image capacity
4. Length Storage: Encode message length in first 32 pixels (32 bits)
5. Message Embedding: Hide message bits in LSBs of subsequent pixels
6. Image Reconstruction: Save modified image with hidden message

### Decoding Process

1. Image Analysis: Load and convert encoded image to numpy array
2. Length Extraction: Read message length from first 32 pixels
3. Message Recovery: Extract hidden bits from LSBs
4. Binary Conversion: Transform binary back to readable text

## 🧠 Technical Implementation

```python
# Core encoding operation
flat_array[i] = (flat_array[i] & ~1) | int(binary_message[i])

# Core decoding operation  
message_bit = flat_array[i] & 1
```

## 🚀 Usage Guide

### Hiding a Message

1. Load Image: Drag & drop, paste, or browse for a PNG file
2. Enter Message: Type your secret message in the text area
3. Encode: Click "Encode Message" and choose save location
4. Share: Distribute the encoded image - it looks identical!

### Extracting a Message

1. Load Encoded Image: Use any input method to load the image
2. Decode: Click "Decode Message"
3. View: The hidden message appears in the text area

## 💡 Technical Details

### LSB Steganography Method

* Modifies only the least significant bit of each color channel
* Changes are visually imperceptible (±1 value change)
* Uses 32-bit header to store message length
* Supports messages up to 4.2 billion characters

### Capacity Calculation

```python
max_capacity = (width * height * 3 - 32) // 8  # characters
```

## 🔐 Security Features

* No visible image alteration
* Message length obfuscation
* Random distribution across image pixels
* Preservation of original image quality

## 📊 Performance

* Processing Speed: ~1-5 seconds for typical images
* Image Quality: No visible degradation
* Message Capacity: Depends on image dimensions
* Format Support: PNG only (lossless preservation)

## 🔍 Example Use Cases

* Confidential Communication
* Digital Watermarking
* Data Hiding
* Educational Tool
* Security Research


## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
