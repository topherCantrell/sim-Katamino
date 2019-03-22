{{
 Left is always  StartRxTx(31, 30, 0, baudrate)
 Right is always StartRxTx( 1,  0, 0, baudrate)

 HI/LO SERIAL BUS

 There are two serial ports: "left" (lower) and "right" (higher).
 The host should be the far left. 

 Typical message:
 {"to":"3A", ... }

 Messages are JSON format. The serial-bus module includes code to
 parse JSON. All messages must be objects "{...}"

 Messages are sent left or right depending on the "to" number. Smaller
 numbers go left. Larger go right. Nodes forward messages that are
 not meant for them. Addresses are always 2 characters: chip number and
 queue name (see below).

 The very first message sent to a node is {"to": "@N"}, where "N" is the
 number/letter of the chip. This always comes in on the LOWER port. This tells
 the chip what's its "to" address number is. The node then adds one and sends
 the message to the UPPER. Thus the addressing ripples down the chain left to
 right.

 There are (up to) five separate message queues A, B, C, D, and E: one for the
 available 5 COGs. Three COGs are used in the bus. Messages to the target nodes
 are routed to the specific queue. Nodes are hardcoded to a fixed queue.

 A message queue can hold ONE message only. Others are ignored.

 Messages {"to":"**" ...} are forwarded to all queues on all chips.
 Messages {"to":"2*" ...} are forwarded to all queues on chip 2.

 API
   get_message(q):ptr - returns a pointer to the current JSON or 0 if there is no message
   clear_message(ptr) - releases the message pointer
   send_message(msg)  - puts the message on the bus

   - acquire the lock with "repeat until not lockset(param_lock_id)"
   - write any parameter
   - write the command
   - wait for the command to go to 0
   - read any return value
   - release the lock with "lockclr(param_lock_id)

 SYNCHRONIZATION:
 
 All nodes share the common parameter block.

 Nodes must acquire the lock using "lockset(param_lock_id)" before writing to the
 command parameters. Nodes must release the lock using "lockclr(param_lock_id")
 after they have written the command trigger.
 
}}

CON
    LEFT_TX     =   30
    LEFT_RX     =   31
    
    RIGHT_TX    =   0 
    RIGHT_RX    =   1
    
    BAUDRATE    =   115200
    QUEUE_SIZE  =   512      ' Max size of a message
    NUM_QUEUES  =   5        ' Number of node-queues

    COM_IDLE          = 0
    COM_GET_MESSAGE   = 1
    COM_SEND_MESSAGE  = 2

VAR
    ' ---------------------------------------------------------------
    long  param_command  ' Set to one of the COM_ constants above
    long  param_argument ' Argument to the request (be sure to set this BEFORE the command)
    long  param_return   ' The get_message returns a pointer (READONLY)
    '
    long  param_lock_id  ' The LOCKNEW id used to sync sharing messages (READONLY)
    long  chip_number    ' Our char (or 0 if not set) (READONLY)
    ' ---------------------------------------------------------------

    ' Each node gets 1 queue
    byte msg_buffers[QUEUE_SIZE * NUM_QUEUES]     

    ' Left/Right messages as they come in
    byte tmp_queue_left[QUEUE_SIZE]
    byte tmp_queue_right[QUEUE_SIZE]    
    byte tmp_queue_left_idx
    byte tmp_queue_right_idx  
     
OBJ
    SER_LEFT  : "Parallax Serial Terminal"
    SER_RIGHT : "Parallax Serial Terminal" 

CON ' DEBUG
    TEST_LED_GREEN     = 2
    TEST_LED_RED       = 3
    TEST_LED_YELLOW    = 4
    TEST_BUTTON_RED    = 5
    TEST_BUTTON_YELLOW = 6
    
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
  
PUB init | i
  ' This is for all the nodes to synchronize using the single
  ' command parameter block.
  '
  ' We don't need this lock in the bus code. As far as we are
  ' concerned, the universe is US and NODE. It is up to the
  ' nodes to decide which one of them is NODE.
  param_lock_id := locknew

  ' Clear the incoming command
  param_command := COM_IDLE

  ' Clear the serial queues
  tmp_queue_left_idx := 0
  tmp_queue_right_idx := 0    

  chip_number := 0 ' Will be an ascii number when set

  ' Clear out the queues
  repeat i from 0 to (QUEUE_SIZE * NUM_QUEUES-1)
    msg_buffers[i] := 0 

  ' Start the serial ports
  SER_LEFT.StartRxTx ( LEFT_RX,  LEFT_TX, 0, BAUDRATE)
  SER_RIGHT.StartRxTx(RIGHT_RX, RIGHT_TX, 0, BAUDRATE)

  initTest

PUB getParamAddr
  return @param_command
  
PUB run

  ' Never returns (takes the cog) 

  repeat
    check_incoming
    check_command

PRI process_message(source_port, msg) | chip,queue,i,nq,p,q

  ' {"to":"cq", ...}
  ' c = chip (or * or @)
  ' q = queue (or *)

  chip := byte[msg+7]
  queue := byte[msg+8]

  ' Special message: set our chip-number
  if chip=="@"
    ' This is a "set-chip-number" message
    chip_number := queue        

    ' Tell the next chip in line (to the right)
    byte[msg+8] := queue + 1
    SER_RIGHT.str(msg)
    return
  
  ' We might need to send this message to our queues          
  if chip == chip_number or chip == "*"
  ' ' This is meant for us ... send it to the queue(s).
    ' We have no way of knowing which node sourced the message, so if
    ' you are local and you are broadcasting to this chip then you'll
    ' get a copy too.
        
    nq := queue - "A" ' ASCII name (A,B,C,D,...) to index (0,1,2,3,...)
        
    repeat i from 0 to (NUM_QUEUES-1)
      ' If this msg was directed to the queue directly or broadcast
      if queue=="*" or i==nq
        ' If the message buffer is not free, we drop this message.
        if msg_buffers[i*QUEUE_SIZE] == 0
          ' Copy msg to the queue                    
          
          p := msg
          q := @msg_buffers+i*QUEUE_SIZE
          repeat while byte[p]<>0
            byte[q] := byte[p]
            q := q + 1
            p := p + 1
          ' Terminate the message
          byte[q] := 0
          
  ' Special message: needs to be broadcast
  if chip == "*"
    ' Broadcast left and/or right 
    if source_port==2
      ' Broadcast from us (to left and right)
      SER_LEFT.str(msg)
      SER_RIGHT.str(msg)
      return      
    elseif source_port==0
      ' Broadcast from left (to right)
      SER_RIGHT.str(msg)
    else
      ' Broadcast from right (to left)
      SER_LEFT.str(msg)
    return

  ' Route this message left or right
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
        tmp_queue_right[tmp_queue_right_idx] := 0
        process_message(1,@tmp_queue_right)
        tmp_queue_right_idx := 0

PRI check_command | p
      
  ' COM_GET_MESSAGE   = 1
  ' COM_CLEAR_MESSAGE = 2
  ' COM_SEND_MESSAGE  = 3

  if param_command == COM_IDLE
    return                   

  if param_command == COM_GET_MESSAGE    
    p := @msg_buffers + (param_argument-"A")*QUEUE_SIZE
    if byte[p] == 0      
      param_return := 0
    else      
      param_return := p    
    
  elseif param_command == COM_SEND_MESSAGE
    process_message(3, param_argument)
    param_return := 0

  ' Whatever it was, we are done with it
  param_command := COM_IDLE
 