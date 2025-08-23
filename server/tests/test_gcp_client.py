import io
import pytest
from werkzeug.datastructures import FileStorage
from utils.gcp_client import GCSImageStorage
from google.cloud import storage

def test_gcs_client_uses_default_project(mocker, app_ctx, db_connection):
    """
    When GCSImageStorage is created
    It should initialise with correct bucket name and storage client
    """
    mock_client_class = mocker.patch('utils.gcp_client.storage.Client')
    mock_client_instance = mock_client_class.return_value
    mock_bucket = mocker.Mock()
    mock_client_instance.bucket.return_value = mock_bucket
    
    storage = GCSImageStorage('test-bucket')
    
    # Assert your class behavior
    assert storage.bucket_name == 'test-bucket'
    mock_client_class.assert_called_once()
    mock_client_instance.bucket.assert_called_once_with('test-bucket')

def test_gcs_client_returns_animal_images(mocker, app_ctx, db_connection,auth_user):
    """
    Given a validbucket name
    list_list_animal_images should return all filenames in the bucket
    """
    mock_client_class = mocker.patch('utils.gcp_client.storage.Client')
    mock_client= mock_client_class.return_value
    
    storage_client = GCSImageStorage('test-bucket')
    
    mock_blob_1 = mocker.Mock()
    mock_blob_1.name = "assets/images/1/image_1.jpg"
    mock_blob_2 = mocker.Mock()
    mock_blob_2.name = "assets/images/1/image_2.jpg"
    mock_blob_3 = mocker.Mock()
    mock_blob_3.name = "assets/images/1/image_3.jpg"
    mock_blob_4 = mocker.Mock()
    mock_blob_4.name = "assets/images/2/Image_1.jpg"
    
    mock_client.list_blobs.return_value = [mock_blob_1, mock_blob_2, mock_blob_3]
    
    result = storage_client.list_animal_images(1)
    
    assert result == ["image_1.jpg","image_2.jpg","image_3.jpg"]
    mock_client.list_blobs.assert_called_once_with('test-bucket', prefix='assets/images/1/', delimiter='/')
    
    """
    Given an invalid bucket name
    list_blobs should return an error
    """

    """
    Given an invalid bucket name
    list_blobs should return an error
    """
    
    """
    Given a file object
    upload_animal_image_from_stream should 
    """