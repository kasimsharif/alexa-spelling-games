"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Word Game " \
                    "Please Confirm to start the game by saying yes or no " \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please Confirm to start the game by saying yes or no"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_word_attributes(selected_word):
    return {"selectedWord": selected_word}


def get_word_list():
    return random.choice([
        "acceptable",
        "accidentally",
        "accommodate",
        "acquire",
        "acquit",
        "amateur",
        "arctic",
        "apparent",
        "argument",
        "atheist",
        "believe",
        "bellwether",
        "calendar",
        "cemetery",
        "conscience",
        "convalesce",
        "column",
        "handkerchief",
        "indict",
        "rhythm",
        "playwright",
        "embarrass",
        "millennium",
        "pharaoh",
        "liaison",
        "supersede",
        "ecstasy",
        "harass",
        "maintenance",
        "occurred",
        "recommend",
        "deductible"
    ])


def check_spelling(intent, session):
    """ Check the spelling of the word
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    if 'Spelling' in intent['slots']:
        spelling = intent['slots']['Spelling']['value']
        if spelling.lower() == session['attributes']['selectedWord'].lower():
            next_word = get_word_list()
            session_attributes = create_word_attributes(next_word)
            speech_output = "Great !! Correct Spelling! Next Word " + next_word + "."

            reprompt_text = "Great !! Correct Spelling! Next Word " + next_word + "."

        else:
            speech_output = "Oops Sorry Answer!! Bye Bye"

            reprompt_text = "Oops Sorry Answer!! Bye Bye"

            should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def repeat_word(intent, session):
    """ Repeating the word
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    selected_word = session['attributes']['selectedWord']
    session_attributes = create_word_attributes(selected_word)


    speech_output = selected_word

    reprompt_text = selected_word

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def next_word(intent, session):
    """ Next word
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    selected_word = get_word_list()
    session_attributes = create_word_attributes(selected_word)

    speech_output = "Next word " + selected_word + "."

    reprompt_text = "Next word "+ selected_word + "."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_confirmation(intent, session):
    """ Set your confirmation by saying Yes or No
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    selected_word = get_word_list()
    session_attributes = create_word_attributes(selected_word)
    if 'Confirm' in intent['slots']:
        confirmation = intent['slots']['Confirm']['value']
        if confirmation == "yes":
            speech_output = "Thanks for confirmation. "  \
                            "Lets Begin the Game, While Responding, 'Say Answer, and then spell the Word'. " \
                            "First Word, 'Spell " + selected_word + "'."
            reprompt_text = "Thanks for confirmation. "  \
                            "Lets Begin the Game, While Responding, 'Say Answer, and then spell the Word'. " \
                            "First Word, 'Spell " + selected_word + "'."
        else:
            speech_output = "Oops Sorry to hear you don't want to Play." \
                        "Bye Bye, Hope to meet with you soon"
            reprompt_text = "Oops Sorry to hear you don't want to Play." \
                        "Bye Bye, Hope to meet with you soon"
            should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ConfirmYesOrNo":
        return get_confirmation(intent, session)
    elif intent_name == "CheckSpelling":
        return check_spelling(intent, session)
    elif intent_name == "RepeatWord":
        return repeat_word(intent, session)
    elif intent_name == "NextWord":
        return next_word(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

