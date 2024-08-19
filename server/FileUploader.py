# TODO : Need to move this logic into the right folder - currently got an import error.

import os
from werkzeug.utils import secure_filename
import imghdr

class FileUploader:
    def __init__(self, upload_location, allowed_extensions):
        self.upload_location = upload_location
        self.allowed_extensions = allowed_extensions

    def is_valid_extension(self, filename):
        file_ext = os.path.splitext(filename)[1]
        return file_ext in self.allowed_extensions

    def validate_and_save(self, uploaded_file):
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            return False, "No file selected"

        if not self.is_valid_extension(filename):
            return False, "Invalid file extension"

        file_ext_validated = self.validate_image(uploaded_file.stream)
        if not file_ext_validated:
            return False, "Invalid image content"

        uploaded_file.save(os.path.join(self.upload_location, filename))
        return True, None
    
    # Confirm a valid image before storing. The first 512 bytes will tell you the image format.
    def validate_image(self, stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')