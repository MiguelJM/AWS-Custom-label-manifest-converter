# AWS-Custom-label-manifest-converter
This Python script converts a csv file into an AWS SageMaker Ground Truth manifest to be used by Rekognition for the custom labels feature.

Instructions:
Modify the set_labels_column function with your own categorical labels.  
Set your own inputs: mode, manifest folder (output), annotations_file_folder (input), and s3 bucket name.  
Make sure to have uploaded all the images in the s3 bucket. The names of the files in the s3 bucket should be the same as in your csv annotations file.  

The structure of the csv annotations file should be as follows, where the x and y fields represent bounding box pixel positions:

| filename  | width | height | class | xmin | ymin | xmax | ymax |
| --- | --- | --- | --- | --- | --- | --- | --- |
| image.jpg  | 416 | 416 | Damage | 160 | 227 | 184 | 270 |
| image_2.jpg  | 416 | 416 | Damage | 12 | 5 | 346 | 379 |
| image_2.jpg  | 416 | 416 | Damage | 117 | 192 | 226 | 272 |


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
         },         
         {
            "class_id":1,
            "top": 192.0, 
            "left": 117.0, 
            "width": 109.0, 
            "height": 80.0
         }
      ]
   },
   "image-1-metadata":{
      "objects":[
         {
            "confidence":1
         },
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
