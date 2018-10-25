from cx_Freeze import setup, Executable
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog, QLineEdit, QFileDialog,QVBoxLayout,QPushButton,QHBoxLayout,QGridLayout, QTableWidget,QTableWidgetItem,QCheckBox
from PyQt5 import QtCore

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["PyQt5.QtCore","PyQt5.QtWidgets"])
import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('exifProc.py', base=base)
]

setup(
    name='ExifProc',
    version = '0.1',
    description = 'Pull Exif Data, Rename Files',
    options = dict(build_exe = buildOptions),
    executables = executables
)