# PhotoClean

Cleaner for photos with sensor line artifacts

![Screenshot_1](/icons/Screenshot1.png?raw=true "App Screenshot")

Parts of the UI are based on a modified version of https://github.com/ap193uee/PyQt-Image-Viewer

To build into a windows executable use:

pyinstaller.exe PhotoClean.spec

which is almost the same as:

pyinstaller.exe --noconfirm --onefile --hide-console hide-early --add-data "main.ui";. --name "PhotoClean" "main.py"

except I added the image folder information to PhotoClean.spec

TODOS:
- Add Hue widget
- Replace Metadata (EXIF) into fixed images
- Batch process is still not implemented
- Output folder is currently hardcoded to <images>//result


