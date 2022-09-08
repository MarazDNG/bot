#include "Mouse.h"
#include <Keyboard.h>

void setup()
{
    Mouse.begin();
    Keyboard.begin();
    // stream.setTimeout(50);
    Serial.begin(9600);
}

void loop()
{
    click_key(210);
    delay(80);
    click_key(210);
    delay(1000);
}

void click_key(int key)
{
    Keyboard.press(key);
    delay(100);
    Keyboard.releaseAll();
}
