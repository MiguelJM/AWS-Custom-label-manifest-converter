# AWS-Custom-label-manifest-converter
This Python script converts a csv file into an AWS SageMaker Ground Truth manifest to be used by Rekognition for the custom labels feature.

The structure of the csv annotations file should be as follows:

filename	width	height	class	xmin	ymin	xmax	ymax
example_image.jpg	416	416	Damage	160	227	184	270
![image](https://user-images.githubusercontent.com/15978111/232622377-77bc7192-c155-4d22-9ed5-a61f8fa9a257.png)


