import os

from flask import send_file
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import math

# list of all tonal pitches pleasurable to the human ear
notesList = [207.65, 220, 233.08, 246.94,
             261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392, 415.3, 440, 466.16, 493.88, 523.25, 554.37,
             587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880, 932.33, 987.77, 1046.5, 1108.73, 1174.66,
             1244.51, 1318.51, 1396.91, 1479.98]


def pitches(star_list):
    # function to convert star coordinates to tonal pitches
    star_pitches = []
    for i in range(len(star_list)):
        x = int(star_list[i][1])
        y = int(star_list[i][2])
        magnitude = math.sqrt(x * x + y * y)
        star_pitches.append(int(magnitude % len(notesList)))
    return star_pitches


def generate_music(star_list):
    # Creates an empty AudioSegment
    result = AudioSegment.silent(duration=0)

    # temporary data set of star coordinates
    # starList = [[4, 500, 800],
    #            [3, 2000, 4250],
    #            [2, 3453, 7532],[5, 3474, 2346],[1, 24345, 2457],[3, 500, 800], [6, 9876, 3465]]

    # gets pitches array from pitches function
    stars = pitches(star_list)
    if len(stars) > 500:
        limit = 100
    else:
        limit = len(stars)
    for n in range(limit):
        # shifts values over 1.44 so that the min is 0 and the max is 22.44
        time = 200  # default note duration in case it doesn't reach an "if" statement
        brightness = float(star_list[n][0]) + 1.44
        # Generate a sine tone with frequency 200 * n
        gen = Sine(notesList[stars[n]])
        # Optional: change the duration of the sounds based on how bright the star is
        """
        if 0 <= brightness < 1:
            time = 200
        elif 1 <= brightness < 2:
            time = 200
        elif 2 <= brightness < 3:
            time = 200
        elif 3 <= brightness < 4:
            time = 300
        elif 4 <= brightness < 5:
            time = 300
        elif 5 <= brightness < 6:
            time = 300
        elif 6 <= brightness < 7:
            time = 300
            """

        # AudioSegment with duration 200ms, gain -3
        sine = gen.to_audio_segment(duration=time).apply_gain(-3)
        # Fade in / out
        sine = sine.fade_in(50).fade_out(100)
        # Changes the volume based on the brightness of the star

        if 0 <= brightness < 1:
            sine += 10
        elif 1 <= brightness < 2:
            sine += 9
        elif 2 <= brightness < 3:
            sine += 8
        elif 3 <= brightness < 4:
            sine += 7
        elif 4 <= brightness < 5:
            sine += 6
        elif 5 <= brightness < 6:
            sine += 5
        elif 6 <= brightness < 7:
            sine +=4
        # Append the sine to our result
        result += sine
    # save the result as an mp3 file
    result.export("./static/music.mp3", format="mp3")
