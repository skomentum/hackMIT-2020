import urllib.request
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import math

# list of all tonal pitches pleasurable to the human ear
notesList = [207.65, 220, 233.08, 246.94,
             261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.3, 440, 466.16, 493.88, 523.25, 554.37,
             587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880, 932.33, 987.77, 1046.5, 1108.73, 1174.66,
             1244.51, 1318.51, 1396.91, 1479.98]

def pitches(starList):
    # function to convert star coordinates to tonal pitches
    starpitches = []
    for i in range(len(starList)):
        x = int(starList[i][1])
        y = int(starList[i][2])
        magnitude = math.sqrt(x * x + y * y)
        starpitches.append(int(magnitude % len(notesList)))
    return starpitches

def music(starList):

# Creates an empty AudioSegment
    result = AudioSegment.silent(duration=0)

#temporary data set of star coordinates
#starList = [[4, 500, 800],
#            [3, 2000, 4250],
#            [2, 3453, 7532],[5, 3474, 2346],[1, 24345, 2457],[3, 500, 800], [6, 9876, 3465]]


#gets pitches array from pitches function
    stars = pitches(starList)
    for n in range(len(stars)):
        print(notesList[stars[n]])
        # shifts values over 1.44 so that the min is 0 and the max is 22.44
        time = 200 #default note duration in case it doesn't reach an "if" statement
        brightness = float(starList[n][0]) + 1.44
        # Generate a sine tone with frequency 200 * n
        gen = Sine(notesList[stars[n]])
        #Optional: change the duration of the sounds based on how bright the star is

        if brightness >= 0 and brightness < 1:
            time = 200
        if brightness >= 1 and brightness < 2:
            time = 200
        if brightness >= 2 and brightness < 3:
            time = 200
        if brightness >= 3 and brightness < 4:
            time = 300
        if brightness >= 4 and brightness < 5:
            time = 300
        if brightness >= 5 and brightness < 6:
            time = 300
        if brightness >=6 and brightness <7:
            time = 300

        # AudioSegment with duration 200ms, gain -3
        sine = gen.to_audio_segment(duration=time).apply_gain(-3)
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
