import os
from tkinter import filedialog, Tk, Button, Label, Entry, Frame, StringVar, messagebox, Radiobutton, Listbox, Scrollbar, ttk
from PIL import Image

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer and Renamer")

        # Set increased window size for better visibility
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.5)  # Set width to 50% of screen width
        window_height = int(screen_height * 0.6)  # Set height to 60% of screen height
        self.root.geometry(f"{window_width}x{window_height}")

        # Frame to hold all widgets with auto-sizing capability
        self.frame_main = Frame(root)
        self.frame_main.pack(fill="both", expand=True)

        self.selected_images = []
        self.scale = StringVar(value="2")
        self.width = StringVar()
        self.height = StringVar()
        self.resize_mode = StringVar(value="scale")
        self.rename_base = StringVar()

        # Import Button
        self.import_button = Button(self.frame_main, text="Import Images", command=self.import_images)
        self.import_button.pack(pady=10)

        # Listbox to display selected images
        self.image_listbox = Listbox(self.frame_main, height=10)
        self.image_listbox.pack(fill="both", padx=10, pady=5, expand=True)

        # Scrollbar for Listbox
        self.scrollbar = Scrollbar(self.image_listbox)
        self.scrollbar.pack(side="right", fill="y")

        # Progress bar for resizing and renaming
        self.progress = ttk.Progressbar(self.frame_main, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        # Resizing Options
        self.frame_options = Frame(self.frame_main)
        self.frame_options.pack(pady=10)

        Label(self.frame_options, text="Resize Type:").grid(row=0, column=0)
        Radiobutton(self.frame_options, text="Scale (x2, x4, x6)", variable=self.resize_mode, value="scale", command=self.toggle_mode).grid(row=0, column=1)
        Radiobutton(self.frame_options, text="Custom Size", variable=self.resize_mode, value="custom", command=self.toggle_mode).grid(row=0, column=2)

        # Scale input
        self.scale_label = Label(self.frame_main, text="Scale Factor (e.g., 2 for x2):")
        self.scale_label.pack()
        self.scale_entry = Entry(self.frame_main, textvariable=self.scale)
        self.scale_entry.pack(pady=5)

        # Custom size inputs
        self.width_label = Label(self.frame_main, text="Width:")
        self.width_entry = Entry(self.frame_main, textvariable=self.width)
        self.height_label = Label(self.frame_main, text="Height:")
        self.height_entry = Entry(self.frame_main, textvariable=self.height)

        # Resize Button
        self.resize_button = Button(self.frame_main, text="Resize Images", command=self.resize_images)
        self.resize_button.pack(pady=10)

        # Export Button
        self.export_button = Button(self.frame_main, text="Export Images", command=self.export_images)
        self.export_button.pack(pady=10)

        # Rename Options
        Label(self.frame_main, text="Rename Base (e.g., 'photo'):").pack(pady=5)
        self.rename_entry = Entry(self.frame_main, textvariable=self.rename_base)
        self.rename_entry.pack(pady=5)

        # Rename Button
        self.rename_button = Button(self.frame_main, text="Rename Images", command=self.rename_images)
        self.rename_button.pack(pady=10)

        # Make sure the window auto-sizes to fit the content
        self.root.pack_propagate(False)

    # Function to import images
    def import_images(self):
        self.selected_images = filedialog.askopenfilenames(
            title="Select Images", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        self.image_listbox.delete(0, 'end')  # Clear the listbox before adding new items
        if self.selected_images:
            for img in self.selected_images:
                self.image_listbox.insert('end', os.path.basename(img))  # Add each image to the listbox
            messagebox.showinfo("Info", f"Imported {len(self.selected_images)} image(s).")

    # Function to export resized images
    def export_images(self):
        if not self.selected_images:
            messagebox.showwarning("Warning", "No images to export. Please import images first.")
            return

        export_folder = filedialog.askdirectory(title="Select Export Folder")
        if not export_folder:
            return

        # Reset progress bar
        self.progress["value"] = 0
        total_images = len(self.selected_images)

        for i, image_path in enumerate(self.selected_images):
            try:
                with Image.open(image_path) as img:
                    # Resizing logic
                    resized_img = None
                    if self.resize_mode.get() == "scale":
                        scale = float(self.scale.get())
                        resized_img = self.resize_image_by_scale(img, scale)
                    else:
                        new_width = int(self.width.get())
                        new_height = int(self.height.get())
                        resized_img = self.resize_image_by_size(img, new_width, new_height)

                    # Construct new filename and save
                    base_name, ext = os.path.splitext(os.path.basename(image_path))
                    new_file_name = f"{base_name}_copy{ext}"
                    new_file_path = os.path.join(export_folder, new_file_name)
                    resized_img.save(new_file_path)
                    print(f"Saved resized image: {new_file_path}")

                # Update progress bar
                self.progress["value"] = ((i+1) / total_images) * 100
                self.root.update_idletasks()  # Refresh the UI

            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                messagebox.showerror("Error", f"Error processing {image_path}: {e}")

        messagebox.showinfo("Success", f"Exported {len(self.selected_images)} image(s) successfully!")

    # Function to resize the image by scaling factors (e.g., x2, x4, x6)
    def resize_image_by_scale(self, image, scale):
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Function to resize the image by custom width and height
    def resize_image_by_size(self, image, width, height):
        return image.resize((width, height), Image.Resampling.LANCZOS)

    # Function to resize images based on the user input
    def resize_images(self):
        if not self.selected_images:
            messagebox.showwarning("Warning", "Please import images before resizing.")
            return

        try:
            if self.resize_mode.get() == "scale":
                scale = float(self.scale.get())
                if scale <= 0:
                    raise ValueError("Scale factor must be greater than zero.")
            else:
                width = int(self.width.get())
                height = int(self.height.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Width and Height must be greater than zero.")

            messagebox.showinfo("Success", "Images resized successfully. You can now export them.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # Function to rename images based on user input
    def rename_images(self):
        if not self.selected_images:
            messagebox.showwarning("Warning", "No images to rename. Please import images first.")
            return

        if not self.rename_base.get():
            messagebox.showwarning("Warning", "Please enter a base name for renaming.")
            return

        rename_folder = filedialog.askdirectory(title="Select Folder for Renamed Images")
        if not rename_folder:
            return

        # Reset progress bar
        self.progress["value"] = 0
        total_images = len(self.selected_images)

        for i, image_path in enumerate(self.selected_images):
            try:
                base_name = self.rename_base.get()
                new_file_name = f"{base_name}-{i+1}{os.path.splitext(image_path)[1]}"
                new_file_path = os.path.join(rename_folder, new_file_name)

                # Copy the image with the new name
                os.rename(image_path, new_file_path)
                print(f"Renamed image to: {new_file_path}")

                # Update progress bar
                self.progress["value"] = ((i+1) / total_images) * 100
                self.root.update_idletasks()  # Refresh the UI

            except Exception as e:
                print(f"Error renaming {image_path}: {e}")
                messagebox.showerror("Error", f"Error renaming {image_path}: {e}")

        messagebox.showinfo("Success", f"Renamed {len(self.selected_images)} image(s) successfully!")

    # Toggle between scale and custom size mode
    def toggle_mode(self):
        if self.resize_mode.get() == "scale":
            self.show_scale_mode()
        else:
            self.show_custom_mode()

    # Display fields for scale mode
    def show_scale_mode(self):
        self.scale_label.pack()
        self.scale_entry.pack(pady=5)
        self.width_label.pack_forget()
        self.width_entry.pack_forget()
        self.height_label.pack_forget()
        self.height_entry.pack_forget()

    # Display fields for custom size mode
    def show_custom_mode(self):
        self.scale_label.pack_forget()
        self.scale_entry.pack_forget()
        self.width_label.pack()
        self.width_entry.pack(pady=5)
        self.height_label.pack()
        self.height_entry.pack(pady=5)

# Main application
if __name__ == "__main__":
    root = Tk()
    app = ImageResizerApp(root)
    root.mainloop()
