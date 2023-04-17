# AWS-Custom-label-manifest-converter
This Python script converts a csv file into an AWS SageMaker Ground Truth manifest to be used by Rekognition for the custom labels feature.

The structure of the csv annotations file should be as follows:
filename	width	height	class	xmin	ymin	xmax	ymax
![image](https://user-images.githubusercontent.com/15978111/232622157-28379b64-21bf-4b20-9157-3a38d69778ff.png)
