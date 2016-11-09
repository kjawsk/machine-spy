function main()
  print "main"
  tmr.alarm(1, 5000, tmr.ALARM_AUTO, publish_data)
end

function publish_data()
    m:publish("/test","publish_data" .. node.chipid(),0,0, function(conn)
        print("Sending data")
    end)
end

print "Connecting to MQTT broker. Please wait..."
m = mqtt.Client( "ESP8266-" .. node.chipid(), 120, "", "")
m:connect("192.168.0.103", 1884, 0, main)
