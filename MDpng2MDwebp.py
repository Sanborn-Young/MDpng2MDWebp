import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import re
import io

def decode_base64_to_image(encoded_string, image_format='PNG'):
    try:
        image_data = base64.b64decode(encoded_string)
        return Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise ValueError(f"Failed to decode image: {str(e)}")

def encode_image_to_base64(image, image_format='WEBP', quality=20):
    buffer = io.BytesIO()
    image.save(buffer, format=image_format, quality=quality)
    encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return encoded_string

def process_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = re.compile(r'!\[Image\]\(data:image/png;base64,([^)]*)\)')
        matches = pattern.findall(content)

        if not matches:
            messagebox.showinfo("Information", "No PNG base64 images found in the file.")
            return

        total_images = len(matches)
        processed_images = 0

        for match in matches:
            try:
                png_image = decode_base64_to_image(match, 'PNG')
                
                if png_image.format != 'PNG':
                    messagebox.showwarning("Warning", f"Skipping non-PNG image: {png_image.format}")
                    continue

                if png_image.width > 1080:
                    webp_image = png_image.resize((1080, int(1080 * png_image.height / png_image.width)))
                else:
                    webp_image = png_image

                webp_encoded_string = encode_image_to_base64(webp_image, 'WEBP', quality=20)
                content = content.replace(f'data:image/png;base64,{match}', f'data:image/webp;base64,{webp_encoded_string}')
                
                processed_images += 1
                root.title(f"Processing... {processed_images}/{total_images}")
                root.update()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process an image: {str(e)}")
                continue

        new_file_path = os.path.splitext(file_path)[0] + 'WP.md'
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        messagebox.showinfo("Success", f"File saved as {new_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if file_path:
        root.title("Processing...")
        root.update()
        process_markdown_file(file_path)
        root.title("Markdown Image Converter")

root = tk.Tk()
root.title("Markdown Image Converter")

open_button = tk.Button(root, text="Open Markdown File", command=open_file_dialog)
open_button.pack(pady=20)

root.mainloop()
