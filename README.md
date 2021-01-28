# TUM WS20/21 Applied Deep Learning NLP Seminar
## Team of Food Match Repository

### How to Use The Notebook
- Follow instructions in the notebook
- Note that the res.json for lambda function is joined manually, the value of type attribute should use all lowercase letter in order to be matched sucessfully

### How to Use Docker to Deploy Sentiment Analysis Model
- Have docker installed on target computer
- Start docker service by 'sudo systemctl start docker' and 'sudo service docker start' (omit quotes, same for commands below)
- In docker_foodmatch, build docker image and upload it if necessary
- For example, run 'docker build --file Dockerfile --tag foodmatch .'
- Start docker image, note that if the system does not have enough memory, it'll get stuck at allocation of memory exceeding limit
- Command like 'docker run -p 8000:8000 foodmatch'
- One can add swap file on Linux system manually, reference: https://docs.alfresco.com/3.4/tasks/swap-space-lin.html 
- Prepare curl commands for testing, example: curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Contenication/json" -d "{\"data\":\"This Restaurant is bad\"}"

### How to Use Lambda Function
- Have Python 3.7 and pip installed
- In lambda foodmatch, use pip to download ask-sdk package in the directory
- Command like 'pip install ask-sdk -t .'
- Additionally, if you're on Linux system, directly install numpy and pandas package; otherwise, one needs to download the Linux distribution of two libraries from
- https://files.pythonhosted.org/packages/b1/e1/8c4c5632adaffc18dba4e03e97458dc1cb00583811e6982fc620b9d88515/numpy-1.19.5-cp37-cp37m-manylinux1_x86_64.whl
- https://files.pythonhosted.org/packages/7a/c2/339e302d4122cb8b166aecc823afed4af6b2193f040f2656eea77d174146/pandas-1.2.1-cp37-cp37m-manylinux1_x86_64.whl
- - Unpack them and paste in lambda function folder
- Also do 'pip install pytz -t .'
- Change line 113's IP address accordingly if you want to use score prediction part
- Compress all files, this part we should have 44 items
- Upload it to lambda function panel on AWS, choose runtime of Python 3.7

### Alexa Developer Console Setup
- Set the endpoint to AWS lambda function, also add trigger of Alexa skill in lambda
- Create intents, including
- GiveReviewIntent, sample utterances like "no", "no I haven't been there" or anything similar
- CaptureReviewIntent, sample utterances like "yes {review}", "I think {review}" or anything include {review} in between, add one intent slot review, slot type of AMAZON.SearchQuery, speech prompt "What is your review for the restaurant?" and turn on "Is this slot required to fulfill the intent?"
- CaptureFoodTypeIntent, sample utterances should have {foodtype}, add one intent slot foodtype of type AMAZON.Food, also turn on "Is this slot required to fulfill the intent?", speech prompt like "I want to eat Japanese today, and you?"
- Next, under "Slot Types" panel, add slot value for food type, all should be in lowercase letter
- Build the model! And test!

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
