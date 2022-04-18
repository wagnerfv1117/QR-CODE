import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qrcode import QRCode, ERROR_CORRECT_H
from PIL import Image

class Qr_qt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WF SAGEN - Generador de códigos QR")
        self.setWindowIcon(QIcon('10.jpg'))

        self.lab1 = QLabel('Introduzca el contenido del código QR')

        self.text1 = QLineEdit('Digite el texto deseado', self)
        self.text1.selectAll()

        self.bt1 = QPushButton('Seleccionar imagen que irá en el centro', self)
        self.bt1.setToolTip("<b> Haga clic en el botón para seleccionar la imagen central que desee insertar </b>")
        self.bt1.clicked.connect(self.chooseImage)

        self.bt2 = QPushButton('generar QR', self)
        self.bt2.setToolTip("<b> Haga clic en el botón para generar el código QR </b>")
        self.bt2.clicked.connect(self.createQr)


        grid = QGridLayout()
        grid.addWidget(self.lab1, 0, 0)
        grid.addWidget(self.text1, 0, 1)
        grid.addWidget(self.bt1, 1, 0)
        grid.addWidget(self.bt2, 1, 1)
        self.setLayout(grid)

        self.show()

    def chooseImage(self):
        self.fname, jud = QFileDialog.getOpenFileName(self, 'abrir un archivo', './', "Image Files (*.jpg *.png)")

    def createQr(self):
        qr = QRCode(version = 1, error_correction = ERROR_CORRECT_H, border = 2)

        qr.add_data(self.text1.text())
        qr.make(fit = True)

        img = qr.make_image()
        img = img.convert("RGB")

        try:
            logo = Image.open(self.fname)

            w, h = img.size
            logo_w = int(w/4)
            logo_h = int(h/4)

            rel_w = int((w-logo_w)/2)
            rel_h = int((h-logo_h)/2)
            logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
            logo = logo.convert("RGBA")
            img.paste(logo, (rel_w, rel_h), logo)
            finame, jud = QFileDialog.getSaveFileName(self, 'guardar codigo QR', './', "Image Files (*.jpg *.png)")
            if jud and img:
                img.save(finame)

        except:
            QMessageBox.about(self, 'Error', 'No Such a File')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    qr = Qr_qt()
    sys.exit(app.exec_())

