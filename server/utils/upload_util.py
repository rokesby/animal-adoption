
from flask import jsonify
from utils.file_formatter import format_filename_for_upload
from utils.gcp_client import GCSImageStorage, get_gcs_public_config


def upload_images(valid_files, id): 
    number_of_valid_images = len(valid_files)
    config = get_gcs_public_config()
    storage_client = GCSImageStorage(config['bucket_name'])
    animal_image_limit = config['animal_image_limit'] 
    current_gcs_image_list = storage_client.list_animal_images(id) 
   
    number_of_gcs_images = len(current_gcs_image_list) 
  
    total_number_of_images = number_of_gcs_images + number_of_valid_images 
    
    remaining_image_limit_number = (animal_image_limit - total_number_of_images)
    print(f'remaining_image_limit_number before limit check {remaining_image_limit_number}')
    if total_number_of_images <= animal_image_limit:
        uploaded_files = []
        failed_uploads = []
        try:
            for file in valid_files:
                formatted_file_obj = format_filename_for_upload(file['file'],file['ext'])
                result = storage_client.upload_animal_image_from_stream(formatted_file_obj, id)
                if result['success']:
                    uploaded_files.append(result['filename'])
                else:
                    failed_uploads.append({"filename": result['filename'], "error":result['error']})
                print(f"you can upload up to {remaining_image_limit_number} more images")
        except Exception as e:
            return jsonify({"error": "Upload failed", "details": str(e)}), 500
        finally:
            remaining_image_limit_number = animal_image_limit - len(uploaded_files)
    else:
        # if the total more than 10 -> denied
        raise Exception("Too many images uploaded")
    return jsonify({"message":"Upload complete",
                    "uploaded": uploaded_files,
                    "failed": failed_uploads,
                    "remaining slots": remaining_image_limit_number
                    }), 201