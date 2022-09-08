#include "Mouse.h"
#include <Keyboard.h>

bool home_flag;

void setup()
{
  // put your setup code here, to run once:
  Mouse.begin();
  Keyboard.begin();
  // stream.setTimeout(50);
  Serial.begin(9600);
  home_flag = false;
}

void loop()
{
  // put your main code here, to run repeatedly:
  // Mouse.move(10, 0, 0);
  // Serial.println("kokot");

  if (Serial.available() > 0)
  {
    String input = Serial.readStringUntil('`');
    if (input[0] == '|')
    {
      input.remove(0, 1);
      // if int
      click_key(input.toInt());
    }
    else if (input[0] == '%')
    {
      // if string
      input.remove(0, 1);
      Keyboard.println(input);
    }
    else if (input[0] == 'c')
    {
      Mouse.press();
      delay(70);
      Mouse.release();
    }
    else if (input[0] == 'l')
    {
      Mouse.press();
    }
    else if (input[0] == 'r')
    {
      Mouse.press(MOUSE_RIGHT);
    }
    else if (input[0] == 'x')
    {
      Mouse.release();
      Mouse.release(MOUSE_RIGHT);
    }
    else
    {
      String x = getValue(input, ':', 0);
      String y = getValue(input, ':', 1);
      // sscanf(input, "%d:%d", &x, &y);
      int a = x.toInt();
      int b = y.toInt();
      // Serial.println(x);
      // Serial.println(y);
      int ka = 1;
      int kb = 1;
      if (a < 0)
      {
        ka = -1;
      }
      if (b < 0)
      {
        kb = -1;
      }

      while (a > 100 || a < -100)
      {

        Mouse.move(100 * ka, 0, 0);
        a -= 100 * ka;
      }
      while (b > 100 || b < -100)
      {
        Mouse.move(0, 100 * kb, 0);
        b -= 100 * kb;
      }
      Mouse.move(a, b, 0);
    }
  }
}

void click_key(char key)
{
  Keyboard.press(key);
  delay(100);
  Keyboard.releaseAll();
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++)
  {
    if (data.charAt(i) == separator || i == maxIndex)
    {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
