
from werkzeug.datastructures import FileStorage

def format_filename_for_upload(file_obj, ext):
    from uuid import uuid4
    
    if ext is None or ext == '':
        print(f'filename missing extension: {file_obj.filename}')
        raise ValueError(("filename is missing an extension"))
    
    filename = str(uuid4())
    file_obj.filename = f"{filename}.{ext}"
    
    return file_obj