# CT image application
Testing task from CEITEC. Simple image application for CT slices.

## Author
- Vasilii Fedorov

## Goal
- Create application in python that will allow user load tomographic slice and put scale on it (based on pixel information). Must be simple and easy for use.

## Main requirements
- [x] Load image
  - Select path to image
- [x] Setting pixel size
- [x] Setting scale size
- [x] Option to crop input data
- [x] Insert scale, choose position
  - 4 default positions in the corners
  - Option to move position by slider
- [x] Display logo (default CEITEC logo)
- [x] Creating a Region Of Interest (ROI)
  - Selection of the region by the user
  - Setting zoom of the ROI
  - ROI will be automatically inserted on the right side next to the input image – expand image matrix according to the size of the selected ROI
- [x] Contrast adjustment
  - Histogram view
  - Setting upper and lower thresholds for histogram by sliders
- [x] Saving final image
  - Select path and format
- [x] Compile application into .exe
  
## Expected view of the application
![software_nahled](https://user-images.githubusercontent.com/62359460/186752396-b89e6a21-8b07-4af7-b67d-5e84f281918d.jpg)

## Proposed application
![ex](https://user-images.githubusercontent.com/62359460/186752998-62633ef7-2bb9-4776-a4d9-1c17444da272.png)

## Usage
1) [Download .rar file](https://drive.google.com/file/d/1MTD9fo97rsXnN1AhHSzxxtqL1hlpXind/view?usp=sharing)
2) Unpack to a folder
3) In folder find "act_ceitec_app.exe"
4) Start .exe, use input CT image from files
