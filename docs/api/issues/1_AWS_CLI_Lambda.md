Trying to create a lambda function using the AWS CLI.

```bash
lmcre@Laurie-mini-PC MINGW64 /c/Projects/odyssey-v2 (main)
$ # Create zip file
zip lambda_welcome_noauth.zip lambda_welcome_noauth.py 

# Create Lambda function
aws lambda create-function \
  --function-name odyssey-welcome-noauth \
  --runtime python3.11 \
  --handler lambda_welcome_noauth.lambda_handler \
  --role arn:aws:iam::203918856272:role/odyssey-auth-lambda-role \
  --zip-file fileb://lambda_welcome_noauth.zip
bash: zip: command not found

An error occurred (AccessDeniedException) when calling the CreateFunction operation: User: arn:aws:iam::203918856272:user/odyssey-drf-s3 is not authorized to perform: iam:PassRole on resource: arn:aws:iam::203918856272:role/odyssey-auth-lambda-role because no identity-based policy allows the iam:PassRole action
```