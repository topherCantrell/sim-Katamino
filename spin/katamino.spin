{{

Messages are pure text. Numbers in the text are two digit decimal.

Configure message:

  "*" = "wwhh..........nnAxxyymm0011,1122,3333:Bxxyymm1111" 

  First the initial board. wwhh (width,height) followed by w*h characters.
  Then nn is the current piece.
  Then the piece-info list with entries separated by ":"
    The first character is the token.
    xx,yy are the current X,Y coordinates
    mm is the current draw string
    Next is the list of draw strings separated by ","    

Status request:

  "?" = True

Response message to status request:

  "status" = 
    "!" if there is no solution to send (still working)
    "*" if the process is complete (also the initial state before config)                    
    "wwhh..........nnAxxyymm0011,1122,3333:Bxxyymm1111" return the current state if a solution is found

Algorithm

  - Load the config
  - Parse out the board width,height
  - Make a copy of the board for resetting

  - REPEAT    
    - Draw current state
    - If success, hold for retrieval
    - Respond to any requests (including new config) 
    - Reset the board
    - Advance the pointer set (detect the end)

}}

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
  
  'cognew(handleButton(p,"C",TEST_BUTTON_RED), @stack3)
  'cognew(handleButton(p,"D",TEST_BUTTON_YELLOW), @stack4)

  bus.run

pri controlLED(params,queue,pin) | lock_id, p

   initTest
     
  ' {"to":"cq","on":true}
  ' {"to":"cq","on":false}
  
  lock_id := long[params+12]

  repeat while long[params]<>0    
        
  repeat
    repeat until not lockset(lock_id)
    long[params+4] := queue
    long[params] := bus#COM_GET_MESSAGE
    repeat while long[params]<>0
    p := long[params+8]
    if p <> 0
      if byte[p+17] == "t"
        setTestLED(pin,1)
      else
        setTestLED(pin,0)
      byte[p] := 0
    lockclr(lock_id)  
  
  ' TODO Magic here

  ' acquire the lock
  ' get the message
  ' release the lock
  
  ' set LED based on byte 15 ... T or F

  ' acquire the lock
  ' release the message
  ' release the lock  

pri handleButton(params,queue,pin) : lock_id

  initTest
  
  lock_id := long[params+12]
  
  ' TODO Magic here

  ' Wait for the button press

  ' acquire the lock
  ' send the message
  ' release the lock

  ' Wait for the button release