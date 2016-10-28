-- initiate the mqtt client and set keepalive timer to 120sec
print("main")
m = mqtt.Client("client_id", 120, "username", "password")

m:on("connect", function(con) print ("connected") end)
m:on("offline", function(con) print ("offline") end)

-- on receive message
m:on("message", function(conn, topic, data)
  print(topic .. ":" )
  if data ~= nil then
    print(data)
  end
end)

m:connect("192.168.0.103", 1884, 0, function(conn) 
  print("connected")
  -- subscribe topic with qos = 0
  m:subscribe("/my_topic",0, function(conn)
    -- publish a message with data = my_message, QoS = 0, retain = 0
    m:publish("/test","my_message",0,0, function(conn) 
      print("sent") 
    end)
  end)
end)
