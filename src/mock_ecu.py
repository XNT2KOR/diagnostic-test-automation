"""Mock ECU that simulates diagnostic responses."""


def process_request(request_payload):
    """Process a diagnostic request and return a response.
    
    Args:
        request_payload: String like "10 01"
    
    Returns:
        String like "50 01" or "7F 10 11" if service not recognized
    """
    
    # Simple mapping: request -> response
    responses = {
        "10 01": "50 01",           # Diagnostic session control
        "22 F1 90": "62 F1 90 12",  # Read data by identifier
        "27 01": "67 01",           # Security access request
    }
    
    if request_payload in responses:
        return responses[request_payload]
    else:
        return "7F 10 11"  # Negative response for unknown service
