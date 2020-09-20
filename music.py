import urllib.request
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import ffmpeg

# Creates an empty AudioSegment
result = AudioSegment.silent(duration=0)

# # boost volume by 6dB
# beginning = first_10_seconds + 6
#
# # reduce volume by 3dB
# end = last_5_seconds - 3
# range is 21.0 to 26.7

# if reading in a file - nvm. NOT reading in a file
# request info (data) from an API and we transform it into cartesian coordinates,
    # and then that is passed directly to this file
# passed as a list of stars (specific stars to include already determined; everything passed in will be played)
    #  each star has an x-coord, y-coord, and brightness
# (stars could be organized as objects of a class but would make it more complex... or organized)
# a 2D list will be passed in: columns are (currently) 1) brightness, 2) a degrees 3) dec degrees
    # need to convert the 2nd/3rd list items into x and y coordinates

# sort list into least x-coord to greatest x-coord so sound plays in order of stars across the screen
    # once sorted, call music function on each star in ordered list

# convert and sort coordinates at the same time, return a 2D list. Pass 2D list into Katherine's music function

# we will call a function to get the list of stars from the API
# copy and paste file from Cade into a star list


# Loop over 1-13 because this is the range that sounds pleasing to hear
brightness = 18
for n in range(4, 8):              # for star in group/list of stars passed in - range is 0 to list length
    brightness = brightness + n
    # Generate a sine tone with frequency 200 * n
    gen = Sine(200 * n)
    # AudioSegment with duration 200ms, gain -3
    sine = gen.to_audio_segment(duration=200).apply_gain(-3)
    # Fade in / out
    sine = sine.fade_in(50).fade_out(100)
    # Changes the volume based on the brightness of the star

    if 21 <= brightness < 22:
        sine = sine
    if 22 <= brightness < 23:
        sine = sine + 10
    if 23 <= brightness < 24:
        sine = sine + 20
    if 24 <= brightness < 25:
        sine = sine + 30
    if 25 <= brightness < 26:
        sine = sine + 40
    if 26 <= brightness < 27:
        sine = sine + 50

    # Append the sine to our result
    result += sine
# Play the result
play(result)
# save the result as an mp3 file
result.export("test.mp3", format="mp3")
