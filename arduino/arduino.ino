#include <Arduboy2.h>


Arduboy2Base arduboy;

void setup() {
  //arduboy.boot();
  //arduboy.display();
  //arduboy.flashlight();
  arduboy.begin();
  //Serial.begin(460800);
  Serial.begin(500000);
}

uint16_t pos = 0;
byte cmd = 0;
byte w, h, x, y , len;
//byte vidbuf[1024];

void loop() {
  //if (!(arduboy.nextFrame())) return;
  //arduboy.clear();

  while(Serial.available()) {
    //byte val = Serial.read();
    //readBytes()
    if (pos > 4) {
      arduboy.clear();
      Serial.readBytes(arduboy.sBuffer ,1024);
      //arduboy.sBuffer[0] = Serial.read();
      //arduboy.drawBitmap(x, y, vidbuf, w, h);
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
