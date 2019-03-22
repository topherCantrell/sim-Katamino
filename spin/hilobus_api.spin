{{

   API for nodes to talk on the hilobus.

}}

CON
 
    COM_IDLE          = 0
    COM_GET_MESSAGE   = 1
    COM_SEND_MESSAGE  = 2

pub send_message(params, mes) | lock_id
  lock_id := long[params+12]
  repeat until not lockset(lock_id)
  long[params+4] := mes
  long[params] := COM_SEND_MESSAGE
  repeat while long[params]<>0
  lockclr(lock_id)

pub get_message(params,queue) | lock_id, p
  lock_id := long[params+12]
  repeat until not lockset(lock_id)
  long[params+4] := queue
  long[params] := COM_GET_MESSAGE
  repeat while long[params]<>0
  p := long[params+8]    
  lockclr(lock_id)
  return p

pub release_message(params, mes)
  ' For now, this is all we have to do. It might be more complicated
  ' in the future.
  byte[mes] := 0
