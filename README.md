# VOD-Image-Resize-CloudFront
An AWS project using AWS Rekognition to smartly crop images and AWS Cloudfront to distribute content

## Description

Resizes images on the fly using an AWS server less architecture.

If the final size does not have the same image ratio, the image is cropped using a smart strategy based on AWS Rekognition text and face detection.

Interesting feature is that the image is only processed once and stored on S3 for future use.

The crop strategy configured in this project is particularly suited to crop movie posters.

## Architecture
![Image of Architecture](https://github.com/vikingen13/VOD-Image-Resize-CloudFront/blob/master/Doc/ImageResize.png)

## Usage
The project deployment is done using AWS Cloud Formation.

* Clone the project on a machine with AWS cli installed and configured.

* First create a bucket to store the artifact by running "make createbucket" .

* Deploy the infrastructure by running "make deploy"

* Deploy the demo web site by running "make deploy-site"

* Copy an image (Agent 327 movie poster is given as an example) in the created S3 bucket.
  * The resized image will be accessible under the following URL: http://cloudfronturl/WIDTHxHEIGHT/imagename.jpg
  * There is also a reference algorithm which crop the image from its center accessible under the following url: http://cloudfronturl/center/WIDTHxHEIGHT/imagename.jpg
  * By default, the system will only resize to the following resolutions: 1080x1440, 800x600, 600x1080 and 720x480
  * Additional resolutions can be added in the AWS lambda environment variable "ALLOWEDRESOLUTION".
  
* You can also copy several movie posters in the S3 bucket originals by running "Make copy-pictures". 

### Demo Web Site:
The demo web site is provided for demonstration purposes. it displays all the images cropped in the 4 initial resolutions. If you want to display only one image, add the parameter ?img=imagename.jpg .

The demowebsite tool can be accessed using the following url: http://cloudfronturl/index.html.
