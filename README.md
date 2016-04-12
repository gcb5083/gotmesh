# got mesh?

got mesh? is the most cheap and simplistic open source 3D scanner, with no moving parts.

# how it works
The system at its core uses draining of a large tub of opaque liquid to create contours between the liquid and the object to be scanned. The contours are captured by your favorite timelapse device (DSLR, smartphone, etc.) and then imported into a folder on your computer. A python script that employs [OpenCV] converts the collection of images to a 3D point cloud mesh of .xyz format. If desired the output file can be converted into an .stl file for 3D printing by a program like [MeshLab].

This project was originally entered in [HackPSU] 2016 and recieved second place overall.

# running the newest point conversion

To run the latest version of the point conversion from command line you need OpenCV installed. The arguement required is the location of the folder containing the images. This will open a preview viewer where you can adjust the edge detection thresholds. To save the current thresholds for all future images, click the save bar. To start processing, click the start bar. This will generate an xyz output file that then can be converted into an .stl file using another program, (we used MeshLab). A sample xyz file, MeshLab postprocessed xyz file and converted STL are included of the rock we used at HackPSU 2016.

Example:

```sh
$ python point_conversion.py '/input/'

# running the original point conversion

To run the HackPSU2016 version of the point conversion from command line you need OpenCV installed. The arguements required are location of the folder containing the images, filter 1 parameter (we used 2000) and, filter filter 2 pameter (we used 2500). This will generate an xyz output file that then can be converted into an .stl file using another program, (we used MeshLab). 

Example:

```sh
$ python point_conversion.py '/rock/' '2000' '2500'
```

# future goals?

 - support time lapse video / video input
 - determine the best liquid
 - improve lighting system


   [OpenCV]: <http://opencv.org/>
   [HackPSU]: <http://hackpsu.org/>
   [MeshLab]: <http://meshlab.sourceforge.net/>


