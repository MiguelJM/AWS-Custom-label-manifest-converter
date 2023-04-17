# AWS-Custom-label-manifest-converter
This Python script converts a csv file into an AWS SageMaker Ground Truth manifest to be used by Rekognition for the custom labels feature.

Instructions:
Modify the set_labels_column function with your own categorical labels.

The structure of the csv annotations file should be as follows, where the x and y fields represent bounding box pixel positions:

![image](https://user-images.githubusercontent.com/15978111/232622377-77bc7192-c155-4d22-9ed5-a61f8fa9a257.png)
| filename  | width | height | class | xmin | ymin | xmax | ymax |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

The script will automatically perform the corresponding convertions:

```python
left = xmin
top = ymax - (ymax - ymin)
width = xmax - xmin
height = ymax - ymin
```

The output will contain one row per image with all the labels in place. The structure of the JSON output (in one row per image) is similar to the following:
```json
 {
   "source-ref":"s3://your_s3_bucket/the_s3_folder/image.jpg",
   "image-0":{
      "image_size":[
         {
            "width":416.0,
            "height":416.0,
            "depth":3
         }
      ],
      "annotations":[
         {
            "class_id":1,
            "top":227.0,
            "left":160.0,
            "width":24.0,
            "height":43.0
         }
      ]
   },
   "image-0-metadata":{
      "objects":[
         {
            "confidence":1
         }
      ],
      "class-map":{
         "0":"Ok",
         "1":"Damage"
      },
      "type":"groundtruth/object-detection",
      "human-annotated":"yes",
      "creation-date":"2023-04-17T00:00:00",
      "job-name":"Python custom manifest creator"
   }
}{
   "source-ref":"s3://your_s3_bucket/the_s3_folder/image_2.jpg",
   "image-1":{
      "image_size":[
         {
            "width":416.0,
            "height":416.0,
            "depth":3
         }
      ],
      "annotations":[
         {
            "class_id":1,
            "top":5.0,
            "left":12.0,
            "width":334.0,
            "height":374.0
         }
      ]
   },
   "image-1-metadata":{
      "objects":[
         {
            "confidence":1
         }
      ],
      "class-map":{
         "0":"Ok",
         "1":"Damage"
      },
      "type":"groundtruth/object-detection",
      "human-annotated":"yes",
      "creation-date":"2023-04-17T00:00:00",
      "job-name":"Python custom manifest creator"
   }
}
```
