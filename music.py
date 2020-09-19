import urllib.request
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import ffmpeg

# Creates an empty AudioSegment
result = AudioSegment.silent(duration=0)

# Loop over 0-14
for n in range(15):
    # Generate a sine tone with frequency 200 * n
    gen = Sine(200 * n)
    # AudioSegment with duration 200ms, gain -3
    sine  = gen.to_audio_segment(duration=200).apply_gain(-3)
    # Fade in / out
    sine = sine.fade_in(50).fade_out(100)
    # Append the sine to our result
    result += sine
# Play the result
play(result)