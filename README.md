# TUM WS20/21 Applied Deep Learning NLP Seminar
## Team of Food Match Repository

### How to use the notebook
- Follow instructions in the notebook
- Note that the res.json for lambda function is joined manually, the value of type attribute should use all lowercase letter to be matched sucessfully

### How to use docker to deploy sentiment analysis model
- Have docker installed on target computer
- In docker_foodmatch, build docker image and upload it if necessary
- Start docker image, note that if the system does not have enough memory, it'll get stuck at allocation of memory exceeding limit
- One can add swap file on Linux manually, reference: https://docs.alfresco.com/3.4/tasks/swap-space-lin.html 
- Prepare curl commands for testing, example: curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Contenication/json" -d "{\"data\":\"This Restaurant is bad\"}"

### How to use lambda function
- Have Python 3 installed
- In lambda foodmatch, use pip to download ask-sdk package
- Additionally, if you're on Linux system, directly install numpy and pandas package; otherwise, one needs to download the Linux distribution of two libraries from
- https://files.pythonhosted.org/packages/b1/e1/8c4c5632adaffc18dba4e03e97458dc1cb00583811e6982fc620b9d88515/numpy-1.19.5-cp37-cp37m-manylinux1_x86_64.whl
- https://files.pythonhosted.org/packages/7a/c2/339e302d4122cb8b166aecc823afed4af6b2193f040f2656eea77d174146/pandas-1.2.1-cp37-cp37m-manylinux1_x86_64.whl
- Also pip install pytz as well
- Unpack them and paste in lambda function folder
- Change line 113's IP address accordingly if you want to use score prediction part
- Compress all files, this part we should have 44 items
- Upload it to lambda function panel on AWS, choose runtime of Python 3.7

### Alexa developer console setup
- Set the endpoint to AWS lambda function, also add trigger of Alexa skill in lambda
- Create intents, including
- GiveReviewIntent, sample utterances like "no", "no I haven't been there" or anything similar
- CaptureReviewIntent, sample utterances like "yes {review}", "I think {review}" or anything include {review} in between, add one intent slot review, slot type of AMAZON.SearchQuery, speech prompt "What is your review for the restaurant?" and turn on "Is this slot required to fulfill the intent?"
- CaptureFoodTypeIntent, sample utterances should have {foodtype}, add one intent slot foodtype of type AMAZON.Food, also turn on "Is this slot required to fulfill the intent?", speech prompt like "I want to eat Japanese today, and you?"
- Next, under "Slot Types" panel, add slot value for food type, all should be in lowercase letter
- Build the model! And test!
