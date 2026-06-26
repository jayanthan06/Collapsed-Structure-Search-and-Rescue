import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# RCWL-0516 Microwave Sensor
microwave_pin = 17
GPIO.setup(microwave_pin, GPIO.IN)

# Ultrasonic Sensor (HC-SR04)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# MCP3008 Setup (SPI)
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# === MQ2 Gas Sensor Reading Function ===
def read_gas_values():
    analog_value = mcp.read_adc(0)  # MQ2 connected to CH0
    voltage = (analog_value / 1023.0) * 3.3  # Convert to voltage (assuming 3.3V logic)
    # Approximate ppm (demo purposes; real-world needs calibration)
    co2_ppm = round(voltage * 1000, 2)
    methane_ppm = round(voltage * 700, 2)
    return co2_ppm, methane_ppm

# === Measure Distance Function (HC-SR04) ===
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = round(pulse_duration * 17150, 2)
    return distance_cm

# === Main Loop ===
try:
    while True:
        co2, methane = read_gas_values()
        movement_detected = GPIO.input(microwave_pin)
        distance = get_distance()

        print(f"\nEstimated CO2 Concentration: {co2} ppm")
        print(f"Estimated Methane Concentration: {methane} ppm")
        print("Microwave Sensor:", "Movement Detected" if movement_detected else "No Movement Detected")

        # Alert Logic
        if co2 > 1.5 or methane > 1.5:
            print("Alert: Living being suspected due to reasonable CO2 or Methane levels")
        if movement_detected:
            print("Alert: Living being suspected due to movement detected")
        if (co2 > 1.5 or methane > 1.5) and movement_detected:
            print("Alert: Living being suspected due to reasonable gas levels and movement detected")

        print(f"Distance to Object: {distance:.2f} cm")

        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program stopped by user.")
