
import random
import time 
import speech_recognition as sr
import playsound
import serial

from playsound import playsound
from random import randint

serialPort = serial.Serial(port = "COM8", baudrate=9600,
                          bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def send_to_arduino(data):
    if not serialPort.is_open: 
        serialPort.open()
    if type(data) == str:
        data = data.strip()
        my_data = data.encode("ascii")
        print(my_data)
        print("Sending: '" + data + "' to serial port.")
        serialPort.write(my_data)
        serialPort.close()

def soundOff(test): #Selects a random voiceline to play when triggered
        value = randint(1, 5) #random number from 1-5

        #value = 6 #Set up for when I do that certain bits in the video
        
        if(test == 0):
            value = 0 #If selecting the test option, only plays the first sound
        if value == 0:
            playsound('Conspiracy Theory.mp3')
        elif value == 1:
            playsound('Ay yo ma.mp3')
        elif value == 2:
            playsound('Oh God.mp3')
        elif value == 3:
            playsound('Petrified.mp3')
        elif value == 4:
            playsound('Spooky.mp3')
        elif value == 5:
            playsound('Forsaken.mp3')
        elif value == 6:
            playsound('Lemons.mp3')
        elif value == 7:
            playsound('Nightmare.mp3')



if __name__ == "__main__":
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # format the instructions string
    instructions = "Start sayin something\n"

    # show instructions and wait 3 seconds before starting the game
    print(instructions)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Speak!'.format(i+1))
            voice = recognize_speech_from_mic(recognizer, microphone)
            if voice["transcription"]:
                break
            if not voice["success"]:
                break
            print("No Voice Detected :(\n")

        # if there was an error, stop the game
        if voice["error"]:
            print("ERROR: {}".format(voice["error"]))
            break

        # show the user the transcription and turn it into a String
        voiceStr = str(voice["transcription"]).lower()
        print("You said: " + voiceStr)

        #incriments down from 2->0
        user_has_more_attempts = i < NUM_GUESSES - 1

        

        #Substrings to try and find specific words in voiceStr
        triggerWords = ["trigger", "global warming", "ex girlfriend", 
                        "depression", "upsetti spaghetti", "i hate you"
                        , "taxes", "father", "i have a gun", ""]
        if any(word in voiceStr for word in triggerWords): #Checks for trigger words in User's voice input
            print("I'm triggered....\n")
            send_to_arduino('a')  #Sending the String "a" if it is a trigger word
            soundOff(1)
        elif(voiceStr is "test" or "testing"):
            print("Test Sequence Initiated")
            send_to_arduino("b")
            soundOff(0)

        if user_has_more_attempts:
            print("Cool beans\n")
        else:
            print("\nTime is up m8")
            break

        serialPort.close()