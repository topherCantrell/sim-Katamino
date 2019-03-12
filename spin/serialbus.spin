CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000

' Left is always  StartRxTx(31, 30, 0, baudrate)
' Right is always StartRxTx(15, 14, 0, baudrate)
'
' SERIAL BUS
'
' There are two serial ports: "left" and "right".
' The host is assumed to be far left.
'
' {"to":"3A", ... }
'
' Messages are JSON format. The serial-bus module includes code to
' parse JSON. All messages must be objects "{...}"
'
' Messages are sent left or right depending on the "to" number. Smaller
' numbers go left, and larger go right. Nodes forward messages that are
' not meant for them. Addresses are always 2 characters: chip number and
' queue name (see below).
'
' The very first message sent to a node is {"you_are": "N"}, where "N" is the
' number/letter of the chip. This tells the chip what's its "to" address number
' is. The node then adds one and sends the message to the right. Thus the
' addressing ripples down the chain left to right. These messages are sent
' to all queues -- a signal for nodes to register to their queues.
'
' There are five separate message queues A, B, C, D, and E. Messages to the
' target node are routed to the given queue. Worker nodes register with the
' bus with the {"alive": "M"} message where "M" is the queue it would like
' to use or "*" for the bus to pick. The bus will send the queue the
' {"you_are": "NM"} message in response to the alive.
'
' A message queue can hold TWO messages only. Others are ignored.
'
' Messages {"to":"*" ...} are forwarded to all queues.
'
' API
'   get_message():ptr - returns a pointer to the current JSON or 0 if there is no message
'   clear_message()   - removes the current message from the queue
'   send_message(msg) - puts the message on the bus  

CON

    LEFT_RX     =   31
    LEFT_TX     =   30
    RIGHT_RX    =   15
    RIGHT_TX    =   14
    BAUDRATE    =   115200
    QUEUE_SIZE  =   512
    NUM_QUEUES  =   5

    COM_IDLE          = 0
    COM_GET_MESSAGE   = 1
    COM_CLEAR_MESSAGE = 2
    COM_SEND_MESSAGE  = 3

VAR
    long  param_command  ' Set to one of the COM_ constants above
    long  param_argument ' The send_message needs a pointer
    long  param_return   ' The get_message returns a pointer

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

PUB run
' Never returns

  param_command := COM_IDLE
  tmp_queue_left_idx := 0
  tmp_queue_right_idx := 0

  current_read_buffer := 0
  
  SER_LEFT.StartRxTx (LEFT_RX,  LEFT_TX,  0, BAUDRATE)
  SER_RIGHT.StartRxTx(RIGHT_RX, RIGHT_TX, 0, BAUDRATE)

  repeat
    check_incoming
    check_command

PRI process_message(is_left,msg)
  ' If for us, send to queue
  ' If for left, send left
  ' If for right, send right (might be both)

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
        process_message(true,tmp_queue_left)
        tmp_queue_left_idx := 0
        
  if SER_RIGHT.RxCount>0
    c := SER_RIGHT.CharIn
    if tmp_queue_right_idx == 0
      ' Start of a message? Must be JSON object. Wait till we see one.
      if c <> "{"
        return
      tmp_queue_right[tmp_queue_right_idx] := c
      tmp_queue_right_idx := tmp_queue_right_idx + 1
    else
      tmp_queue_right[tmp_queue_right_idx] := c
      tmp_queue_right_idx := tmp_queue_right_idx + 1      
      if c=="}"
        process_message(true,tmp_queue_left)
        tmp_queue_right_idx := 0
        tmp_queue_right[tmp_queue_right_idx] := 0  

PRI check_command

  
