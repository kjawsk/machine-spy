BROKER = "192.168.0.103"
BRPORT = 8883
BRUSER = ""
BRPWD  = ""
CLIENTID = "ESP8266-" ..  node.chipid()
INPUT_PIN = 1
TEST_PIN = 2
GPIO_TMR_TIMEOUT = 5000
MQTT_TMR_TIMEOUT = 2000
MQTT_KEEPALIVE = 120
GPIO_TIMER = 0
RECONNECT_TIMER = 1
is_broker_connected = 0
tick_counter = 0

-------------------- MQTT HANDLING -----------------------------

function publish_data()
    tick_counter = tick_counter + 1
    if is_broker_connected == 1 then
        m:publish("/test",
            CLIENTID .. '/' .. tick_counter,
            0,0, function(conn) print("Sending data: " .. tick_counter) end)
        tick_counter = 0
    end
end

function handle_broker_offline(client)
    print ("Connection to the broker is lost. Reconnecting...")
    is_broker_connected = 0
    m:close()

    tmr.alarm(RECONNECT_TIMER, MQTT_TMR_TIMEOUT, tmr.ALARM_AUTO, connect_to_broker)
end

function handle_connection_error (client, reason)
    print("Failed reason: "..reason)
end

function connect_to_broker()
    print ("Waiting for the broker")
    tls.cert.verify(true)
    m:connect(
        BROKER, BRPORT, 1,
        function (client)
            print("Connected to MQTT:" .. BROKER .. ":" .. BRPORT .." as " .. CLIENTID )
            tmr.unregister(RECONNECT_TIMER)
            is_broker_connected = 1
        end,
        handle_connection_error
    )
    m:on("offline", handle_broker_offline)
end

-------------------- GPIO HANDLING -----------------------------

function toggle_input()
    if gpio.read(INPUT_PIN) == 1 then
        gpio.write(TEST_PIN, gpio.LOW)
    else
        gpio.write(TEST_PIN, gpio.HIGH)
        print("Rising edge! " .. tick_counter)
    end
end

function gpio_handling()
    print("GPIO handling started")

    gpio.mode(INPUT_PIN, gpio.INT)
    gpio.trig(INPUT_PIN, "up", publish_data)

    -- it is only for testing purposes - toggle input every GPIO_TMR_TIMEOUT
    gpio.mode(TEST_PIN, gpio.OUTPUT)
    tmr.alarm(GPIO_TIMER, GPIO_TMR_TIMEOUT, tmr.ALARM_AUTO, toggle_input)
end

----------------------------------------------------------------

print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( CLIENTID, MQTT_KEEPALIVE, BRUSER, BRPWD)
connect_to_broker()
gpio_handling()
