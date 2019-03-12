'
' SERIAL BUS
'
' There are two serial ports: "left" and "right".
' The host is assumed to be far left.
'
' {"to":"3A", ... }
'
' Messages are JSON format. The serial-bus module includes code to
' parse JSON.
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
'   get_message() : returns a pointer to the current JSON or 0 if there is no message
'   clear_message(): removes the current message from the queue
'   send_message(msg): puts the message on the bus