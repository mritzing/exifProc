import sys
import exifread
import os
import datetime
import csv
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog, QLineEdit, QFileDialog,QVBoxLayout,QPushButton,QHBoxLayout,QGridLayout, QTableWidget,QTableWidgetItem,QCheckBox
from PyQt5 import QtCore
#base pyqt5 tutorial available at https://build-system.fman.io/pyqt5-tutorial
#and http://zetcode.com/gui/pyqt5/

#https://pymotw.com/2/ConfigParser/

class exifExport(QWidget):
	def __init__(self):
		super().__init__()
		self.modelDict = {}
		self.initUI()
		
	# ============= layout ===============
	def initUI(self):
	
		grid = QGridLayout()
		grid.setSpacing(10)


		self.pushButtonDirectory = QPushButton('Input Directory', self)
		self.pushButtonDirectory.clicked.connect(self.choose_directory)
		self.lineEditDirectory = QLineEdit('',self)
	

		self.pushButtonModel = QPushButton('Select Model File', self)
		self.pushButtonModel.clicked.connect(self.choose_model)
		self.lineEditModel = QLineEdit('',self)


#		self.testButton = QPushButton('Test', self)
#		self.testButton.clicked.connect(self.test_funct)

		self.outputLabel = QLabel("Output File Name")
		self.fileExport = QLineEdit('',self)
		self.runButton = QPushButton('Run', self)
		self.runButton.clicked.connect(self.run_funct)


		self.renameCheck = QCheckBox('Rename With Datetime', self)


		self.tableModel = QTableWidget()
		self.tableModel.setColumnCount(3)

		grid.addWidget(self.pushButtonDirectory, 1, 0)
		grid.addWidget(self.lineEditDirectory, 1, 1)

		grid.addWidget(self.pushButtonModel, 2, 0)
		grid.addWidget(self.lineEditModel, 2, 1)

		grid.addWidget(self.tableModel, 3,0,2,0)

		grid.addWidget(self.renameCheck, 5, 0)
		grid.addWidget(self.outputLabel, 6, 0)
		grid.addWidget(self.fileExport, 6, 1)
		grid.addWidget(self.runButton, 6, 2)

		self.setLayout(grid)
		self.show()


	# ============= signals ===============
	def test_funct(self):
		checkedList = []
		for key in self.modelDict:
			if self.modelDict[key].checkState() == QtCore.Qt.Checked:
				checkedList.append(key)
		print(checkedList)

	def choose_model(self, file):
		modelFile = QFileDialog.getOpenFileName(self,"", "*.jpg")
		if Path(modelFile[0]).is_file():
			self.lineEditModel.setText(modelFile[0])
			f = open(modelFile[0], 'rb')
			tags = exifread.process_file(f)
			#clear current model
			self.tableModel.setRowCount(0);
			self.modelDict.clear()
			row = 0;
			for key in tags:
				#maker note adds a bunch of not useful fields, remove if statement to add back in
				if 'MakerNote' not in key:
					self.tableModel.insertRow(row)
					self.tableModel.setItem(row, 1,  QTableWidgetItem(str(key)))
					#display converted lat/long
					if key=='GPS GPSLatitude':
						latVal = self.convertLat(tags)
						self.tableModel.setItem(row, 2,  QTableWidgetItem(str(latVal)))
					elif key=='GPS GPSLongitude':
						longVal = self.convertLong(tags)
						self.tableModel.setItem(row, 2,  QTableWidgetItem(str(longVal)))
					else:
						self.tableModel.setItem(row, 2,  QTableWidgetItem(str(tags[key])))
					chkBoxItem = QTableWidgetItem()
					chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
					chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
					self.modelDict[key] = chkBoxItem
					self.tableModel.setItem(row, 0,  self.modelDict[key])
					row = row + 1
			self.tableModel.resizeColumnsToContents()
			#fill table with exif info 
			# check mark | key | value 
			# tuple  checkmarkbutton w/ key value


	def choose_directory(self):
		inputDirectory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if Path(inputDirectory).is_dir():
			self.lineEditDirectory.setText(inputDirectory)

	def run_funct(self):

		inputDir = self.lineEditDirectory.text()
		if not os.path.isdir(inputDir):
			print("Invalid Input Directory")
			return None
		rename = False
		exportName = ""
		#saves export as current datetime if none specificied
		if len(self.fileExport.text()) < 1:
			exportName = str(datetime.datetime.now())
			exportName = exportName.replace(":","_")
			exportName = exportName.replace(" ","_")
			exportName = exportName.replace("-","_")
			exportName = exportName.replace(".","_")
		else:
			exportName = self.fileExport.text().split(".")[0]

		exportName = exportName + ".csv"
		exportName = os.path.join(inputDir, exportName)
		if self.renameCheck == QtCore.Qt.Checked:
			rename = True
		#get model dictionary
		checkedList = []
		for key in self.modelDict:
			if self.modelDict[key].checkState() == QtCore.Qt.Checked:
				checkedList.append(key)
		
		

		csvList = []
		headers = checkedList
		csvList.append(["Filename"] + checkedList)
		for file in os.listdir(inputDir):
			current = os.path.join(inputDir, file)
			if os.path.isfile(current):
				if current.lower().endswith(".jpg"):
					f = open(current, 'rb')
					tags = exifread.process_file(f)
					f.close()
					#rename check
					testList = [current]
					if self.renameCheck.isChecked():
						fname = str(tags['EXIF DateTimeOriginal'])
						fname = str(fname).replace(":","_")
						fname = str(fname).replace(" ","_")
						fname = fname + ".JPG"
						try:
							os.rename(current,  os.path.join(inputDir,fname))
						except:
							print("Can't rename duplicate file exists")
						testList = [os.path.join(inputDir,fname)]
					for key in checkedList:
						if key=='GPS GPSLatitude':
							latVal = self.convertLat(tags)
							testList.append(latVal)
						elif key=='GPS GPSLongitude':
							longVal = self.convertLong(tags)
							testList.append(longVal)
						else:
							try:
								testList.append(str(tags[key]))
							except:
								testList.append("")
								print (Key + " not found")
					csvList.append(testList)
		with open(exportName, "w", newline='') as f:
			writer = csv.writer(f)
			writer.writerows(csvList)
		print("Succesfully exported info to " + exportName)

		



	# ============= helpers ===============
	#https://sno.phy.queensu.ca/~phil/exiftool/TagNames/GPS.html EXIF GPS Conversion info
	"""
	Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
	:param value:
	:type value: exifread.utils.Ratio
	:rtype: float
	"""
	def _convert_to_degress(self, value):

		d = float(value.values[0].num) / float(value.values[0].den)
		m = float(value.values[1].num) / float(value.values[1].den)
		s = float(value.values[2].num) / float(value.values[2].den)

		return d + (m / 60.0) + (s / 3600.0)

	def convertLat(self, tags):
		latitude = tags.get('GPS GPSLatitude')
		latitude_ref = tags.get('GPS GPSLatitudeRef')
		if latitude:
			lat_value = self._convert_to_degress(latitude)
			if latitude_ref.values != 'N':
				lat_value = -lat_value
		else:
			return {}
		return lat_value

	def convertLong(self, tags):
		longitude = tags.get('GPS GPSLongitude')
		longitude_ref = tags.get('GPS GPSLongitudeRef')
		if longitude:
			lon_value = self._convert_to_degress(longitude)
		if longitude_ref.values != 'E':
			lon_value = -lon_value
		else:
			return {}
		return lon_value




#======================== MAIN ================================
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = exifExport()
	sys.exit(app.exec_())