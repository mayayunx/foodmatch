# TUM WS20/21 Applied Deep Learning NLP Seminar
## Team of Food Match Repository

### Introduction
* This is a project of developing an Alexa skill of
    * Recommending restaurants based on input food type (e.g., Japanese, Chinese, Vegetarian) with machine generated comments for recommendation
    * Predicting and rating user's review automatically online
---
### System Architecture
- Download Yelp dataset, do some pre-processing to parse out useful data
- Train different models for text generation of food types, and generate some comment to create ```res.json``` for lambda function to use
- Use NLPRule to check and correct possible grammatical errors for the comments
- Train a live sentiment analysis model and combine it to use with docker
- Build a docker image, install required libraries, push it to AWS
- Create lambda function and compress it with essential packages, upload it to AWS lambda function console
- Establish the Alexa skill and configure content
- Start an instance on EC2, install docker and pull back the image, run it as a backend
- If user gives review, store it in ```tmp``` folder in lambda function, then upload it to Simple Storage Service (S3)
---
### How to Use The Notebook
- Follow instructions in the notebook
- Note that the ```res.json``` for lambda function is joined manually, the value of type attribute should use all lowercase letter in order to be matched sucessfully
---
### How to Use Docker to Deploy Sentiment Analysis Model
- Due to large size of the score prediction model, one can download it via [text_classification_modelv3](https://drive.google.com/drive/folders/1MFmLfYniSQcMo9CN4RL1JrHWl3dS80WB?usp=sharing).
- Then place the whole folder under ```api/ml/text_classification_modelv3```
- Inside ```text_classification_modelv3``` folder, it should have: ```config.json```, ```tf_model.h5```
- Have docker installed on target computer
- Start docker service by ```sudo systemctl start docker``` and ```sudo service docker start``` (omit quotes, same for commands below)
- In docker_foodmatch, build docker image and upload it if necessary
- For example, run ```docker build --file Dockerfile --tag foodmatch .```
- Start docker image, note that if the system does not have enough memory, it'll get stuck at allocation of memory exceeding limit
- Run with ```docker run -p 8000:8000 foodmatch```
- One can add swap file on Linux system manually, reference: [Adding swap space in Linux](https://docs.alfresco.com/3.4/tasks/swap-space-lin.html)
- Prepare curl commands for testing, example: ```curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Contenication/json" -d "{\"data\":\"This Restaurant is bad\"}"```
---
### How to Use Lambda Function
- Have Python 3.7 and pip installed
- In lambda_foodmatch, use pip to download ask-sdk package in the directory by```pip install ask-sdk -t .```
- Additionally, if you're on Linux system, directly install numpy and pandas package
- ```pip install numpy -t .```
- ```pip install pandas -t .```
- Otherwise, one needs to download the Linux distribution of two libraries from
- [NumPy v1.19.5 Python 3.7 Linux Distribution](https://files.pythonhosted.org/packages/b1/e1/8c4c5632adaffc18dba4e03e97458dc1cb00583811e6982fc620b9d88515/numpy-1.19.5-cp37-cp37m-manylinux1_x86_64.whl)
- [Pandas v1.2.1 Python 3.7 Linux Distribution](https://files.pythonhosted.org/packages/7a/c2/339e302d4122cb8b166aecc823afed4af6b2193f040f2656eea77d174146/pandas-1.2.1-cp37-cp37m-manylinux1_x86_64.whl)
- Unpack and paste them in lambda function folder
- Also do ```pip install pytz -t .```
- Change lambda function file line 114's IP address accordingly if you want to use score prediction part
- Compress all files, this part the zip file should contain 44 items
- Upload it to lambda function panel on AWS, choose runtime of Python 3.7
---
### Alexa Developer Console Setup
- Set the endpoint to AWS lambda function, also add trigger of Alexa skill in lambda
- Create intents, including
- ```GiveReviewIntent```, sample utterances like ```no```, ```no I haven't been there``` or anything similar
- ```CaptureReviewIntent```, sample utterances like ```yes {review}```, ```I think {review}``` or anything include ```{review}``` in between, add one intent slot review, slot type of ```AMAZON.SearchQuery```, speech prompt ```What is your review for the restaurant?``` and turn on ```Is this slot required to fulfill the intent?```
- ```CaptureFoodTypeIntent```, sample utterances should have ```{foodtype}```, add one intent slot foodtype of type ```AMAZON.Food```, also turn on ```Is this slot required to fulfill the intent?```, speech prompt like ```I want to eat Japanese today, and you?```
- Next, under ```Slot Types``` panel, add slot value for food type, all should be in lowercase letter
- Build the model! And test!
---
### Example Results
- Ask recommendation for a sushi restaurant
<img src="https://github.com/mayayunx/foodmatch/blob/main/Example/sushi%20no.png" width="512">

- Ask recommendation for a pizza restaurant
<img src="https://github.com/mayayunx/foodmatch/blob/main/Example/pizza%20no.png" width="512">

- User rating of score 5 to burger restaurant
<img src="https://github.com/mayayunx/foodmatch/blob/main/Example/burger%205.png" width="512">

- User rating of score 3 to korean restaurant
<img src="https://github.com/mayayunx/foodmatch/blob/main/Example/korean%203.png" width="512">

- User rating of score 0 to asian fusion restaurant
<img src="https://github.com/mayayunx/foodmatch/blob/main/Example/asian%20fusion%200.png" width="512">

---
### Remark
- For AWS free tier's EC2 instance, the default memory for the score prediction model is definitely not enough. One can use swap files technique to add more by trading off some disk space
- Training of two models with huge yelp dataset take time, however, even with few epochs, the results are already acceptable
- Lambda function environment is a read-only file system, so it's not able to write files on it. One can use ```tmp``` folder in lambda function to write files temporarily, the content is not guaranteed to be stored for long time and could disapper in any minute. As our project use, one can uplolad it to S3, or send it to backend server for proper saving
- In order to use S3 normally, first create an access point for the lambda function in S3 webpage, add the ARN id of lambda function
- In IAM management console, add new policies: ```AmazonS3FullAccess```, ```AWSLambdaExecute``` and attach this role to lambda function
- In ```res.json```, do not type any comments; make sure the text is regular, do not comprise multiple punctuations e.g. ```...```, ```!!!```, this will make Alexa unable to process and throw an error
