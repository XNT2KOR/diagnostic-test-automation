"""Simple unit tests for the mock ECU."""

from src.mock_ecu import process_request


def test_session_control_response():
    """Test that ECU returns correct response for session control."""
    response = process_request("10 01")
    assert response == "50 01"


def test_read_data_response():
    """Test that ECU returns correct response for read data."""
    response = process_request("22 F1 90")
    assert response == "62 F1 90 12"


def test_security_access_response():
    """Test that ECU returns correct response for security access."""
    response = process_request("27 01")
    assert response == "67 01"


def test_unknown_service_returns_negative_response():
    """Test that unknown service gets negative response."""
    response = process_request("99 99")
    assert response == "7F 10 11"
