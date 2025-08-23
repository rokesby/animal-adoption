import pytest
import io
from werkzeug.datastructures import FileStorage

from utils.file_formatter import format_filename_for_upload

def test_format_image_filename_for_upload():
    """
    Given an image file
    format_image_for_upload 
    should return an image file with a new filename
    """

    jpg_bytes = b'\xff\xd8\xff\xe0'
    
    jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='test.jpg'
            )

    print(f"jpg_obj filename = {jpg_obj.filename}")
    
    result = format_filename_for_upload(jpg_obj, 'jpg')
    print(f"result filename: {result.filename}")
    assert result.filename != 'test.jpg'
    
def test_format_filename_for_upload_is_valid_uuid():
    """
    Given an image file
    format_image_for_upload 
    should replace the filename with a UUID string
    AND retain the file extension
    """
    import uuid
    
    jpg_bytes = b'\xff\xd8\xff\xe0'
    
    jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='test.jpg'
            )

    print(f"jpg_obj filename = {jpg_obj.filename}")
    
    result = format_filename_for_upload(jpg_obj, 'jpg')
    print(f"result filename: {result.filename}")
    parts = result.filename.split('.')
    assert len(parts) == 2
    uuid_part = parts[0]
    extension_part = parts[-1]
        
    parsed_uuid = uuid.UUID(uuid_part, version=4) 
    assert parsed_uuid is not None
    assert extension_part == 'jpg'
    
def test_filename_missing_extension_error():
    """
    Given an image file
    If the filename is missing an extension
    It should throw an error 'filename is missing an extension'
    """
    
    jpg_bytes = b'\xff\xd8\xff\xe0'
    
    jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='testfilenamemissingextension'
            )

    print(f"jpg_obj filename = {jpg_obj.filename}")
    with pytest.raises(ValueError) as err:
        result = format_filename_for_upload(jpg_obj, '')
        print(f"result filename: {result.filename}")
    error_message = str(err.value)
    assert error_message == "filename is missing an extension"
    
@pytest.mark.skip("unifinished")
def test_format_multiple_image_for_upload():
    """
    Given a list of images
    format_image_for_upload 
    should return a list of unique filenames
    """

    jpg_bytes = b'\xff\xd8\xff\xe0'
    
    jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='test.jpg'
            )
    
    image_list = []
    for num in range(3):
        jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename=f'test_{num}.jpg'
            )
        image_list.append(jpg_obj)
    
    print(image_list)
    
    result = format_filename_for_upload()
    assert result