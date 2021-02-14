import moviepy.editor as mp
import serial
import time

WIDTH = 128
HEIGHT = 64
COMPORT = 'COM6'
THRES = 128

ser = serial.Serial()
ser.baudrate = 500000
ser.port = COMPORT
ser.open()

clip = mp.VideoFileClip('badapple.mp4')
clip_resized = clip.resize((WIDTH,HEIGHT))
# clip_resized.write_videofile("movie_resized.mp4")
# iterating frames 
frames = clip_resized.iter_frames() 
  
# # counter to count the frames 
counter = 0

arr = bytearray(int(WIDTH*HEIGHT/8 +5))
for i in range(int(WIDTH*HEIGHT/8 +5)):
  arr[i] = 2

arr[0] = 118
arr[1] = WIDTH
arr[2] = HEIGHT
arr[3] = 0
arr[4] = 0
#fr = frames[0]
#fr = clip_resized.get_frame(18)
# clip_resized.save_frame('my_image.jpeg', t=2) # save frame at t=2 as JPEG
  
# # using loop to tranverse the frames 
for value in frames: 
  for y in range(HEIGHT >> 3):
    for x in range(WIDTH):
      outb = 0
      cnt = int(5+x+y*WIDTH)
      for z in range(8):
        ison = (value[z+y*8][x][0] > THRES)
        outb = outb + (ison << z)
      arr[cnt] = outb

  ser.write(arr)
  # incrementing the counter 
  counter += 1

ser.close()
      
# printing the value of the counter 
print("Counter Value ", end = " : ") 
print(counter) 

  
# showing  clip  
# clip_resized.preview()
# clip_resized.show()
# clip_resized.ipython_display(width = 360) 