import json
import typing

from textblob import TextBlob

def get_polarity(event, context) -> json:
    '''
        Receive a json and return the feeling of the input.
        
        Parameters:
        - event: dict, required
        The event object that contains the input to the Lambda function. 
        
        - context: object, required
        The context object provided by AWS Lambda, containing metadata and runtime information.
        
        Returns:
        - json:
            Received sentence
            The polarity returned by TextBlob
            The Feeling of the sentence: 
                - < -0.8 : Negative sentiment
                - > -0.8 and < 0.2 : Neutral Sentiment 
                - > 0.2 : Positive sentiment
    '''

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary.")
    
    body = event.get("body")
    if not body:
        return {
            "Error": "Invalid input: no body found."
        }

    try:
        json_body = json.loads(body)
    except json.JSONDecodeError:
        return {
            "Error": "Invalid input: unable to parse JSON body."
        }
    sentence = json_body.get("sentence")
    
    if not isinstance(sentence, str):
        return {
            "Error": "Invalid input: 'sentence' must be a string."
        }

    blob = TextBlob(sentence)
    polarity = blob.polarity
    if(polarity < -0.8):
        feeling = "Negative"
    elif(polarity > 0.2):
        feeling = "Positive"
    else:
        feeling = "Neutral"

    return {
        "sentence": sentence,
        "polarity": polarity,
        "feeling":feeling
    }