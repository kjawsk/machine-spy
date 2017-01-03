BROKER = "192.168.0.103"
BRPORT = 1884
BRUSER = ""
BRPWD  = ""
CLIENTID = "ESP8266-" ..  node.chipid()
INPUT_PIN = 1
TEST_PIN = 2
TIMER_TIMEOUT = 5000
MQTT_KEEPALIVE = 120
GPIO_TIMER = 0
RECONNECT_TIMER = 1
IS_BROKER_CONNECTED = 0
id1 = 0

-------------------- MQTT HANDLING -----------------------------

function publish_data()
    id1 = id1 + 1
    if IS_BROKER_CONNECTED == 1 then
        m:publish("/test", CLIENTID,0,0, function(conn)
            print("Sending data: " .. id1)
        end)
    end
end

function handle_broker_offline(client)
    print ("Connection to the broker is lost. Reconnecting...")
    IS_BROKER_CONNECTED = 0
    m:close()

    tmr.alarm(RECONNECT_TIMER, TIMER_TIMEOUT, tmr.ALARM_AUTO, connect_to_broker)
end

function handle_connection_error (client, reason)
    print("Failed reason: "..reason)
end

function connect_to_broker()
    print ("Waiting for the broker")
    m:connect(
        BROKER, BRPORT, 0,
        function (client)
            print("Connected to MQTT:" .. BROKER .. ":" .. BRPORT .." as " .. CLIENTID )
            tmr.unregister(RECONNECT_TIMER)
            IS_BROKER_CONNECTED = 1
        end,
        handle_connection_error
    )
    m:on("offline", handle_broker_offline)
end

-------------------- GPIO HANDLING -----------------------------

function toggle_input()
    print("Input toggled")
    if gpio.read(INPUT_PIN) == 1 then
        gpio.write(TEST_PIN, gpio.LOW)
    else
        gpio.write(TEST_PIN, gpio.HIGH)
    end
end

function gpio_handling()
    print("GPIO handling started")

    gpio.mode(INPUT_PIN, gpio.INT)
    gpio.trig(INPUT_PIN, "up", publish_data)

    -- it is only for testing purposes - toggle input every TIMER_TIMEOUT
    gpio.mode(TEST_PIN, gpio.OUTPUT)
    tmr.alarm(GPIO_TIMER, TIMER_TIMEOUT, tmr.ALARM_AUTO, toggle_input)
end

----------------------------------------------------------------

print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( CLIENTID, MQTT_KEEPALIVE, BRUSER, BRPWD)
connect_to_broker()
gpio_handling()
