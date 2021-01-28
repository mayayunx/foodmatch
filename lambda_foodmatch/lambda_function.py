# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


import requests
import json
import pandas as pd
import boto3
# Load restaurant json file under the same directory as lambda function
df = pd.read_json('res.json', lines=True)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Food Match! What kind of food do you wish for today?"
        reprompt_text = "I don't know a good restaurant for that, do you want to try anything else?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class CaptureFoodTypeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureFoodTypeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        foodtype = slots["foodtype"].value.lower()
        restaurant, comment = "", ""

        df_filter = df[(df['type'].str.contains(foodtype, na=False))]

        # If no match
        if df_filter.empty:
            reprompt_text = "I don't know any good restaurants for {foodtype}. Do you want to try anything else?".format(foodtype=foodtype)
            return (
                handler_input.response_builder
                    .speak(reprompt_text)
                    .ask(reprompt_text)
                    .response
            )

        # If match
        result = df_filter.sample(1)
        session_attr["comment"] = result['text'].values[0]
        restaurant = result['name'].values[0]
        session_attr["restaurant"] = restaurant
        speak_output = "It's a match! I found you a restaurant to have {foodtype}. It is called {restaurant}. Have you been there? Leave a review for it if yes, then I can rate the restaurant for you!".format(foodtype=foodtype, restaurant=restaurant)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
    
    
class GiveReviewIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GiveReviewIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        comment = session_attr["comment"]
        speak_output = "Here's my review: {comment}".format(comment=comment)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CaptureReviewIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureReviewIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        review = slots["review"].value
        session_attr = handler_input.attributes_manager.session_attributes

        # Change to your instance's address
        IPv4_adress = "18.197.167.241"
        url = f"http://{IPv4_adress}:8000/predict"
        data = {"data":"\""+str(review)+"\""}
        r = requests.post(url, data = json.dumps(data))
        resp = r.json()
        stars = resp["data"]
        speak_output = "I will give the restaurant {stars} star based on your review.".format(stars=stars)


        # Block for saving the review, need to setup access point on s3 before using
        '''
        data = {}
        data['restaurant'] = session_attr['restaurant']
        data['comment'] = str(review)
        data['stars'] = stars
        file = open('/tmp/rate.json', 'a')
        file.write(json.dumps(data) + '\r\n')
        file.close()

        with open('/tmp/rate.json') as f:
            string = f.read()
        utfstr = string.encode('utf-8')

        s3 = boto3.resource("s3")
        s3.Bucket('foodmatch').put_object(Key='rate/rate.json', Body=utfstr)
        '''


        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureFoodTypeIntentHandler())
sb.add_request_handler(GiveReviewIntentHandler())
sb.add_request_handler(CaptureReviewIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()