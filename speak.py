import os
import sys

def speak(message=None, language='en-us', speed=175, pitch_adj=25,
          capitals=40, word_gap='20ms', amplitude=180):
    """
    Use festival for text-to-speech translation

    Parameters
    ----------
    message : str, optional, (default = None)
        message to translate to speech
    """
    
    if message is None:
        message = 'You did not give me anyting to say'

    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        # linux
        os.system('echo "' + str(message) + '" | festival --tts')

    elif _platform == "darwin":
        # OS X
        os.system('say "' + str(message) + '"')

    elif _platform == "win32":
        # Windows...
        print("Windows not supported")


if __name__ == '__main__':

    if len(sys.argv) > 1:
        speak(message=sys.argv[1])
    else:
        speak(message='hello, world')
