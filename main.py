import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QPushButton, QLineEdit, QFontDialog,
    QFileDialog, QTextEdit, QAction, QMessageBox
)
from PyQt5.QtCore import pyqtSignal


class InputNameWindow(QWidget):
    nameEntered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Nama")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("Masukkan Nama:"))
        layout.addWidget(self.name_edit)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.send_name)
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def send_name(self):
        self.nameEntered.emit(self.name_edit.text())
        self.close()


class TabApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTab Application + Action Bar")
        self.resize(500, 300)

        self.nama = ""
        self.tabs = QTabWidget()

        self.tabs.addTab(self.tab_input_nama_ui(), "Input Nama")
        self.tabs.addTab(self.tab_set_font_ui(), "Set Font")
        self.tabs.addTab(self.tab_buka_file_ui(), "Buka File")

        # Widget utama (central)
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Tambahkan ActionBar / MenuBar
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Fitur Menu
        fitur_menu = menubar.addMenu("Fitur")
        input_nama_action = QAction("Input Nama", self)
        input_nama_action.triggered.connect(self.show_input_nama_tab)
        set_font_action = QAction("Set Font", self)
        set_font_action.triggered.connect(self.show_set_font_tab)
        buka_file_action = QAction("Buka File", self)
        buka_file_action.triggered.connect(self.show_buka_file_tab)

        fitur_menu.addAction(input_nama_action)
        fitur_menu.addAction(set_font_action)
        fitur_menu.addAction(buka_file_action)

    def tab_input_nama_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.btn_input_nama = QPushButton("Input Nama")
        self.btn_input_nama.clicked.connect(self.open_input_window)

        self.label_nama_kiri = QLabel("Nama:")
        self.label_nama_kanan = QLabel("")

        name_layout = QFormLayout()
        name_layout.addRow(self.label_nama_kiri, self.label_nama_kanan)

        layout.addWidget(self.btn_input_nama)
        layout.addLayout(name_layout)
        tab.setLayout(layout)
        return tab

    def tab_set_font_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.label_nama_font_kiri = QLabel("Nama:")
        self.label_nama_font_kanan = QLabel("")

        name_layout = QFormLayout()
        name_layout.addRow(self.label_nama_font_kiri, self.label_nama_font_kanan)

        btn_font = QPushButton("Pilih Font")
        btn_font.clicked.connect(self.change_font)

        layout.addLayout(name_layout)
        layout.addWidget(btn_font)
        tab.setLayout(layout)
        return tab

    def tab_buka_file_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.file_content = QTextEdit()
        self.file_content.setReadOnly(True)

        btn_open_file = QPushButton("Buka File .txt")
        btn_open_file.clicked.connect(self.open_file)

        layout.addWidget(btn_open_file)
        layout.addWidget(self.file_content)
        tab.setLayout(layout)
        return tab

    def open_input_window(self):
        self.input_window = InputNameWindow()
        self.input_window.nameEntered.connect(self.set_nama)
        self.input_window.show()

    def set_nama(self, name):
        self.nama = name
        self.label_nama_kanan.setText(name)
        self.label_nama_font_kanan.setText(name)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.label_nama_font_kiri.setFont(font)
            self.label_nama_font_kanan.setFont(font)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Buka File Teks", "", "Text Files (*.txt)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as file:
                self.file_content.setText(file.read())

    def show_input_nama_tab(self):
        self.tabs.setCurrentIndex(0)

    def show_set_font_tab(self):
        self.tabs.setCurrentIndex(1)

    def show_buka_file_tab(self):
        self.tabs.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabApp()
    window.show()
    sys.exit(app.exec_())
