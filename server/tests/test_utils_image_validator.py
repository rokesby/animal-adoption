import io
import pytest
from werkzeug.datastructures import FileStorage
from utils.image_validator import check_image_validity, is_valid_image, is_valid_image_format, is_within_size_limit
from flask import current_app

def test_valid_image_validation():
    """
    If an image is passed to is_valid_image
    It should return true
    """
    png_bytes = b'\x89PNG\r\n\x1a\n'
    file_obj = FileStorage(
        stream=io.BytesIO(png_bytes),
        filename='test.png'
    )
    
    assert is_valid_image(file_obj) == True
    
def test_valid_image_validation_webp():
    """
    If an image is passed to is_valid_image
    It should return true
    """
    webp_bytes = (
    b'RIFF' + (30).to_bytes(4, 'little') + b'WEBP'
    + b'VP8 '                       # Simple WebP chunk marker
    + (10).to_bytes(4, 'little')   # Fake chunk size
    + b'\x9D\x01\x2A'              # VP8 keyframe start
    + b'\x00' * 7                  # Padding to make it "longer"
    )
    file_obj = FileStorage(
        stream=io.BytesIO(webp_bytes),
        filename='test.webp'
    )
    assert is_valid_image(file_obj) == True
    
def test_invalid_image_validation():
    """
    If an invalid image is passed to is_valid_image
    It should return a TypeError
    """
    mp4_bytes = (
    b'\x00\x00\x00\x18'
    b'ftyp'
    b'isom'
    b'\x00\x00\x00\x00'
    b'isom'
    b'avc1'
)
    file_obj = FileStorage(
        stream=io.BytesIO(mp4_bytes),
        filename='invalid.Mov'
    )
    
    with pytest.raises(TypeError) as err:
        result = is_valid_image(file_obj)
        print(f"Function returned: {result}")
        print(f"Type of result: {type(result)}")
    error_message = str(err.value)
    print(error_message)
    assert 'Not a valid image' in error_message
    

def test_valid_png(app_ctx, db_connection):
    """
    If an png is passed to is_valid_image_format
    It should return true
    """
    png_bytes = b'\x89PNG\r\n\x1a\n'
    file_obj = FileStorage(
        stream=io.BytesIO(png_bytes),
        filename='test.png'
    )
    assert is_valid_image_format(file_obj) == True
    
def test_valid_jpg(app_ctx, db_connection):
    """
    If an jpg is passed to is_valid_image_format
    It should return true
    """
    jpg_bytes = b'\xff\xd8\xff\xe0'
    file_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='test.jpg'
    )
    assert is_valid_image_format(file_obj) == True
    
def test_valid_jpeg(app_ctx, db_connection):
    """
    If an jpeg is passed to is_valid_image_format
    It should return true
    """
    
    jpeg_bytes = b'\xff\xd8\xff\xe0'
    file_obj = FileStorage(
        stream=io.BytesIO(jpeg_bytes),
        filename='test.jpeg'
    )
    assert is_valid_image_format(file_obj) == True
    
def test_valid_gif(app_ctx, db_connection):
    """
    If an jpeg is passed to is_valid_image_format
    It should return true
    """
    gif_bytes = b'GIF87a'
    file_obj = FileStorage(
        stream=io.BytesIO(gif_bytes),
        filename='test.gif'
    )
    assert is_valid_image_format(file_obj) == True
    
def test_valid_webp(app_ctx, db_connection):
    """
    If an webp is passed to is_valid_image_format
    It should return true
    """
    webp_bytes = (
    b'RIFF' + (30).to_bytes(4, 'little') + b'WEBP'
    + b'VP8 '                       # Simple WebP chunk marker
    + (10).to_bytes(4, 'little')   # Fake chunk size
    + b'\x9D\x01\x2A'              # VP8 keyframe start
    + b'\x00' * 7                  # Padding to make it "longer"
    )
    file_obj = FileStorage(
        stream=io.BytesIO(webp_bytes),
        filename='test.webp'
    )
    assert is_valid_image_format(file_obj) == True
    
def test_mp4_is_invalid_image_format(app_ctx, db_connection):
    """
    If an mp4 file is passed to is_valid_image_format
    It should return a TypeError
    """
    mp4_bytes = (
    b'\x00\x00\x00\x18'
    b'ftyp'
    b'isom'
    b'\x00\x00\x00\x00'
    b'isom'
    b'avc1'
)
    file_obj = FileStorage(
        stream=io.BytesIO(mp4_bytes),
        filename='invalid.mp4'
    )

    with pytest.raises(TypeError) as err:
        result = is_valid_image_format(file_obj)
        print(f"Function returned: {result}")
        print(f"Type of result: {type(result)}")
    error_message = str(err.value)
    print(error_message)
    assert 'mp4 format is not accepted' in error_message
    
