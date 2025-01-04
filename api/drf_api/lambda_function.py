"""
This is the lambda function for the API.
"""

def lambda_handler():
    """
    This is the lambda handler for the API.
    """
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Enable CORS
            'Content-Type': 'application/json'
        },
        'body': 'Hello World!'
    }
