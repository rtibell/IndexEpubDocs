#!/bin/bash

echo "Make Zip"
rm -f epub-index-upload.zip
sh mkzip-upload.sh

echo "Remove old Lambda"
aws --profile rt-aws-java-usr --region eu-central-1 s3api put-bucket-notification-configuration --bucket=ratts-epub-docs --notification-configuration="{}"
sleep 1
aws --profile rt-aws-java-usr --region eu-central-1 lambda delete-function \
          --function-name "RTAWS-epub-doc-upload" 
sleep 1

echo "Create Lambda"
rm -f RTAWS-epub-doc-upload.json
aws --profile rt-aws-java-usr --region eu-central-1 lambda create-function \
          --function-name "RTAWS-epub-doc-upload" \
          --memory-size 512 \
          --runtime "python2.7" \
          --role "arn:aws:iam::187928521526:role/service-role/lambdaRole" \
          --handler LambdaUploadTrigger.lambda_handler \
          --description "Uppload Epub trigger. Starting trigger." \
          --timeout 30 \
          --publish \
          --zip-file "fileb://epub-index-upload.zip" > RTAWS-epub-doc-upload.json
#cat RTAWS-epub-doc-upload.json
sleep 1

aws --profile rt-aws-java-usr --region eu-central-1 lambda publish-version --function-name "RTAWS-epub-doc-upload" > RTAWS-epub-doc-upload-rel.json
evarn=`grep Arn RTAWS-epub-doc-upload-rel.json | awk '{printf("%s\n",$2);}' | sed -e 's/,//' | sed -e 's/"//g'`
echo "Published Lambda ${evarn}"
sleep 1

echo "Setup S3 Lambda Trigger"
cat upload-trigg.json | sed -e "s/__REPLACE-LAMBDA__/${evarn}/" > curr-upload-trigg.json
aws --profile rt-aws-java-usr --region eu-central-1 s3api put-bucket-notification-configuration --bucket=ratts-epub-docs --cli-input-json file://curr-upload-trigg.json
cat curr-upload-trigg.json
rm -f curr-upload-trigg.json

