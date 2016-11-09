-- Configuration to connect to the MQTT broker.
BROKER = "192.168.0.103"   -- Ip/hostname of MQTT broker
BRPORT = 1884             -- MQTT broker port
BRUSER = ""           -- If MQTT authenitcation is used then define the user
BRPWD  = ""            -- The above user password
CLIENTID = "ESP8266-" ..  node.chipid() -- The MQTT ID. Change to something you like
TIMER_TIMEOUT = 5000
MQTT_KEEPALIVE = 120

-- Control variables.
id1 = 0

function publish_data()
    m:publish("/test", CLIENTID .. " publish_data: " .. id1,0,0, function(conn)
        print("Sending data: " .. id1)
        id1 = id1 + 1
    end)
end

function receive_data(client, topic, data)
    if data ~= nil then
        print(topic .. " : " ..  data)
    end
end

--main program to run after the subscriptions are done
function run_main_prog()
    print("Connected to MQTT:" .. BROKER .. ":" .. BRPORT .." as " .. CLIENTID )

    -- publish data with TIMER_TIMEOUT interval
    tmr.alarm(1, TIMER_TIMEOUT, tmr.ALARM_AUTO, publish_data)

    m:subscribe("/ping",0, function(client) print("subscribe success") end)
    m:on("message", receive_data)
end

function handle_connection_error (client, reason)
    print("failed reason: "..reason)
end

-- connect to the broker
print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( CLIENTID, MQTT_KEEPALIVE, BRUSER, BRPWD)
m:connect( BROKER , BRPORT, 0, run_main_prog, handle_connection_error)
