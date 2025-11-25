"""
Main application entry point for Image Steganography Tool
"""
from tkinterdnd2 import TkinterDnD
from gui import create_main_window

def main():
    """Initialize and start the steganography application"""
    root = TkinterDnD.Tk()
    create_main_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()