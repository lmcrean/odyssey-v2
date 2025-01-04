def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Enable CORS
            'Content-Type': 'application/json'
        },
        'body': 'Hello World!'
    }