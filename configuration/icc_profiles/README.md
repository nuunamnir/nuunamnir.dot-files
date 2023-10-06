# Creating ICC Profiles Using Spyder5PRO
## Getting Started
Install [DisplayCAL Python 3](https://github.com/eoyilmaz/displaycal-py3) by executing following commands in the desired directory:
```
git clone https://github.com/eoyilmaz/displaycal-py3
cd ./displaycal-py3/
git checkout develop
python -m venv ./displaycal_venv
source displaycal_venv/bin/activate
pip install -r requirements.txt
python -m build
pip install dist/DisplayCAL-3.9.*.whl
```
Reset to screen to factory settings and set the brightness to maximum (100) and contrast to medium (50), sharpness to medium (60) and response time to "faster".
### Perform Calibration
Target is the "Video, D65" preset. Start the calibration and follow the instructions. The calibration will take about 30 to 60 minutes.
### Copy File and Update .xinitrc
Copy the files from `.local/share/DisplayCAL/storage/` to the desired location and update the .xinitrc file:
```
dispwin -d 1 -i ~/.config/icc_profiles/profile.icc
```

