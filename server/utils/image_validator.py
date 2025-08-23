import filetype
import filetype.utils
from flask import current_app
from werkzeug.datastructures import FileStorage
import io

def guess_file_type(file_obj: FileStorage):
    kind = filetype.guess(file_obj)
    if kind is None:
        raise TypeError(f"Cannot guess file type!")
    else:
        return kind.extension
    

def is_valid_image(file_obj: FileStorage):
    
    guess_file_type(file_obj)
    
    is_valid = filetype.is_image(file_obj)
    
    if not is_valid:
        raise TypeError(f"Not a valid image")
    else:
        return is_valid

def is_valid_image_format(file_obj: FileStorage):
    
    allowed_extensions = current_app.config['IMAGE_UPLOAD_EXTENSIONS']
    
    extension = guess_file_type(file_obj)
    
    if extension in allowed_extensions:
        return True
    else:
        raise TypeError(f"{extension} format is not accepted")

def is_within_size_limit(file_obj: FileStorage):
    
    max_content_length = current_app.config['MAX_CONTENT_LENGTH'] 
    # print(f"max content length {max_content_length}")
    # max_size = (max_size_mb * 1024 * 1024)
    # print('max size:', max_size)
    
    file_obj.stream.seek(0, io.SEEK_END)
    size = file_obj.stream.tell()
    file_obj.stream.seek(0) # reset the cursor to the start of the stream
    if size <= max_content_length:
        return True
    else:
        raise Exception(f"file is too large")
    

def check_image_validity(files):
    files = files[:]
    valid_files = []
    invalid_files = []
    for file in files:
        try:
            ext = guess_file_type(file)
            is_valid_image(file)
            is_valid_image_format(file)
            is_within_size_limit(file)
            valid_files.append({'file':file,'ext':ext})
        except Exception as e:
            invalid_files.append({"file":file, "error":str(e)})
            print(f"{file} is not valid: {str(e)}")
    return valid_files, invalid_files