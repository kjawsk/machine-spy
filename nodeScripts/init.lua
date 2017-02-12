dofile("credentials.lua")

function startup()
    if file.open("init.lua") == nil then
        print("init.lua deleted or renamed")
    else
        print("Running")
        file.close("init.lua")
        dofile("main.lua")
    end
end

print("Connecting to WiFi access point...")
wifi.setmode(wifi.STATION)
wifi.sta.config(SSID,PASSWORD)
-- wifi.sta.connect() not necessary because config() uses auto-connect=true by default
tmr.alarm(1, 1000, 1, function()
    if wifi.sta.getip() == nil then
        print("Waiting for IP address...")
    else
        tmr.stop(1)
        print("WiFi connection established, IP address: " .. wifi.sta.getip())
        print("You have 3 seconds to abort")
        print("Waiting... ")
        print(tls.cert.verify([[
        -----BEGIN CERTIFICATE-----
        MIIDpzCCAo+gAwIBAgIJANbWLRIOD3PEMA0GCSqGSIb3DQEBDQUAMGoxFzAVBgNV
        BAMMDkFuIE1RVFQgYnJva2VyMRYwFAYDVQQKDA1Pd25UcmFja3Mub3JnMRQwEgYD
        VQQLDAtnZW5lcmF0ZS1DQTEhMB8GCSqGSIb3DQEJARYSbm9ib2R5QGV4YW1wbGUu
        bmV0MB4XDTE3MDIxMTE3MTk1NFoXDTMyMDIwODE3MTk1NFowajEXMBUGA1UEAwwO
        QW4gTVFUVCBicm9rZXIxFjAUBgNVBAoMDU93blRyYWNrcy5vcmcxFDASBgNVBAsM
        C2dlbmVyYXRlLUNBMSEwHwYJKoZIhvcNAQkBFhJub2JvZHlAZXhhbXBsZS5uZXQw
        ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDq18j/mekgEdQcpQXFy5YV
        6J53guWla7VBA25nbYXif1+HNSVlk6BQBm1CixIUK4ZW6e0/7BbZ1Pm25QMLgKeD
        ONcCmM2CB4QkJNDirHCyrK9DThe2Lcs0zNNWDa+EkAyWbH0ejwPlFtYV9GGaMHxI
        wgl/dix4d8DLcdaWdVly0MbHzxMVB+cbLBf1+i4PsE3crt95svUOs3m2upu8ycbq
        +oInnebrE7HWoBqXr0VWXlpAt2tsEy8pzSlEaSaCuvZVxzwfbcS7c8KV7kPP4hpz
        qTgvSkw6SfMH2oDAoY0hwJncn8XS+gJZHTO9DbuhU1/xg0vU09EWVa6mxfDDGxUF
        AgMBAAGjUDBOMB0GA1UdDgQWBBQCPNcs6/u8/E9Xut23a3CYf0EmuDAfBgNVHSME
        GDAWgBQCPNcs6/u8/E9Xut23a3CYf0EmuDAMBgNVHRMEBTADAQH/MA0GCSqGSIb3
        DQEBDQUAA4IBAQDgz9LK2DPbRxwXGAVfR8LOEAHvmCAfItBtX/0AbaZ6h2DouHxW
        QI00FcR2Z1ip56yq/k0XzcCHLXLftnjgslRSwADW2xo29Dgar+B7Ay1hLdAIXNDz
        T0fXKkMKz2V4f1yqZGII0Z2Y8gL3cTNEjoWaGjwkHAIQboF3zkjz/HFrT/C0x04S
        Bel9N3QKIeE+LpAWkeesPl2Jik/bnYX4aWDqhLJrXU7tobxPZ7QIXwwrugJN4IhO
        XE+5Xwjdz9E3kD1E2taIl3fu449KABkdEqBTdsCiVCKX9hzXEI+olEBTSfpoSbk3
        OIiUtrbi4/rEddqEYXo/MNaPpxgePOpK9vU3
        -----END CERTIFICATE-----
        ]]))
        collectgarbage()
        -- it is time to brake init
        tmr.alarm(0, 3000, 0, startup)
    end
end)
