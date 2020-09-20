import urllib.request
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import math

# list of all tonal pitches
notesList = [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185, 196, 207.65, 220, 233.08, 246.94,
             261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.3, 440, 466.16, 493.88, 523.25, 554.37,
             587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880, 932.33, 987.77, 1046.5, 1108.73, 1174.66,
             1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760, 1864.66, 1975.53, 2093, 2217.46, 2349.32,
             2489.02]

def pitches():
    # function to convert star coordinates to tonal pitches
    starpitches = []
    for i in range(len(starList)):
        x = int(starList[i][1])
        y = int(starList[i][2])
        magnitude = math.sqrt(x * x + y * y)
        starpitches.append(int(magnitude % len(notesList)))
    return starpitches

# Creates an empty AudioSegment
result = AudioSegment.silent(duration=0)

#temporary data set of star coordinates
starList = [[600, 500, 800],
            [3000, 2000, 4250],
            [2760, 4500, 2431]]


#gets pitches array from pitches function
stars = pitches()
for n in range(len(stars)):
    # shifts values over 1.44 so that the min is 0 and the max is 22.44
    brightness = float(starList[n][0]) + 1.44
    # Generate a sine tone with frequency 200 * n
    gen = Sine(notesList[stars[n]])
    # AudioSegment with duration 200ms, gain -3
    sine = gen.to_audio_segment(duration=200).apply_gain(-3)
    # Fade in / out
    sine = sine.fade_in(50).fade_out(100)
    # Changes the volume based on the brightness of the star

    if brightness >= 0 and brightness < 1:
        sine += 60
    if brightness >= 1 and brightness < 2:
        sine += 40
    if brightness >= 2 and brightness < 3:
        sine += 20
    if brightness >= 3 and brightness < 4:
        sine = sine
    if brightness >= 4 and brightness < 5:
        sine -= 20
    if brightness >= 5 and brightness < 6:
        sine -= 40
    if brightness >=6 and brightness <7:
        sine -= 60

    # Append the sine to our result
    result += sine
# Play the result
play(result)
# save the result as an mp3 file
result.export("test.mp3", format="mp3")
