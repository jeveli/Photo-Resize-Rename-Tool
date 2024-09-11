
# Photo Resizer and Renamer

**Photo Resizer and Renamer** is a simple and efficient tool that allows users to resize and rename multiple photos in bulk. The program features a graphical user interface (GUI) built with `tkinter` and is packaged as an executable, so it can be used without the need for Python or external dependencies.

## Features

- **Batch Resizing**: Resize multiple images at once by scale (e.g., 2x, 4x) or by specifying custom width and height.
- **Bulk Renaming**: Rename a set of images sequentially with a specified base name (e.g., `photo-1.jpg`, `photo-2.jpg`, etc.).
- **User-Friendly GUI**: Easy-to-use interface for selecting images, setting options, and exporting resized and renamed photos.
- **No Python Required**: Compiled as a standalone executable, the program runs without needing Python installed on the user’s system.

## How to Use

1. **Open the Program**: Download and run the (`Install Resize & Rename Tool.exe`).
2. **Import Photos**: Click the **Import Images** button to select the photos you want to resize or rename.
3. **Resize Photos**:
   - Choose whether to resize by scale or by custom size.
   - For **scale**, enter a factor (e.g., `2` for 2x).
   - For **custom size**, specify the desired width and height.
   - Click **Resize Images** to apply the changes.
4. **Rename Photos**:
   - Enter a base name (e.g., `photo`) in the renaming field.
   - Click **Rename Images** to rename the photos sequentially.
5. **Export**: Save the resized and/or renamed photos to the desired directory.

## Installation

- The program is distributed as an executable file and does not require Python or any external dependencies.
- Simply download the latest release from the [Releases](https://github.com/your-username/photo-resizer/releases) section and run the installer.

## Compiling from Source

To compile the program from source, you need:
- Python 3.x
- Required Python packages: `Pillow`, `tkinter`

Run the following command to install the dependencies:

```bash
pip install Pillow
```

You can compile the script to an executable using `PyInstaller`:

```bash
pyinstaller --onefile --windowed "photo_resize.py"
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter bugs or have feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/your-username/photo-resizer/blob/master/LICENSE) file for details.
