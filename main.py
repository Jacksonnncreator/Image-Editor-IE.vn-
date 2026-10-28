
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QLabel,
    QPushButton, QListWidget, QVBoxLayout, QHBoxLayout
)
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL.ImageFilter import SHARPEN


# Step 1: Create app and window
app = QApplication([])

win = QWidget()
win.resize(700, 500)
win.setWindowTitle("IE.vn 🙂‍↔️")


# Step 2: Create Widgets (UI)
lb_image = QLabel("Image")
lb_image.setAlignment(Qt.AlignCenter)

btn_dir = QPushButton("__FOLDER__")
lw_files = QListWidget()

btn_left = QPushButton("Turn left")
btn_right = QPushButton("Turn right")
btn_mirror = QPushButton("Mirror")
btn_sharpen = QPushButton("Sharpness V")
btn_bw = QPushButton("B/W")


# Step 3: Align layouts
row = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2.addWidget(lb_image)

row_tools = QHBoxLayout()

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharpen)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)


# Step 4: Filter files
def filter_files(files, extensions):
    result = []

    for filename in files:
        for ext in extensions:
            if filename.lower().endswith(ext):
                result.append(filename)
                break

    return result


# Step 5: Choose folder
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


# Step 6: Style
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


# Step 7: Image Processor
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

    def do_left(self):
        if self.image is None:
            return

        self.image = self.image.transpose(
            Image.Transpose.ROTATE_90
        )

        self.saveImage()

        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )

        self.showImage(image_path)

    def do_right(self):
        if self.image is None:
            return

        self.image = self.image.transpose(
            Image.Transpose.ROTATE_270
        )

        self.saveImage()

        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )

        self.showImage(image_path)

    def do_flip(self):
        if self.image is None:
            return

        self.image = self.image.transpose(
            Image.Transpose.FLIP_LEFT_RIGHT
        )

        self.saveImage()

        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )

        self.showImage(image_path)

    def do_bw(self):
        if self.image is None:
            return

        self.image = self.image.convert("L")

        self.saveImage()

        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )

        self.showImage(image_path)

    def do_sharpen(self):
        if self.image is None:
            return

        self.image = self.image.filter(SHARPEN)

        self.saveImage()

        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )

        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()

        pixmapImage = QPixmap(path)

        w = lb_image.width()
        h = lb_image.height()

        pixmapImage = pixmapImage.scaled(
            w,
            h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        lb_image.setPixmap(pixmapImage)
        lb_image.show()


# Step 8: Create object
workimage = ImageProcessor()


# Step 9: Select image
def ShowchoosenImage():
    if lw_files.currentItem() is None:
        return

    filename = lw_files.currentItem().text()

    workimage.loadImage(filename)

    workimage.showImage(
        os.path.join(workdir, filename)
    )


# Step 10: Connect buttons
lw_files.currentRowChanged.connect(ShowchoosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_right.clicked.connect(workimage.do_right)
btn_left.clicked.connect(workimage.do_left)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharpen.clicked.connect(workimage.do_sharpen)


# Step 11: Run application
win.show()
app.exec()
