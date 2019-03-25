{{

Messages are pure text. Numbers in the text are two digit decimal.

Configure message:

{"to":"??","C":"wwhh..........Axxyymm0011,1122,3333:Bxxyymm1111"} 

  First the initial board. wwhh (width,height) followed by w*h characters.
  Then the piece-info list with entries separated by ":"
    The first character is the token.
    xx,yy are the current X,Y coordinates
    mm is the current draw string
    Next is the list of draw strings separated by ","    

Status request:

{"to":"??","R":True}

Response message to status request:

{"to":"00","T":"..seeBelow.."}

  "status" = 
    "!" if there is no solution to send (still working)
    "*" if the process is complete (also the initial state before config)                    
    "wwhh..........Axxyymm0011,1122,3333:Bxxyymm1111" return the current state if a solution is found

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

    DQUOTE = $22

OBJ
  bus : "hilobus"
  API : "hilobus_api"

pri getNumber(p) | a,b
  a := byte[p] - "0"
  b := byte[p+1] - "0"
  return a*10+b

pri setNumber(p,value)
  byte[p] := value / 10
  byte[p+1] := value // 10

pri getCell(p,x,y,width,height) 
  return byte[p+width*y+x]

pri setCell(p,x,y,width,height,value)
  byte[p+width*y+x] := value

pri main_loop | p, q, width, height, i, j 

  ' ##### Parse out the board (width, hight, state)

  ' TODO p is the config start

  width := getNumber(p)
  height := getNumber(p+2)

  ' TODO q is the 60-byte scratch buffer

  ' Copy the initial starting board
  repeat i from 0 to (width*height-1)
    byte[q+i] := byte[p+i]

  ' i is the starting point of the pieces

pri draw_board(p,q,width,height) | i, token, x, y, m, c
{{
   p = pointer to first piece
   q = pointer to board
   width, height = board dimensions
   returns:
     0 if drawn OK or
     token if there is an overlap
}}

  ' Try all pieces
  repeat while byte[p]<>DQUOTE
  
    ' Location of the piece and the draw string number
    token := byte[p]
    x := getNumber(p+1)
    y := getNumber(p+3)
    m := getNumber(p+5)
    p := p + 7    
    
    ' Find the draw string for this piece
    repeat while m<>0
      repeat while byte[i]<>","
        p := p + 1
      m := m - 1
      p := p + 1

    ' The first cell is the starting x,y
    c := getCell(q,x,y,width,height)
    if c<>"." and c<>token
      ' Not us ... don't even try the others
      return token
    
    ' Try all the chars in the draw string         
    repeat while byte[p]<>"," and byte[p]<>DQUOTE
      c := byte[p]
      p := p + 1
      if c=="1"                                           
        y := y - 1
      elseif c=="2"
        x := x + 1
      elseif c=="3"
        y := y + 1
      else
        x := x - 1
      c := getCell(q,x,y,width,height)
      if c<>"." and c<>token
        return token
      setCell(q,x,y,width,height,token)    

    ' Next piece
    repeat while byte[p]<>":" and byte[p]<>DQUOTE
      p := p + 1
    if byte[p]==":"
      ' Skip the colon or leave the DQUOTE
      p := p + 1

  ' 0 means all drawn OK ... no overlap
  return 0      

pri one_run(p,q, width, height) | i, token, x, y, m, overlap, c
{{
  p = pointer to first piece
  q = pointer to board
  width, height = dimensions of the board
}}   

  ' ##### Draw the board

  c := draw_board(p,q,width,height)  

  ' ##### Advance the pointer set

  ' TODO return 2 if success
  ' TODO return 3 if no more to try

  ' Keep calling me
  return 0 


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
   
  repeat
    p := API.get_message(params,queue)
    if p <> 0
      if byte[p+17] == "t"
        setTestLED(pin,1)
      else
        setTestLED(pin,0)
    API.release_message(params,p)  
  
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

  
  ' TODO Magic here

  ' Wait for the button press

  ' acquire the lock
  ' send the message
  ' release the lock

  ' Wait for the button release