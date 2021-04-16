export AWS_DEFAULT_REGION=eu-west-1
bucketsite = aws cloudformation describe-stacks --stack-name vodImgResize --query "Stacks[0].Outputs[?OutputKey=='Bucket'].OutputValue" --output text
bucketpict = aws cloudformation describe-stacks --stack-name vodImgResize --query "Stacks[0].Outputs[?OutputKey=='BucketPict'].OutputValue" --output text

all: createbucket deploy deploy-site

createbucket:
	aws s3 mb s3://vodimageresizeartifacts022021

deploy:
	aws cloudformation package --template-file VODImgResize.yml --s3-bucket vodimageresizeartifacts022021 --output-template-file package.template
	aws cloudformation deploy --template-file package.template --stack-name vodImgResize --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

deploy-site:
	aws s3 sync www s3://$$($(bucketsite))
	aws s3 cp www/picList.json s3://$$($(bucketsite)) --cache-control max-age=0

copy-pictures:
	aws s3 sync testImages/input s3://$$($(bucketpict))