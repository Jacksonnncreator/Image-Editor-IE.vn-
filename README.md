# 📸 Beginner's Guide: Building Your First Desktop Photo Editor in Python

Welcome to Python GUI development! In this tutorial, we will break down a complete desktop application built with **PyQt5** (for the graphical interface) and **Pillow / PIL** (for image processing).

---

## 📋 Overview

This application allows users to:
1. Select a folder on their computer.
2. View a list of supported image files (`.jpg`, `.png`, `.jpeg`, `.gif`).
3. Display selected images on screen.
4. Apply various image transformations:
   - **Rotate** (Left / Right)
   - **Flip** (Horizontal Mirror)
   - **Sharpen**
   - **Black & White** (Grayscale conversion)
5. Automatically save modified images inside a dedicated `Modified` folder.

---

## 🛠️ Prerequisites & Setup

Before running the code, install the required third-party libraries using `pip`:

```bash
pip install PyQt5 Pillow
```

---

## 🧩 Step-by-Step Code Walkthrough

---

### Step 1: Initialize Application & Window

Every PyQt application requires a `QApplication` instance to manage the application's control flow and main settings.

```python
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])

win = QWidget()
win.resize(700, 500)
win.setWindowTitle("IE.vn 🙂‍↔️")
```

---

### Step 2: Create UI Widgets

Widgets are the building blocks of a user interface (buttons, text labels, lists).

```python
from PyQt5.QtWidgets import QLabel, QPushButton, QListWidget
from PyQt5.QtCore import Qt

# Image display display area
lb_image = QLabel("Image")
lb_image.setAlignment(Qt.AlignCenter)

# Folder selector button and image file list
btn_dir = QPushButton("__FOLDER__")
lw_files = QListWidget()

# Image editing buttons
btn_left = QPushButton("Turn left")
btn_right = QPushButton("Turn right")
btn_mirror = QPushButton("Mirror")
btn_sharpen = QPushButton("Sharpness V")
btn_bw = QPushButton("B/W")
```

---

### Step 3: Layout Management

PyQt uses **Layouts** to organize widgets in rows and columns so they resize nicely.

```python
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

row = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

# Left Column: Folder button and file list
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

# Right Column: Image display and tool buttons
col2.addWidget(lb_image)

row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharpen)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)

# Assemble layout proportions (20% left sidebar, 80% main area)
row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)
```

---

### Step 4 & 5: File Filtering and Directory Selection

Functions handle reading directory contents and filtering supported image extensions.

```python
import os
from PyQt5.QtWidgets import QFileDialog

def filter_files(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.lower().endswith(ext):
                result.append(filename)
                break
    return result

workdir = ""

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def ShowFilenamelist():
    extensions = [".jpg", ".png", ".jpeg", ".gif"]
    chooseWorkdir()

    if not workdir:
        return

    filenames = filter_files(os.listdir(workdir), extensions)

    lw_files.clear()
    lb_image.clear()
    workimage.image = None

    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(ShowFilenamelist)
```

---

### Step 6: Custom Styling (QSS)

Qt Style Sheets (QSS) let you style desktop components using syntax similar to web CSS.

```python
win.setStyleSheet("""
    QWidget {
        background-color: #00FF80;
        font-family: Arial;
        font-size: 20px;
    }

    QPushButton {
        background-color: #2C5842;
        font-size: 22px;
        color: white;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #A1FFD0;
        color: black;
    }
""")
```

---

### Step 7: The Core Image Processor Class

This Object-Oriented Programming (OOP) class handles reading, editing, saving, and rendering images using PIL (Pillow) and PyQt's `QPixmap`.

```python
from PIL import Image
from PIL.ImageFilter import SHARPEN
from PyQt5.QtGui import QPixmap

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified"

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        with Image.open(fullname) as img:
            self.image = img.copy()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        os.makedirs(path, exist_ok=True)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def showImage(self, path):
        lb_image.hide()
        pixmapImage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapImage = pixmapImage.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lb_image.setPixmap(pixmapImage)
        lb_image.show()

    # Image Operations
    def do_left(self):
        if self.image is None: return
        self.image = self.image.transpose(Image.Transpose.ROTATE_90)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_right(self):
        if self.image is None: return
        self.image = self.image.transpose(Image.Transpose.ROTATE_270)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_flip(self):
        if self.image is None: return
        self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_bw(self):
        if self.image is None: return
        self.image = self.image.convert("L")
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_sharpen(self):
        if self.image is None: return
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))
```

---

### Step 8–11: Object Creation, Event Connections & Event Loop

Finally, instantiate the processor, connect events (clicks and selection changes), and launch the application loop.

```python
# Instantiate image processor
workimage = ImageProcessor()

# Event: User selects a file from the list
def ShowchoosenImage():
    if lw_files.currentItem() is None:
        return
    filename = lw_files.currentItem().text()
    workimage.loadImage(filename)
    workimage.showImage(os.path.join(workdir, filename))

# Signal & Slot Connections
lw_files.currentRowChanged.connect(ShowchoosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_right.clicked.connect(workimage.do_right)
btn_left.clicked.connect(workimage.do_left)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharpen.clicked.connect(workimage.do_sharpen)

# Display main window and launch loop
win.show()
app.exec()
```

---

## 💡 Key Programming Concepts Demonstrated

1. **GUI Event Loop:** `app.exec()` keeps the application running and listening for user actions.
2. **Signals & Slots:** Connecting UI actions like `btn_bw.clicked` to backend logic methods like `workimage.do_bw`.
3. **Encapsulation:** Grouping image attributes and operations cleanly inside the `ImageProcessor` class.
4. **File I/O & Path Operations:** Safe cross-platform path handling using `os.path.join()`.