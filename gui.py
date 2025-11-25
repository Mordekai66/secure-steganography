"""
Tkinter GUI with Drag & Drop and Copy-Paste
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import ImageGrab, Image
from file_handlers import validate_png, get_image_info
from steganography import encode_message, decode_message

# Global state
current_image_path = None
image_label = None
message_text = None
status_label = None
root = None

def create_main_window(window):
    """Create the main application window"""
    global root
    root = window
    
    setup_window()
    main_frame = create_main_frame()
    create_gui_components(main_frame)
    setup_bindings()

def setup_window():
    """Configure window settings"""
    root.title("SecureSteg - Image Steganography")
    root.geometry("700x600")
    # root.resizable(False, False)

def create_main_frame():
    """Create and return main frame"""
    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    return main_frame

def create_gui_components(parent):
    """Create all GUI components"""
    create_header(parent)
    create_image_section(parent)
    create_message_section(parent)
    create_actions_section(parent)
    create_status_bar(parent)

def create_header(parent):
    """Create application header"""
    ttk.Label(parent, text="SecureSteg", font=('Arial', 16, 'bold')).pack(pady=(0, 5))
    ttk.Label(parent, text="Hide & Extract Secret Messages in PNG Images", font=('Arial', 10)).pack(pady=(0, 15))

def create_image_section(parent):
    """Create image upload section"""
    global image_label
    
    # Image frame
    frame = ttk.LabelFrame(parent, text="Image Upload", padding=10)
    frame.pack(fill=tk.X, pady=(0, 10))
    
    # Instructions
    ttk.Label(frame, text="• Drag & Drop PNG file\n• Paste with Ctrl+V\n• Click to Browse", justify=tk.LEFT).pack(anchor=tk.W)
    
    drop_frame = tk.Frame(frame, relief='sunken', bg='white', height=120)
    drop_frame.pack(fill=tk.X, pady=10)
    drop_frame.pack_propagate(False)
    
    try:
        root.drop_target_register('*')
        root.dnd_bind('<<Drop>>', lambda e: handle_drop(e, drop_frame))
    except Exception as e:
        print(f"Drag-drop setup warning: {e}")
    
    image_label = tk.Label(drop_frame, text="Drag PNG Here\nor Click to Browse\nor Paste (Ctrl+V)", bg='white', anchor=tk.CENTER, justify=tk.CENTER)
    image_label.pack(expand=True)
    
    # Bind click event
    image_label.bind('<Button-1>', lambda e: browse_image())
    drop_frame.bind('<Button-1>', lambda e: browse_image())
    
    # Buttons frame
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=(5, 0))
    
    # Browse button
    ttk.Button(btn_frame, text="Browse Image", command=browse_image).pack(side=tk.LEFT, padx=(0, 10))
    
    # Clear Image button
    ttk.Button(btn_frame, text="Clear Image", command=clear_image).pack(side=tk.LEFT)

def create_message_section(parent):
    """Create message input section"""
    global message_text
    
    frame = ttk.LabelFrame(parent, text="Secret Message", padding=10)
    frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    # Text area with scrollbar
    text_frame = ttk.Frame(frame)
    text_frame.pack(fill=tk.BOTH, expand=True)
    
    message_text = tk.Text(text_frame, height=6, wrap=tk.WORD, font=('Arial', 10))
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=message_text.yview)
    
    message_text.configure(yscrollcommand=scrollbar.set)
    message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def create_actions_section(parent):
    """Create action buttons"""
    frame = ttk.Frame(parent)
    frame.pack(pady=10)
    
    ttk.Button(frame, text="Encode Message", command=encode_action).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame, text="Decode Message", command=decode_action).pack(side=tk.LEFT, padx=5)

def create_status_bar(parent):
    """Create status bar"""
    global status_label
    status_label = ttk.Label(parent, text="Ready - Drag & Drop or Paste images", relief=tk.SUNKEN, font=('Arial', 8))
    status_label.pack(fill=tk.X, pady=(5, 0))

def setup_bindings():
    """Setup keyboard and clipboard bindings"""
    root.bind('<Control-v>', handle_paste)

def handle_drop(event, frame=None):
    """Handle dropped files"""
    try:
        files = root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')
            if validate_png(file_path):
                load_image_display(file_path)
                update_status(f"Loaded via drag & drop: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Error", "Please drop a valid PNG file")
    except Exception as e:
        messagebox.showerror("Error", f"Drop failed: {str(e)}")

def handle_paste(event=None):
    """Handle paste from clipboard using PIL"""
    try:
        clipboard_image = ImageGrab.grabclipboard()
        
        if clipboard_image:
            if clipboard_image.mode != 'RGB':
                clipboard_image = clipboard_image.convert('RGB')
            
            import tempfile
            temp_path = os.path.join(tempfile.gettempdir(), f"pasted_{os.getpid()}.png")
            clipboard_image.save(temp_path, 'PNG')
            
            if validate_png(temp_path):
                load_image_display(temp_path)
                update_status("Image pasted from clipboard")
                return
        
        try:
            clipboard_data = root.clipboard_get()
            if clipboard_data and '\n' not in clipboard_data:
                file_path = clipboard_data.strip()

                if file_path.startswith('file://'):
                    file_path = file_path[7:]
                
                if validate_png(file_path):
                    load_image_display(file_path)
                    update_status("Image loaded from clipboard path")
                    return
        except tk.TclError:
            pass
            
        messagebox.showinfo("Info", "No image found in clipboard")
        
    except Exception as e:
        messagebox.showerror("Error", f"Paste failed: {str(e)}")

def browse_image():
    """Browse for image file"""
    file_path = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if file_path and validate_png(file_path):
        load_image_display(file_path)
        update_status(f"Loaded: {os.path.basename(file_path)}")
    elif file_path:
        messagebox.showerror("Error", "Please select a valid PNG file")

def load_image_display(file_path):
    """Load image and update display"""
    global current_image_path
    current_image_path = file_path
    
    info = get_image_info(file_path)
    if info:
        text = f"✓ {os.path.basename(file_path)}\nSize: {info['width']}x{info['height']}\nReady for encode/decode"
    else:
        text = f"✓ {os.path.basename(file_path)}\nReady for encode/decode"
    
    image_label.config(text=text)

def clear_image():
    """Clear current image"""
    global current_image_path
    current_image_path = None
    image_label.config(text="Drag PNG Here\nor Click to Browse\nor Paste (Ctrl+V)")
    update_status("Image cleared")
    messagebox.showinfo("Cleared", "Image has been cleared successfully")

def encode_action():
    """Handle encode action"""
    if not current_image_path:
        messagebox.showerror("Error", "Please load an image first")
        return
    
    message = message_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to encode")
        return
    
    output_path = filedialog.asksaveasfilename(
        title="Save encoded image as...",
        initialfile=f"encoded_{os.path.basename(current_image_path)}",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    
    if output_path:
        try:
            if encode_message(current_image_path, message, output_path):
                messagebox.showinfo("Success", f"Message encoded successfully!\nSaved as: {os.path.basename(output_path)}")
                update_status("Message encoded successfully")
                message_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Failed to encode message")
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")

def decode_action():
    """Handle decode action"""
    if not current_image_path:
        messagebox.showerror("Error", "Please load an image first")
        return
    
    try:
        decoded_message = decode_message(current_image_path)
        if decoded_message:
            message_text.delete("1.0", tk.END)
            message_text.insert("1.0", decoded_message)
            update_status("Message decoded successfully")
        else:
            messagebox.showinfo("No Message", "No hidden message found in the image")
    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {str(e)}")

def update_status(message):
    """Update status bar"""
    if status_label:
        status_label.config(text=message)