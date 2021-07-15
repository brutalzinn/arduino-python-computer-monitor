import serial
ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port
ser.write('{"mem":"testeee"}\n'.encode('ascii')) # Convert the decimal number to ASCII then send it to the Arduino
ser.close()