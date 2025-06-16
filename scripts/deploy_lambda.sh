#!/bin/bash
set -e

FUNCTION_NAME=${LAMBDA_FUNCTION_NAME:-AutoKeywordPipeline}
ROLE_ARN=${LAMBDA_ROLE_ARN}
ZIP_FILE=lambda_package.zip
BUILD_DIR=lambda_build

# Clean build dir
rm -rf "$BUILD_DIR" "$ZIP_FILE"
mkdir -p "$BUILD_DIR"

# Install dependencies
pip install --quiet -r requirements.txt -t "$BUILD_DIR"

# Copy source files
cp lambda_function.py keyword_auto_pipeline.py "$BUILD_DIR"/

# Create zip package
cd "$BUILD_DIR"
zip -qr "../$ZIP_FILE" .
cd ..

# Deploy to AWS Lambda
if aws lambda get-function --function-name "$FUNCTION_NAME" >/dev/null 2>&1; then
    echo "Updating existing Lambda function: $FUNCTION_NAME"
    aws lambda update-function-code --function-name "$FUNCTION_NAME" --zip-file fileb://$ZIP_FILE
else
    if [ -z "$ROLE_ARN" ]; then
        echo "LAMBDA_ROLE_ARN environment variable must be set for create-function" >&2
        exit 1
    fi
    echo "Creating new Lambda function: $FUNCTION_NAME"
    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime python3.10 \
        --role "$ROLE_ARN" \
        --handler lambda_function.lambda_handler \
        --zip-file fileb://$ZIP_FILE
fi
