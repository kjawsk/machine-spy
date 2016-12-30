BROKER = "192.168.0.103"
BRPORT = 1884
BRUSER = ""
BRPWD  = ""
CLIENTID = "ESP8266-" ..  node.chipid()
INPUT_PIN = 1
TEST_PIN = 2
TIMER_TIMEOUT = 5000
MQTT_KEEPALIVE = 120
id1 = 0

function publish_data()
    m:publish("/test", CLIENTID,0,0, function(conn)
        print("Sending data: " .. id1)
        id1 = id1 + 1
    end)
end

function receive_data(client, topic, data)
    if data ~= nil then
        print(topic .. " : " ..  data)
    end
end

function toggle_input()
    if gpio.read(INPUT_PIN) == 1 then
        gpio.write(TEST_PIN, gpio.LOW)
    else
        gpio.write(TEST_PIN, gpio.HIGH)
    end
end

function run_main_prog()
    print("Connected to MQTT:" .. BROKER .. ":" .. BRPORT .." as " .. CLIENTID )

    gpio.mode(INPUT_PIN, gpio.INT)
    gpio.trig(INPUT_PIN, "up", publish_data)

    -- it is only for testing purposes - toggle input every TIMER_TIMEOUT
    gpio.mode(TEST_PIN, gpio.OUTPUT)
    tmr.alarm(1, TIMER_TIMEOUT, tmr.ALARM_AUTO, toggle_input)

    m:subscribe("/ping",0, function(client) print("Subscribe success") end)
    m:on("message", receive_data)
end

function handle_connection_error (client, reason)
    print("Failed reason: "..reason)
end

print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( CLIENTID, MQTT_KEEPALIVE, BRUSER, BRPWD)
m:connect( BROKER , BRPORT, 0, run_main_prog, handle_connection_error)
