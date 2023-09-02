# EFD-spliter-for-GWAS

Contour extraction and Fourier parameter analysis of images containing objects.  
We wrote this pipeline to perform simple processing of images containing fruit and to perform Fourier parameter extraction and mathematical analysis.  
All functions are contained in main.py.

# Requirements
 - requirements.txt
 
# Installation

Clone this repository  
Install requirements.txt  
Open bash, go to the main repository folder and run the following command:
```
>pip install -r requirements.txt
```
# Start Up
If the installation is complete, then in python run:
```
>main()
```

## 1.Picture division

Multiple objects on a single image can be segmented to obtain an image containing only a single object. 
>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.

 - The input file should be an **RGB image** containing the target fruit.
 - Need to choose according to the picture background colour selection.

```
choose the function you want(1-12):1
input the folder of origin picture:./demo/use
input the folder of output picture:./demo/use_out
choose background color, white, black or other(w/b/o):b
```
 
## 2.Find contours

RGB-based contour acquisition of images requires a large difference between the object colour and the background colour, allowing for more accurate recognition.
>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.

 - You can choose in this step whether you want area unification at the same time (**default area is 70,000 pixels**).
```
choose the function you want(1-12):2
if you want to resize your pics in the same area(y/n):n
choose the background of your pics, white, black or other(w/b/o):b
input the folder of origin picture:./demo/use_out
input the folder of output picture:./demo/use_contour
```
## 3.Resize

Area correction of the binarised image after contour recognition so that the number of pixels within the contour is the human input value.
>You need to enter the path to the folder where the image is located and the path to the output folder and the number of pixels within the outline required. The pipeline will determine the output folder and automatically create a new one if it does not exist.

 - Default area is 70,000 pixels.
```
choose the function you want(1-12):3
input the folder of origin picture:./demo/use_contour
input the route of output picture:./demo/use_resize
input the average area of output picture:70000
```
## 4.Rotation based on average

Inter-profile orientation correction according to the average profile.
```
choose the function you want(1-12):4
input the folder of origin picture:./demo/use_resize
input the route of output picture:./demo/use_rotation1
```

## 5.Get average

Calculating the average area of multiple contours.
```
choose the function you want(1-12):5
input the folder of origin picture:./demo/use_rotation1
input the route of output picture:./demo/use_average
```

## 6.Rotation based on symmetric

Orientation correction of contours according to symmetry.
>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.
```
choose the function you want(1-12):6
input the folder of origin picture:./demo/use_average
input the route of output picture:./demo/use_rotation2
```

## 7.Get EFDs

Fourier operator parsing of the contours, obtaining the first **10 levels** of parameters by default and outputting as a **csv file**.
>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.
```
choose the function you want(1-12):7
input the folder of origin picture:./demo/use_rotation2
input the route of output csv:./demo/efd
```

## 8.Reconstruction
Contour reconstruction based on multilevel Fourier coefficients.
 - Allows the profile to be fitted to the Fourier parameters.
```
choose the function you want(1-12):8
input the folder of origin picture:。/demo/use_rotation2
input the route of output picture:。/demo/use_rconstruction
```

## 9.Get area ratio

Calculate the overlap between the reconstructed profile and the original profile and output the overlap as a table.
```
choose the function you want(1-12):9
input the folder of origin picture:./demo/use_rotation2
input the route of output csv:./demo/use_area_ratio
```

## 10.Statistical EFDs format
Summarising and formatting Fourier coefficients for multiple profiles.
```
choose the function you want(1-12):10
input the folder of tables:./demo/use_efd
input the route of output csv:./demo/use_efds
```

## 11.Contour reconstruction for different genotypes
Contour reconstruction according to different genotypes

 - The input file is the calculated mean Fourier coefficients for the different genotypes.
 - The output file is the result of plotting the different genotypes in separate colours. All contours are plotted with the principle of overlapping centres of mass.
