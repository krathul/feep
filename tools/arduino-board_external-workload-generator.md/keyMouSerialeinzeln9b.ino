// Add this before you include the HID-Project.
#include <HID-Settings.h>
#include <HID-Project.h>


/*
* keyMouSerial
* Decode received serial bytes to a USB HID keyboard and mouse
* Copyleft Peter Burkimsher 2015-06-26
* peterburk@gmail.com
*
* Requires Arduino with 32U4. Tested on Leonardo and Micro. 
*/

/*
#include <Mouse.h>
#include <MouseTo.h> // https://github.com/per1234/MouseTo
#include <Keyboard.h>
*/

// The previous mouse coordinates
unsigned int xValue;
unsigned int yValue;

// for debugging
String outputstring;

// definitions
boolean moreThanOneExpected = false;
String nextCommand = "none";


// http://www.elektronik-labor.de/Arduino/Leonardo3.html
// ummappen für deutsches KeyBoard-Layout

byte usToDE[256] =
{
//  0,  0,  0,  0,  0,  0,  0,  0, BS, TB, CR,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  8,  9, 10,  0,  0, 13,  0,  0,

    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,

// BL,  !,  @,  \,  $,  %,  ^,  |,  *,  (,  },  ],  ,,  /,  .,  &,
//          "               &   /   (   )   *   +       -       /
   32, 33, 64, 92, 36, 37, 94,124, 42, 40,125, 93, 44, 47, 46, 38,

//  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  >,  <,   ,  ),   ,  _,
//                                          :   ;      =        ?
   48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 60,  0, 41,  0, 95,

//   ,  A,  B,  C,  D,  E,  F,  G,  H,  I,  J,  K,  L,  M,  N,  O,
//   
    0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,

//  P,  Q,  R,  S,  T,  U,  V,  W,  X,  Z,  Y,   ,   ,   ,  `,  ?,
//                                      Y   Z   [   \   ]   ^   _
   80, 81, 82, 83, 84, 85, 86, 87, 88, 90, 89,  0,  0,  0, 96, 63,

//  +,  a,  b,  c,  d,  e,  f,  g,  h,  i,  j,  k,  l,  m,  n,  o,
//  `
   43, 97, 98, 99,100,101,102,103,104,105,106,107,108,109,110,111,

//  p,  q,  r,  s,  t,  u,  v,  w,  x,  z,  y,   ,   ,   ,   ,  DEL,
//                                      y   z    {   |   }   ~
  112,113,114,115,116,117,118,119,120,122,121,  0,  0,  0,  0,  178,

// 128,  129,  130,  131,  132,  133,  134,  135,  136,  137,  138,  139,  140,  141,  142,  143
// ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  
   128,  129,  130,  131,  132,  133,  134,  135,  136,  137,  138,  139,  140,  141,  142,  143,
// 144,  145,  146,  147,  148,  149,  150,  151,  152,  153,  154,  155,  156,  157,  158,  159
// ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  
   144,  145,  146,  147,  148,  149,  150,  151,  152,  153,  154,  155,  156,  157,  158,  159,
// 160,  161,  162,  163,  164,  165,  166,  167,  168,  169,  170,  171,  172,  173,  174,  175
//  ,  ¡,  ¢,  £,  €,  ¥,  Š,  §,  š,  ©,  ª,  «,  ¬,  ­,  ®,  ¯
   160,  161,  162,  163,  164,  165,  166,   35,  168,  169,  170,  171,  172,  173,  174,  175,
// 176,  177,  178,  179,  180,  181,  182,  183,  184,  185,  186,  187,  188,  189,  190,  191
// °,  ±,  ²,  ³,  Ž,  µ,  ¶,  ·,  ž,  ¹,  º,  »,  Œ,  œ,  Ÿ,  ¿
  126,  177,  178,  179,   61,  181,  182,  183,  184,  185,  186,  187,  188,  189,  190,  191,
// 192,  193,  194,  195,  196,  197,  198,  199,  200,  201,  202,  203,  204,  205,  206,  207
// À,  Á,  Â,  Ã,  Ä,  Å,  Æ,  Ç,  È,  É,  Ê,  Ë,  Ì,  Í,  Î,  Ï
  192,  193,  194,  195,   34,  197,  198,  199,  200,  201,  202,  203,  204,  205,  206,  207,
// 208,  209,  210,  211,  212,  213,  214,  215,  216,  217,  218,  219,  220,  221,  222,  223
// Ð,  Ñ,  Ò,  Ó,  Ô,  Õ,  Ö,  ×,  Ø,  Ù,  Ú,  Û,  Ü,  Ý,  Þ,  ß
  208,  209,  210,  211,  212,  213,   58,  215,  216,  217,  218,  219,  123,  221,  222,   45,
// 224,  225,  226,  227,  228,  229,  230,  231,  232,  233,  234,  235,  236,  237,  238,  239
// à,  á,  â,  ã,  ä,  å,  æ,  ç,  è,  é,  ê,  ë,  ì,  í,  î,  ï
  224,  225,  226,  227,  228,  229,  230,  231,  232,  233,  234,  235,  236,  237,  238,  239,
// 240,  241,  242,  243,   39,  245,  246,  247,  248,  249,  250,  251,  252,  253,  254,  255
// ð,  ñ,  ò,  ó,  ô,  õ,  ö,  ÷,  ø,  ù,  ú,  û,  ü,  ý,  þ,  ÿ
  240,  241,  242,  243,  244,  245,   59,  247,  248,  249,  250,   91,  252,  253,  254,  255

/*
// 
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0, 35,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,

/*

//  0,  0,  0,  0,  0,  0,  0,  0, BS, TB, CR,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  8,  9, 10,  0,  0, 13,  0,  0,

    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,

// BL,  !,  Ä,  §,  $,  %,  /,  ä,  ),  =,  (,  `,  ,,  ß,  .,  -,
//          "               &   /   (   )   *   +       -       /
   32, 33,196,167, 36, 37, 47,228, 41, 61, 40, 96, 44,223, 46, 45,

//  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  Ö,  ö,  ;,  ´,  :,  _,
//                                          :   ;      =        ?
   48, 49, 50, 51, 52, 53, 54, 55, 56, 57,214,246, 59,180, 58, 95,

//  ",  A,  B,  C,  D,  E,  F,  G,  H,  I,  J,  K,  L,  M,  N,  O,
//  0
   34, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,

//  P,  Q,  R,  S,  T,  U,  V,  W,  X,  Z,  Y,  ü,  #,  +,  &,  ?,
//                                      Y   Z   [   \   ]   ^   _
   80, 81, 82, 83, 84, 85, 86, 87, 88, 90, 89,252, 35, 43, 38, 63,

//  ^,  a,  b,  c,  d,  e,  f,  g,  h,  i,  j,  k,  l,  m,  n,  o,
//  `
   94, 97, 98, 99,100,101,102,103,104,105,106,107,108,109,110,111,

//  p,  q,  r,  s,  t,  u,  v,  w,  x,  z,  y,  Ü,   ,  *,  °, DEL,
//                                      y   z    {   |   }   ~
  112,113,114,115,116,117,118,119,120,122,121,220, 39, 42,176, 178

*/

};