def test_psd_is_invalid_image_format(app_ctx, db_connection):
    """
    If an invalid image is passed to is_valid_image_format
    It should return a TypeError
    """
    psd_bytes = (
    b'8BPS'             # Signature
    b'\x00\x01'         # Version 1
    b'\x00 * 6'    # Reserved
    b'\x00\x01'         # Number of channels
    b'\x00\x00\x00\x10' # Height = 16
    b'\x00\x00\x00\x10' # Width = 16
    b'\x00\x08'         # Bit depth = 8
    b'\x00\x03'         # Color mode = RGB
    )
    file_obj = FileStorage(
        stream=io.BytesIO(psd_bytes),
        filename='invalid.psd'
    )

    with pytest.raises(TypeError) as err:
        result = is_valid_image_format(file_obj)
        print(f"Function returned: {result}")
        print(f"Type of result: {type(result)}")
    error_message = str(err.value)
    print(error_message)
    assert 'psd format is not accepted' in error_message 
    
    
def test_image_within_size_limit_is_valid(app_ctx, db_connection):
    """
    If a file is under 5mb
    is_within_size_limit should return true
    """
    jpg_bytes = b'\xff\xd8\xff\xe0' #4 bytes
    three_mb = 3 * 1024 * 1024
    padding_size = three_mb - len(jpg_bytes)
    
    jpg_bytes = b'\xff\xd8\xff\xe0' + b'\x00' * padding_size
    
    file_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='3mb_test.jpg'
            )
        
    assert is_within_size_limit(file_obj) == True
    
def test_image_image_over_size_limit(app_ctx, db_connection):
    current_app.config['ACCESS_TOKEN_EXPIRY']
    
    jpg_bytes = b'\xff\xd8\xff\xe0' #4 bytes
    four_mb = 4 * 1024 * 1024
    padding_size = four_mb - len(jpg_bytes)
    
    
    jpg_bytes = b'\xff\xd8\xff\xe0' + b'\x00' * padding_size
    
    file_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='3mb_test.jpg'
            )
    with pytest.raises(Exception) as err:
        result = is_within_size_limit(file_obj)
        print(f"Function returned: {result}")
        print(f"Type of result: {type(result)}")
    error_message = str(err.value)
    print(error_message)
    assert 'file is too large' in error_message
    
def test_check_image_validity_with_valid_images(app_ctx, db_connection):
    """
    Given a list of images that are ALL valid
    check_image_validity should return ALL images in a list
    """
    jpg_bytes = b'\xff\xd8\xff\xe0' #4 bytes
    three_mb = 3 * 1024 * 1024
    padding_size = three_mb - len(jpg_bytes)
    
    jpg_bytes = b'\xff\xd8\xff\xe0' + b'\x00' * padding_size
    
    file_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='3mb_test.jpg'
            )
    files = []
    
    for i in range(3):
        file_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename=f"3mb_test_{i}.jpg"
            )
        files.append(file_obj)
    
    print(files)
    valid_files, _ = check_image_validity(files)
    print(valid_files)
    assert len(valid_files) == 3
    
def test_check_image_validity_with_invalid_images(app_ctx, db_connection):
    """
    Given a list of images that are ALL invalid
    check_image_validity should return an empty list
    """
    jpg_bytes = b'\xff\xd8\xff\xe0' #4 bytes
    four_mb = 4 * 1024 * 1024
    padding_size = four_mb - len(jpg_bytes)
    
    jpg_bytes = b'\xff\xd8\xff\xe0' + b'\x00' * padding_size
    
    jpg_obj = FileStorage(
        stream=io.BytesIO(jpg_bytes),
        filename='4mb_test.jpg'
            )
    
    psd_bytes = (
    b'8BPS'             # Signature
    b'\x00\x01'         # Version 1
    b'\x00 * 6'    # Reserved
    b'\x00\x01'         # Number of channels
    b'\x00\x00\x00\x10' # Height = 16
    b'\x00\x00\x00\x10' # Width = 16
    b'\x00\x08'         # Bit depth = 8
    b'\x00\x03'         # Color mode = RGB
    )
    psd_obj = FileStorage(
        stream=io.BytesIO(psd_bytes),
        filename='invalid.psd'
    )
    
    mp4_bytes = (
    b'\x00\x00\x00\x18'
    b'ftyp'
    b'isom'
    b'\x00\x00\x00\x00'
    b'isom'
    b'avc1'
)
    mp4_obj = FileStorage(
        stream=io.BytesIO(mp4_bytes),
        filename='invalid.mp4'
    )
    files = [jpg_obj,psd_obj,mp4_obj]
    
    valid_files, invalid_files = check_image_validity(files)
    print(f'valid files: {valid_files}')
    print(f'invalid files: {invalid_files}')
    assert len(invalid_files) == 3
    assert len(valid_files) == 0
    