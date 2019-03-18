CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000

' Left is always  StartRxTx(31, 30, 0, baudrate)
' Right is always StartRxTx( 1,  0, 0, baudrate)
'
' HI/LO SERIAL BUS
'
' There are two serial ports: "left" (lower) and "right" (higher).
' The host should be the far left. 
'
' Typical message:
' {"to":"3A", ... }
'
' Messages are JSON format. The serial-bus module includes code to
' parse JSON. All messages must be objects "{...}"
'
' Messages are sent left or right depending on the "to" number. Smaller
' numbers go left. Larger go right. Nodes forward messages that are
' not meant for them. Addresses are always 2 characters: chip number and
' queue name (see below).
'
' The very first message sent to a node is {"to": "@N"}, where "N" is the
' number/letter of the chip. This always comes in on the LOWER port. This tells
' the chip what's its "to" address number is. The node then adds one and sends
' the message to the UPPER. Thus the addressing ripples down the chain left to
' right. These messages are also sent to all queues -- a signal for nodes that
' the bus is ready.
'
' There are five separate message queues A, B, C, D, and E. Messages to the
' target nodes are routed to the specific queue. Nodes are hardcoded to a
' fixed queue.
'
' A message queue can hold TWO messages only. Others are ignored.
'
' Messages {"to":"**" ...} are forwarded to all queues on all chips.
' Messages {"to":"2*" ...} are forwarded to all queues on chip 2.
'
' API
'   get_message():ptr - returns a pointer to the current JSON or 0 if there is no message
'   clear_message()   - removes the current message from the queue
'   send_message(msg) - puts the message on the bus  

CON

    LEFT_TX     =   30
    LEFT_RX     =   31
    
    RIGHT_TX    =   0 
    RIGHT_RX    =   1
    
    BAUDRATE    =   115200
    QUEUE_SIZE  =   512
    NUM_QUEUES  =   5

    COM_IDLE          = 0
    COM_GET_MESSAGE   = 1
    COM_CLEAR_MESSAGE = 2
    COM_SEND_MESSAGE  = 3

CON

    TEST_LED_GREEN     = 2
    TEST_LED_RED       = 3
    TEST_LED_YELLOW    = 4
    TEST_BUTTON_RED    = 5
    TEST_BUTTON_YELLOW = 6

VAR
    long  param_command  ' Set to one of the COM_ constants above
    long  param_argument ' The send_message needs a pointer
    long  param_return   ' The get_message returns a pointer

    byte chip_number

    byte msg_buffers[QUEUE_SIZE * NUM_QUEUES * 2] 
    byte current_read_buffer[NUM_QUEUES]
    
    byte tmp_queue_left[QUEUE_SIZE]
    byte tmp_queue_right[QUEUE_SIZE]    
    byte tmp_queue_left_idx
    byte tmp_queue_right_idx
    
    byte queues[NUM_QUEUES * QUEUE_SIZE]
     
OBJ
    SER_LEFT  : "Parallax Serial Terminal"
    SER_RIGHT : "Parallax Serial Terminal"

pri initTest
  dira[TEST_LED_GREEN] := 1
  outa[TEST_LED_GREEN] := 0
  dira[TEST_LED_RED] := 1
  outa[TEST_LED_RED] := 0
  dira[TEST_LED_YELLOW] := 1
  outa[TEST_LED_YELLOW] := 0  
  dira[TEST_BUTTON_RED] := 0
  dira[TEST_BUTTON_YELLOW] := 0 

pri getTest(p)
  return !ina[p]

pri setTest(p,val)
  outa[p] := val

pri doTest
  initTest
  repeat
    outa[TEST_LED_RED] := !ina[TEST_BUTTON_RED]
    outa[TEST_LED_YELLOW] := !ina[TEST_BUTTON_YELLOW]  

PUB run
' Never returns

  initTest

  param_command := COM_IDLE
  tmp_queue_left_idx := 0
  tmp_queue_right_idx := 0

  current_read_buffer := 0

  chip_number := 0 ' Will be an ascii number when set
  
  SER_LEFT.StartRxTx ( LEFT_RX,  LEFT_TX, 0, BAUDRATE)
  SER_RIGHT.StartRxTx(RIGHT_RX, RIGHT_TX, 0, BAUDRATE)

  repeat
    check_incoming
    'check_command

PRI process_message(source_port, msg) | chip,queue

  chip := byte[msg+7]
  queue := byte[msg+8]

  if chip=="@"
    ' This is a "set-chip-number" message
    chip_number := queue
    byte[@SET_CHIP_NUM_MESSAGE+8] := queue + 1

    ' Tell the next chip in line (to the right)
    SER_RIGHT.str(@SET_CHIP_NUM_MESSAGE)
    return

  if chip == "*"
    ' Broadcast 
    if source_port==2
      ' Broadcast from us (to left and right)
      SER_LEFT.str(msg)
      SER_RIGHT.str(msg)
    elseif source_port==0
      ' Broadcast from left (to right)
      SER_RIGHT.str(msg)
    else
      ' Broadcast from right (to left)
      SER_LEFT.str(msg)     
    return
            
  if chip == chip_number
    ' This is meant for us ... send it to the queue(s)
    if chip=="A" or chip=="*"
      setTest(2,1)
    if chip=="B" or chip=="*"
      setTest(3,1)
    if chip=="C" or chip=="*"
      setTest(4,1)
    ' TODO send to queues
    return  

  if chip < chip_number
    ' Going LEFT
    SER_LEFT.str(msg)
  else
    ' Going RIGHT 
    SER_RIGHT.str(msg) 

PRI check_incoming | c

  if SER_LEFT.RxCount>0
    c := SER_LEFT.CharIn
    if tmp_queue_left_idx == 0
      ' Start of a message? Must be JSON object. Wait till we see one.
      if c <> "{"
        return
      tmp_queue_left[tmp_queue_left_idx] := c
      tmp_queue_left_idx := tmp_queue_left_idx + 1
    else
      tmp_queue_left[tmp_queue_left_idx] := c
      tmp_queue_left_idx := tmp_queue_left_idx + 1      
      if c=="}"
        tmp_queue_left[tmp_queue_left_idx] := 0
        process_message(0,@tmp_queue_left)
        tmp_queue_left_idx := 0
        
  'if SER_RIGHT.RxCount>0
  '  c := SER_RIGHT.CharIn
  '  if tmp_queue_right_idx == 0
  '    ' Start of a message? Must be JSON object. Wait till we see one.
  '    if c <> "{"
  '      return
  '    tmp_queue_right[tmp_queue_right_idx] := c
  '    tmp_queue_right_idx := tmp_queue_right_idx + 1
  '  else
  '    tmp_queue_right[tmp_queue_right_idx] := c
  '    tmp_queue_right_idx := tmp_queue_right_idx + 1      
  '    if c=="}"
  '      process_message(1,tmp_queue_left)
  '      tmp_queue_right_idx := 0
  '      tmp_queue_right[tmp_queue_right_idx] := 0  

PRI check_command

DAT

SET_CHIP_NUM_MESSAGE
  '     {"to":"@?"}
  byte "{",$22,"to",$22,":",$22,"@",0,$22,"}",0