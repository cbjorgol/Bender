import subprocess
import sys

def speak(message=None, language='en-us', speed=175, pitch_adj=25,
          capitals=40, word_gap='20ms', amplitude=180):
    """
    Use espeak for text-to-speech translation

    Parameters
    ----------
    message : str, optional, (default = None)
        message to translate to speech
    language : str, optional, (default='en-us')
        language to use for voice
    speed : int, optional (default=135)
        speed in words per minute, 80 to 450, default is 135
    pitch_adj : int, optional (default=1)
	Pitch adjustment, 0 to 99
    capitals : int, optional (default=30)
        Pitch increase for capital letters
    word_gap : str, optional (default='30ms')
        word gap.  pause between words, units of 10mS
    amplitude : int, optional (default=180)
        Amplitude, 0 to 200 
    """
    
    if message is None:
        message = 'You did not give me anyting to say'

    language = '-v'+language
    speed = '-s'+str(speed)
    pitch_adj = '-p'+str(pitch_adj)
    capitals = '-k'+str(capitals)
    word_gap = '-g'+str(word_gap)
    amplitude = '-a'+str(amplitude)

    subprocess.call([
        'sudo', 
        'espeak', 
        language, 
        speed, 
        pitch_adj,
        capitals,
        #word_gap,
        #amplitude,
        '"'+message+'"',
    ])


if __name__ == '__main__':

    if len(sys.argv) > 1:
        speak(message=sys.argv[1])
    else:
        speak(message='hello, world')
