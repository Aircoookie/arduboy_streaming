# MIT License

# Copyright (c) 2021 Christian Schwinne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import moviepy.editor as mp
import serial
import time
from timeit import default_timer as timer

COMPORT = 'COM6' # Arduboy com port
VWIDTH = 128 # Width of the video on the Arduboy screen
OWIDTH = 128 # Width of the Arduboy screen
HEIGHT = 64 # Height of the Arduboy screen
THRES = 128 # Values below are treated as black, above as white
CHAN = 0 # Color channel to get values from (0=red,1=green,2=blue)
XOFFSET = (OWIDTH - VWIDTH) >> 1

ser = serial.Serial()
ser.baudrate = 500000
ser.port = COMPORT
ser.open()

clip = mp.VideoFileClip('badapple.mp4')
clip_resized = clip.resize((VWIDTH,HEIGHT))
print('%d FPS' % clip_resized.fps)
frametime = 1000 / clip_resized.fps
# clip_resized.write_videofile("movie_resized.mp4")
# iterating frames 
frames = clip_resized.iter_frames() 
  
# # counter to count the frames 
counter = 0

arr = bytearray(int(OWIDTH*HEIGHT/8 +5))
for i in range(int(OWIDTH*HEIGHT/8 +5)):
  arr[i] = 0

arr[0] = 118 #'v'
arr[1] = VWIDTH
arr[2] = HEIGHT
arr[3] = 0
arr[4] = 0
start = timer()
  
# # using loop to tranverse the frames 
for value in frames: 
  curr = (timer() - start)*1000
  shouldframe = int(curr / frametime)
  if counter < shouldframe: # can't keep up, drop frame
    print('D')
    counter += 1
    continue

  if counter > shouldframe: # wait until next frame due
    untilnext = (counter*frametime) - curr
    time.sleep(untilnext/1000)
  
  for y in range(HEIGHT >> 3):
    m = y*OWIDTH+5+XOFFSET
    m8 = y*8
    for x in range(VWIDTH):
      out = 0
      cnt = int(x+m)
      for z in range(8):
        ison = (value[z+m8][x][0] > THRES)
        out += (ison << z)
      arr[cnt] = out

  ser.write(arr)
  counter += 1

ser.close()