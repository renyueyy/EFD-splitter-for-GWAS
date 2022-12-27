# Fourier Analysis of Contours
Contour extraction and Fourier parameter analysis of images containing objects.     
We wrote this pipeline to perform simple processing of images containing fruit and to perform Fourier parameter extraction and mathematical analysis.   
All functions are contained in main.py.  
## Installation 
Clone this repository   
Install requirements.txt  
Open bash, go to the main repository folder and run the following command:  
## 
    >pip install -r requirements.txt

## Start up
If the installation is complete, then in python run :    
## 
    >main()
We can see the results of the run as shown below:  

![main1](https://img-blog.csdnimg.cn/053086f687104e00bd9b8cd343974d14.png)  

there are 9 main functions in the pipeline:     
## 
    >1.picture division 
    Multiple objects on a single image can be segmented to obtain an image containing only a single object. 
    >>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.
    
    >2.find contour  
    RGB-based contour acquisition of images requires a large difference between the object colour and the background colour, allowing for more accurate recognition.
    >>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.
    
    >3.resize    
    Area correction of the binarised image after contour recognition so that the number of pixels within the contour is the human input value.
    >>You need to enter the path to the folder where the image is located and the path to the output folder and the number of pixels within the outline required. The default number of pixels used in this study is 70,000. The pipeline will determine the output folder and automatically create a new one if it does not exist.
    
    >4.rotation based on average 
    Inter-profile orientation correction according to the average profile.
    
    >5.get average   
    Calculating the average area of multiple contours.
    
    >6.rotation based on symmetric   
    Orientation correction of contours according to symmetry.
    >>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.

    >7.get efd   
    Fourier operator parsing of the contours, obtaining the first 10 levels of parameters by default and outputting as a csv file.
    >>You need to enter the path to the folder where the image is located and the path to the output folder. The pipeline will determine the output folder and automatically create a new one if it does not exist.

    >8.reconstruction  
    This function allows the profile to be fitted to the Fourier parameters
    
    >9.area ratio:    
    Calculate the overlap between the reconstructed profile and the original profile and output the overlap as a table.
    
  10.exist：you can choose to exit the pipeline or continue running it   
