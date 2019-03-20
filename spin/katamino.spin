CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000

CON ' DEBUG
    TEST_LED_GREEN     = 2
    TEST_LED_RED       = 3
    TEST_LED_YELLOW    = 4
    TEST_BUTTON_RED    = 5
    TEST_BUTTON_YELLOW = 6

OBJ
  bus : "hilobus"

pri initTest
  dira[TEST_LED_GREEN] := 1
  outa[TEST_LED_GREEN] := 0
  dira[TEST_LED_RED] := 1
  outa[TEST_LED_RED] := 0
  dira[TEST_LED_YELLOW] := 1
  outa[TEST_LED_YELLOW] := 0  
  dira[TEST_BUTTON_RED] := 0
  dira[TEST_BUTTON_YELLOW] := 0 

pri getTestButton(p)
  return !ina[p]

pri setTestLED(p,val)
  outa[p] := val

var
  long stack1[256]
  long stack2[256]
  long stack3[256]
  long stack4[256]   
    
PUB run | p

  bus.init
  
  p := bus.getParamAddr
  cognew(controlLED(p,"A",TEST_LED_GREEN), @stack1) 
  cognew(controlLED(p,"B",TEST_LED_RED), @stack2)
  
  cognew(handleButton(p,"C",TEST_BUTTON_RED), @stack3)
  cognew(handleButton(p,"D",TEST_BUTTON_YELLOW), @stack4)

  bus.run

pri controlLED(params,queue,pin) : lock_id

  ' {"to":"cq","on":True}
  ' {"to":"cq","on":False}
  
  lock_id := long[params+12]
  ' TODO Magic here

  ' acquire the lock
  ' get the message
  ' release the lock
  
  ' set LED based on byte 15 ... T or F

  ' acquire the lock
  ' release the message
  ' release the lock  

pri handleButton(params,queue,pin) : lock_id
  lock_id := long[params+12]
  
  ' TODO Magic here

  ' Wait for the button press

  ' acquire the lock
  ' send the message
  ' release the lock

  ' Wait for the button release