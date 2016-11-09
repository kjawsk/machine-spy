function startup()
    if file.open("init.lua") == nil then
        print("init.lua deleted or renamed")
    else
        print("Running")
        file.close("init.lua")
        --the actual application is stored in 'application.lua'
        dofile("main.lua")
    end
end

print("Connecting to WiFi access point...")
wifi.setmode(wifi.STATION)

-- wifi.sta.connect() not necessary because config() uses auto-connect=true by default
tmr.alarm(1, 1000, 1, function()
    if wifi.sta.getip() == nil then
        print("Waiting for IP address...")
    else
        tmr.stop(1)
        print("WiFi connection established, IP address: " .. wifi.sta.getip())
        print("You have 3 seconds to abort")
        print("Waiting... ")
        collectgarbage()
        -- it is time to brake init
        tmr.alarm(0, 3000, 0, startup)
    end
end)
