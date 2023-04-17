# AWS-Custom-label-manifest-converter
This Python script converts a csv file into an AWS SageMaker Ground Truth manifest to be used by Rekognition for the custom labels feature.

The structure of the csv annotations file should be as follows:

filename	width	height	class	xmin	ymin	xmax	ymax
image_1.jpg	416	416	Damage	160	227	184	270
![image](https://user-images.githubusercontent.com/15978111/232622316-ac38afad-35b6-4b73-9fb3-e1cae98712f6.png)

