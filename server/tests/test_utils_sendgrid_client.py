import os
import pytest
import requests
from utils.sendgrid_api_client import send_verification_email
from sendgrid.helpers.mail import SendGridException


"""
GIVEN a pin
AND a token
AND a recipient
send_verification_email should return a 202 response
"""
    
def test_email_contains_pin_and_link(app_ctx, mocker):
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here"
    )

    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]

    # Validate request_body contains the expected HTML
    assert "123456" in request_body["content"][0]["value"]
    assert "verify?token=jwt-token-here" in request_body["content"][0]["value"]
    assert request_body["personalizations"][0]["to"][0]["email"] == test_recipient
    assert request_body["from"]["email"] == "mattwilkesdev@gmail.com"


def test_email_network_error(app_ctx, mocker):
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    instance = mock_sg_client.return_value
    
    instance.client.mail.send.post.side_effect = requests.exceptions.RequestException("Network error")
    
    with pytest.raises(requests.exceptions.RequestException) as err:
        send_verification_email(
            recipient="test@example.com",
            pin="123456",
            token="jwt-token-here"
        )
    
    assert "Network error" in str(err.value)

def test_email_internal_server_error(app_ctx, mocker):
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    instance = mock_sg_client.return_value
    
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.body = '{"error": "Internal server error"}'
    mock_response.headers = {"Content-Type": "application/json"}
    
    instance.client.mail.send.post.return_value = mock_response

    send_verification_email(
        recipient="test@example.com",
        pin="123456",
        token="jwt-token-here"
    )

    assert instance.client.mail.send.post.call_count == 1
    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    assert "123456" in request_body["content"][0]["value"]

