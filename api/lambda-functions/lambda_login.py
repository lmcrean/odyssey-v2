import json
import os
import jwt
import time
from datetime import datetime, timedelta

def generate_token(user_id, username):
    """Generate JWT token for the user"""
    secret = os.environ.get('JWT_SECRET', 'your-secret-key')  # In production, use AWS Secrets Manager
    expiration = datetime.utcnow() + timedelta(days=1)
    
    token = jwt.encode({
        'user_id': user_id,
        'username': username,
        'exp': expiration
    }, secret, algorithm='HS256')
    
    return token

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        username = body.get('username')
        password = body.get('password')
        
        if not all([username, password]):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
                'body': json.dumps({
                    'error': 'Missing required fields'
                })
            }
        
        # For now, we'll simulate login (in production, verify against database)
        # Using timestamp as mock user_id like in registration
        user_id = str(int(time.time()))
        token = generate_token(user_id, username)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'token': token,
                'user_id': user_id,
                'message': 'Login successful'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'error': str(e)
            })
        } 