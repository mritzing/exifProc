# exifProc
For exporting EXIF image data to a tabular format (csv)
# Instructions : 
1) Choose an input directory, will process all .jpg images from that directory.
2) Select Model File, preferably from the same set of images, and select the fields that you would like to export
3) Option to rename files w/ datetime exists 
4) Choose CSV export file name
5) Click run, the export file will be placed in the input directory.

![alt text](https://raw.githubusercontent.com/mritzing/exifProc/master/ScreenGrab.png)

PyQT5 Library used to make GUI  , https://build-system.fman.io/pyqt5-tutorial
exifreader to pull data , https://pypi.org/project/ExifRead/

Code Explanation : 

def initUI(self): Creates UI elements
  Elements (buttons/fields) are created and then connected with appropriate functions
def choose_model(self, file): Fills table with metadata selections
  Takes model file input and uses exifread to pull metadata fields, puts those into modelDict and the qt table
    modelDict[key] = checkBox , key is the metadata name , checkbox is the connected qt checkbox 
    Converts lat long automatically
    Ignores some fields (MakerNote, JPEGThumbnail)
def run_funct(self):  produces output
  Evaluates all choices , modelDict rename, and exports appropriate files
  
