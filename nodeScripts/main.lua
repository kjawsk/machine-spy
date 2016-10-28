-- Configuration to connect to the MQTT broker.
BROKER = "192.168.0.103"   -- Ip/hostname of MQTT broker
BRPORT = 1884             -- MQTT broker port
BRUSER = ""           -- If MQTT authenitcation is used then define the user
BRPWD  = ""            -- The above user password
CLIENTID = "ESP8266-" ..  node.chipid() -- The MQTT ID. Change to something you like

-- connect to the broker
print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( CLIENTID, 120, BRUSER, BRPWD)
m:connect( BROKER , BRPORT, 0, function(conn)
    print("Connected to MQTT:" .. BROKER .. ":" .. BRPORT .." as " .. CLIENTID )
    run_main_prog()
end)

-- Control variables.
id1 = 0

print "Publish..."
function publish_data1()
    m:publish("/test","publish_data1 "..CLIENTID,0,0, function(conn)
        print("Sending data1: " .. id1)
        id1 = id1 + 1
    end)
end

--main program to run after the subscriptions are done
print "run main..."
function run_main_prog()
     print("Main program")
     tmr.alarm(2, 5000, 1, publish_data1 )
end