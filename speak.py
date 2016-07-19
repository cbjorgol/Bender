import os
import sys
import six

from sys import platform as _platform

def speak(message):
    """
    Use festival for text-to-speech translation

    Parameters
    ----------
    message : str, optional, (default = None)
        message to translate to speech
    """
    
    if message is None:
        message = 'You did not give me anyting to say'
    else:
        if not isinstance(message, six.string_types):
            message = "Non text data"



    if _platform == "linux" or _platform == "linux2":
        # linux
        os.system('echo "' + str(message) + '" | festival --tts')

    elif _platform == "darwin":
        # OS X
        os.system('say "' + str(message) + '"')

    elif _platform == "win32":
        # Windows...
        print("Windows not supported")

def clean_text(text):
    pass

if __name__ == '__main__':

    if len(sys.argv) > 1:
        speak(message=sys.argv[1])
    else:
        speak(message='hello, world')
