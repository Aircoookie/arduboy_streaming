/*
  MIT License
  
  Copyright (c) 2021 Christian Schwinne
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
 */

#include <Arduboy2.h>

Arduboy2Base arduboy;

void setup() {
  arduboy.begin();
  Serial.begin(500000);
}

uint16_t pos = 0;
byte cmd = 0;
byte w, h, x, y , len;

void loop() {
  //if (!(arduboy.nextFrame())) return;
  //arduboy.clear();

  while(Serial.available()) {
    if (pos > 4) {
      arduboy.clear();
      Serial.readBytes(arduboy.sBuffer, 1024);
      arduboy.display();
      pos = 0;
    } else {
      byte val = Serial.read();
      switch (pos) {
        case 0: {
          if (val == 'v') cmd = 1; //video
          else return; //unknown command
          break; //video
        }
        case 1: if (cmd == 1) w = val; break;
        case 2: if (cmd == 1) h = val; break;
        case 3: if (cmd == 1) x = val; break;
        case 4: if (cmd == 1) {y = val; len = (w*h) >> 3;} break;
      }
      pos++;
    }
  }
}
