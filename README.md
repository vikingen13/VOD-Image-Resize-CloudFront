# VOD-Image-Resize
An AWS project using AWS Rekognition to smartly crop images

## Description

Resizes images on the fly using an AWS server less architecture.

If the final size does not have the same image ratio, the image is cropped using a smart strategy based on AWS Rekognition text and face detection.

Interesting feature is that the image is only processed once at the first request and stored on S3 for future use. In other words, an unused image will never be processed and a used image will be processed only once.

The crop strategy configured in this project is particularly suited to crop movie posters.

## Architecture
![Image of Architecture](https://github.com/vikingen13/VOD-Image-Resize/blob/master/Doc/ImageResize.png)

## Usage
The project deployment can be done using AWS Cloud Formation.

* Create an AWS Bucket where you have the right to write. This bucket will be used as an artefactory repository. In our example, this bucket will be name ArtefactoryBucket.

* Clone the project on a machine with AWS cli installed and configured.

* Execute the following command to upload the lambda function to the artefactory bucket

```aws cloudformation package --template-file VODImgResize.yml --s3-bucket ArtefactoryBucket --output yaml > packaged-template.yaml```

* Execute the following command to deploy the infrastructure using cloud formation

```aws cloudformation create-stack --stack-name YOURSTACKNAME --template-body file://packaged-template.yaml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM```

* Open AWS console and check that the deployment is ok. In the Output tab, you have the url of the website to use.

* Copy an image (Agent 327 movie poster is given as an example) in the newly created S3 bucket.
  * The resized image will be accessible under the following URL: http://websiteurl/WIDTHxHEIGHT/imagename.jpg
  * There is also a reference algorithm which crop the image from its center accessible under the following url: http://websiteurl/center/WIDTHxHEIGHT/imagename.jpg
  * By default, the system will only resize to the following resolutions: 1080x1440, 800x600, 600x1080 and 720x480
  * Additional resolutions can be added in the AWS lambda environment variable "ALLOWEDRESOLUTION". If ALLOWEDRESOLUTION is removed, all resolutions will be allowed.
  
### Optional:
You can copy the index.html file and the JS folder located in the www folder at the root of the S3 bucket containing the images. It will install a monitoring tool to be used only for tests purposes. The monitoring tool will display all the images cropped in the 4 initial resolutions. If you want to display only one image, add the parameter ?img=imagename.jpg .

The monitoring tool can be accessed using the following url: http://websiteurl/index.html.