// map US-keyboard to german keyboard
byte translateKey(byte k) {
  if (k >= 128) return k; // gebe alle Zeichen >= 128 unverändert zurück
   // return usToDE[ k];
   return k;
}

// setup - Start listening to serial at 9600 baud. 
void setup() 
{
  // open the serial port:
  Serial1.begin(9600);
  
  // Sends a clean report to the host. This is important on any Arduino type.
  Keyboard.begin();

  // Sends a clean report to the host. This is important on any Arduino type.
  AbsoluteMouse.begin();

  // Move to coordinate (16bit signed, -32768 - 32767)
  // Moving to the same position twice will not work!
  // X and Y start in the upper left corner.
  AbsoluteMouse.moveTo(0, 0);


  /*
  // initialize control over the mouse:
  Mouse.begin();
  MouseTo.setCorrectionFactor(1);
  MouseTo.home();
  Keyboard.begin();
  */
} // end setup

// loop - Continuously decode bytes until power is disconnected
void loop()
{
  // While the serial line has bytes coming in
  while (Serial1.available()) 
  {
    // Get the new byte
    byte inChar = (byte)Serial1.read();

    if (nextCommand == "nextValueX") {
        // Calculate the horizontal mouse movement
        if (moreThanOneExpected) {
          // collect lower part one of x-value
          xValue = (byte)inChar;
          moreThanOneExpected = false;
        }
        else {
          // collect higher part of x-value and assemble to 16-bit integer
          xValue = word((byte)inChar,xValue);
          nextCommand = "none";
        }
    }
    else if (nextCommand == "nextValueY") {
        // Calculate the vertical mouse movement
        if (moreThanOneExpected) {
          // collect lower part one of y-value
          yValue = (byte)inChar;
          moreThanOneExpected = false;
        }
        else {
          // collect higher part of y-value and assemble to 16-bit integer
          yValue = word((byte)inChar,yValue);
          nextCommand = "none";
        }
    }
    else if (nextCommand == "nextValuePressed") {
        // Press the left mouse button when we receive an 'l'
        if (inChar == 'l') 
        {
          AbsoluteMouse.press();
        }
        // Press the right mouse button when we receive an 'r'
        else if (inChar == 'r') 
        {
          AbsoluteMouse.press(MOUSE_RIGHT);
        }
        nextCommand = "none";
    }
    else if (nextCommand == "nextValueReleased") {
        // Release the left mouse button when we receive an 'l'
        if (inChar == 'l') 
        {
          AbsoluteMouse.release();
        }
        // Release the right mouse button when we receive an 'r'
        else if (inChar == 'r') 
        {
          AbsoluteMouse.release(MOUSE_RIGHT);
        }
        nextCommand = "none";
    }
    else if (nextCommand == "nextValueKey") {
        // Write the recieved character to the USB keyboard
        // Do not use Keyboard.write() because this releases all keys (also Modifier keys)
        // Keyboard.write(translateKey(inChar));
        Keyboard.press(translateKey(inChar));
        Keyboard.release(translateKey(inChar));
        
        // For a single keypress use press() and release()
        // If you really wish to press a RAW keycode without the name use this:
        // Keyboard.write(inChar);
        // Keyboard.write(KeyboardKeycode(inChar));
        
        /*
        outputstring = "druck: "+String(inChar)+" ";
        for (int i = 0; i < outputstring.length(); i++) {
           Keyboard.write(outputstring.charAt(i));
        }
        */
        nextCommand = "none";
    }
    else if (nextCommand == "nextValueKeyDown") {
        // Write the recieved character to the USB keyboard
        // Keyboard.press(translateKey(inChar));
        Keyboard.press(KeyboardKeycode(inChar));
        nextCommand = "none";
    }
    else if (nextCommand == "nextValueKeyUp") {
        // Write the recieved character to the USB keyboard
        // Keyboard.release(translateKey(inChar));
        Keyboard.release(KeyboardKeycode(inChar));
        nextCommand = "none";
    }
    else {
      // check which command was received
      switch (inChar) {
        case 'x':
          // If we receive an 'x', expect an x coordinate next time
          nextCommand = "nextValueX";
          moreThanOneExpected = true;
          break;
        case 'y':
          // If we receive an 'y', expect an y coordinate next time
          nextCommand = "nextValueY";
          moreThanOneExpected = true;
          break;
        case 'b':
          // If we receive an 'b', expect a mouse button press next time
          nextCommand = "nextValuePressed";
          break;
        case 'B':
          // If we receive an 'B', expect a mouse button released next time
          nextCommand = "nextValueReleased";
          break;
        case 'k':
          // If we receive an 'k', expect a printable key next time
          nextCommand = "nextValueKey";
          break;
        case 'd':
          // If we receive an 'd', expect a non-printable key pressed Down next time
          nextCommand = "nextValueKeyDown";
          break;
        case 'u':
          // If we receive an 'u', expect a a non-printable key released Up next time
          nextCommand = "nextValueKeyUp";
          break;
        case 'm':
          // If we receive an 'm', move the mouse
          // Move the mouse
          // Keyboard.println("x="+String(xValue)+" y="+String(yValue));
          AbsoluteMouse.moveTo(xValue, yValue);
          // while (MouseTo.move() == false) {}
          /*
          outputstring = "x="+String(xValue)+" y="+String(yValue)+char(176);
            for (int i = 0; i < outputstring.length(); i++) {
               Keyboard.write(outputstring.charAt(i));
               Keyboard.releaseAll();
            }
           */
          nextCommand = "none";
          break;
        default:
          // no valid command was given
          nextCommand = "nextValueKeyUp";
            
        } // end switch inChar
        
    } // end nextCommand
    
  } // end while serial is available
  
} // end loop

