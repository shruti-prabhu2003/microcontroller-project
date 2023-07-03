import time
import network
import socket
from machine import Pin

relay1 = Pin(15, Pin.OUT)
ledState = 'LED State Unknown'
relay2=Pin(16,Pin.OUT)
relay3=Pin(21,Pin.OUT)
ssid = 'Shruti'
password = 'dubb3619'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body{
            font-family:Arial;
            text-align: center;
            margin: 0px auto;
            padding-top:30px;
            background-image: url("bg photo.jpg");
              background-position: center;
              background-repeat: no-repeat;
              background-size: cover;
              color: black;
        }
        .switch{
            position:relative;
            display:inline-block;
            width:120px;
            height:68px
        }
        .switch input{
            display:none
        }
        .slider{
            position:absolute;
            top:0;
            left:0;
            right:0;
            bottom:0;
            background-color:#ccc;
            border-radius:34px
        }
        .slider:before{
            position:absolute;
            content:"";
            height:52px;
            width:52px;left:8px;bottom:8px;
            background-color:#fff;
            -webkit-transition:.4s;
            transition:.4s;
            border-radius:68px
        }
        input:checked+.slider{background-color:#2196F3}
        input:checked+.slider:before{
            -webkit-transform:translateX(52px);
            -ms-transform:translateX(52px);
            transform:translateX(52px)
        }
        </style>
        <script>
        function toggleCheckbox(element,relay_num)
        {
            var xhr = new XMLHttpRequest();
            if(element.checked){
                xhr.open("GET", "/?relay"+relay_num +"=on", true);
            }
            else {
                xhr.open("GET", "/?relay"+relay_num +"=off", true);
            }
            xhr.send();
        }
       
        </script>
    </head>
    <body>
        <h1>WELCOME TO REMOTE ON OFF SWITCH ARENA</h1>
        <h2>using Raspberry pi PICO W</h2>
        <h3>Project by: </h3>
        <h3>SHRUTI PRABHU 2021200096</h3>
        <h3>SAKSHI PAWANE 2021200091</h3>
    <label class="switch">
      <input type="checkbox" onchange="toggleCheckbox(this,1)" %s>
      <span class="slider">
      </span></label>
    <label class="switch">
        <input type="checkbox" onchange="toggleCheckbox(this,2)" %s>
        <span class="slider"></span>
    </label>
    <label class="switch">
        <input type="checkbox" onchange="toggleCheckbox(this,3)" %s>
        <span class="slider"></span>
    </label>
    </body>
    </html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        relay1_on = request.find('relay1=on')
        relay1_off = request.find('relay1=off')
        relay2_on = request.find('relay2=on')
        relay2_off = request.find('relay2=off')
        relay3_on = request.find('relay3=on')
        relay3_off = request.find('relay3=off')
        
       
        
        if relay1_on == 8:
            print("led on")
            relay1.on()
        if relay1_off == 8:
            print("led off")
            relay1.off()
        if relay2_on == 8:
            print("led on")
            relay2.on()
        if relay2_off == 8:
            print("led off")
            relay2.off()
        if relay3_on == 8:
            print("led on")
            relay3.on()
        if relay3_off == 8:
            print("led off")
            relay3.off()
        
        
        
        
        # Create and send response
        
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')