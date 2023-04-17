# Developer: Miguel Angel Jara Maldonado
# Creation Date: 2023/04/14
# Last Modification Date: 2023/04/17 16:52
# Description: This script takes the labels of the dataset from a csv file and creates a Sage Maker manifest file.

import time
import json
import pandas as pd
import numpy as np
from datetime import date


# This function makes sure that JSON can encode non built-in datatypes.
# Certain data types of the dataframe will fail when encoding to JSON.
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


# Converts the coordinates from the csv file to the format expected by sagemaker.
def convert_add_new_coordinates( annotations_df ):
    coords_dictionaries = list()
    annotations_df['box left'] = annotations_df['xmin']
    # For some reason with the original ymax it puts the box exactly below the real box. Also, this is a subtraction, posibly the coordinate system counts from top to bottom.
    annotations_df['box top'] = annotations_df['ymax'] - (annotations_df['ymax'] - annotations_df['ymin'])
    annotations_df['box width'] = (annotations_df['xmax'] - annotations_df['xmin'])
    annotations_df['box height'] = (annotations_df['ymax'] - annotations_df['ymin'])

    return annotations_df


# Creates a new column with the categorical labels converted to numeric.
def set_labels_column( df ):
    df['class_id'] = df.apply(lambda row:
                                1 if row['class'] == 'Damage'
                                else 0, axis=1)
    return df


# Removes those rows that have NaN values in all the columns.
def drop_rows_with_all_nans( df ):
    df = df.dropna(how='all')
    return df


# Rename a dataframe column.
def rename_columns( df, old_col_names, new_col_names ):
    if len(old_col_names) != len(new_col_names):
        raise ValueError("rename_columns: The lenght of the new and old column names is not equal.")

    for index, old_col_name in enumerate(old_col_names):
        df = rename_column( df, old_col_name, new_col_names[index] )

    return df


# Rename a dataframe column.
def rename_column( df, old_col_name, new_col_name ):
    df = df.rename({old_col_name: new_col_name}, axis=1)

    return df


# Opens the csv file with the label annotations.
def read_csv_file( csv_path ):
    annotations_df = pd.read_csv( csv_path )
    annotations_df = drop_rows_with_all_nans( annotations_df )
    annotations_df = set_labels_column( annotations_df )

    return annotations_df


# Generates the list of all label annotations for one image. (top, left, width and height)
def generate_annotations_list( image_annotations_df ):
    image_annotations_df = rename_columns( image_annotations_df, 
                                        ['box top', 'box left', 'box width', 'box height'], 
                                        ['top', 'left', 'width', 'height'] )
    annotations_dict_list = image_annotations_df.to_dict('records')

    return annotations_dict_list


# Generates the json structure of the .manifest file.
def generate_json_manifest_dictionary( image_annotations_df, s3_bucket_name, image_counter, current_date ):
    if( len(image_annotations_df) == 0 ):
        raise Exception( "There are no image annotations rows for image {}.".format( image_counter ) )

    first_row_data = image_annotations_df.iloc[0]


    image_name = first_row_data['filename']
    s3_image_dir = s3_bucket_name + image_name

    img_width = first_row_data['width']
    img_height = first_row_data['height']

    image_id = "image-" + str(image_counter)
    image_metadata = "{}-metadata".format(image_id)
    channels = 3 # This is normally 3 for RGB

    labels_dict = { "0": "Ok",
                    "1": "Damage" }

    annotations_list = generate_annotations_list( image_annotations_df[ ['class_id', 'box top', 'box left', 'box width', 'box height'] ] )

    objects_list = [{"confidence": 1}] * len( image_annotations_df )

    manifest_dictionary = {
        "source-ref": s3_image_dir,
        image_id: 
        {
            "image_size": 
            [{
                "width": img_width,
                "height": img_height,
                "depth": channels
            }],
            "annotations": annotations_list
        },
        image_metadata: 
        {
            "objects": objects_list,
            "class-map": labels_dict,
            "type": "groundtruth/object-detection",
            "human-annotated": "yes",
            "creation-date": current_date,
            "job-name": "Python custom manifest creator"
        }
    }

    return manifest_dictionary


# Retrieves all the rows of the manifest file as a list of dictionaries.
def get_manifest_dictionaries( annotations_df, s3_bucket_name ):
    manifest_dicts_list = []
    file_names = annotations_df['filename'].unique()
    current_date = str( date.today().strftime("%Y-%m-%dT%H:%M:%S") )

    for index, file_name in enumerate(file_names):
        image_annotations_df = annotations_df[ annotations_df['filename'] == file_name ]
        current_file_manifest = generate_json_manifest_dictionary( image_annotations_df, s3_bucket_name, index, current_date )
        manifest_dicts_list.append( current_file_manifest )

    return manifest_dicts_list


# Save the manifest in a .manifest file.
def save_manifest( manifest_file_path, manifest_dictionaries ):
    with open(manifest_file_path, "w", encoding="UTF-8") as output_file:
        for manifest in manifest_dictionaries:
            output_file.write(json.dumps(manifest, cls=NpEncoder))
            output_file.write('\n')
    return


# Takes the labels of the dataset from a csv file and creates a Sage Maker manifest file.
def main( csv_file_path, manifest_file_path, s3_bucket_name ):
    annotations_df = read_csv_file( csv_file_path )

    # annotations_df = annotations_df.iloc[:3]
    annotations_df = convert_add_new_coordinates( annotations_df )  
    manifest_dicts_list = get_manifest_dictionaries( annotations_df, s3_bucket_name )

    save_manifest( manifest_file_path, manifest_dicts_list )    

    return


# This is used for cmd tests only and it is not executed when called from elsewhere.
if __name__ == "__main__":

    startTime = time.time()    

    modes = ['train', 'test', 'validation']    
    ### Set inputs ###
    mode = modes[0]

    manifest_folder = r'C:\\Users\\xmij\\Documents\\ML\\Image processing\\src\\Container anomaly detection\\Manifests\\Python generated manifests\\'
    annotations_file_folder = r'C:\\Users\\xmij\\Documents\\ML\\Image processing\\Images from Container Damage Detection\\' + mode + '\\'
    s3_bucket_name = "s3://abat-aws-image-rekognition/container-" + mode + '/'
    ###--------- ###        

    csv_file_path = annotations_file_folder + '_annotations.csv'
    manifest_file_path = manifest_folder + mode + '_manifest.manifest'

    main( csv_file_path, manifest_file_path, s3_bucket_name )
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))

