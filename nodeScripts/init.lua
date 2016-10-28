-- file : init.lua
wifi.setmode(wifi.STATION);
wifi.sta.config("Siec_Szefa","24ogoralki")
wifi.sta.connect()

dofile("main.lua")
