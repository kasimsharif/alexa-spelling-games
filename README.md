# Alexa Skill Set - Spelling Games
Spelling games Skill set for Alexa

This Lambda function is for custom skill set for Alexa written in python 2.7

I have created following Intents:

1. ConfirmYesOrNo -  For confirming to play spelling games.
2. CheckSpelling -  To check the spelling of the word.
3. RepeatWord -  Repeating the same word again.
4. NextWord - Asking for some other word.

## Understanding the lambda functions

### Welcome Response

When I say **Alexa, Open Spelling Games** this the following function which gets triggered

Alexa : " Welcome to the Word Game , Please Confirm to start the game by saying yes or no"

    ```def get_welcome_response():                                                                          
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
        card_title, speech_output, reprompt_text, should_end_session))```
        
### Confirming the Response

Confirm the response by saying YES/NO

```def get_confirmation(intent, session):                                                               
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
```                                                                                                  
                             
                                                                     
If you confirm as **YES** games starts and Alexa gives you first word to spell, if you say **NO** game ends.

### Check the Spellings

To Answer the Spelling Say **Answer, <!Spell that word>** (Utterance defined for this Intent), Prefixing **Answer** before spelling the word.

Following Function check the spelling. If correct spelling it give new random word:
get_word_list() -  list of words
Store that word in session attribute 
                                                                                                     
```def check_spelling(intent, session):                                                                 
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
```

### Repeat the word

To make alexa repeat the same say **Repeat the word** (Utterance defined for this Intent)

```def repeat_word(intent, session):                                                                    
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
```

### Next Word

Make Alexa to say new word, say **Next Word** (Utterance defined for this Intent)

```def next_word(intent, session):                                                                      
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
```
        
        
