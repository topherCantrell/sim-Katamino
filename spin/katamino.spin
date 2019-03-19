CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000

OBJ
  bus : "hilobus"

PUB run
  bus.run

' start a couple of test COGs that watch for "A", "B", etc and light lights

' start a couple of test COGs that watch a switch and send messages
