# CSSR Raspberry Pi Zero W Project

This project is a Collapsed Structure Search and Rescue (CSSR) system using:
- **MQ2 gas sensor** (connected via MCP3008 for CO2 and methane detection)
- **RCWL-0516 microwave motion sensor**
- **HC-SR04 ultrasonic distance sensor**
- **Raspberry Pi Zero W**

## Features
- Detects motion, gas levels, and distance
- Raises alerts if movement or gas signatures suggest human presence
- Designed for use in disaster scenarios like building collapse

## Wiring Overview

| Component       | Raspberry Pi GPIO | Notes                    |
|----------------|-------------------|--------------------------|
| MQ2 Sensor      | ADC CH0 (MCP3008) | Requires analog input    |
| MCP3008 (SPI)   | CLK: GPIO11, MISO: GPIO9, MOSI: GPIO10, CS: GPIO8 | Power with 3.3V |
| RCWL-0516       | GPIO17            | OUT pin connected        |
| HC-SR04 TRIG    | GPIO23            | Output trigger pin       |
| HC-SR04 ECHO    | GPIO24            | Input echo pin           |

## Requirements

Install dependencies:
```bash
pip3 install adafruit-blinka adafruit-circuitpython-mcp3xxx RPi.GPIO
```

## Running the Code

```bash
python3 cssr_pi_zero.py
```

## Notes
- The gas readings are based on the analog value via MCP3008. Real ppm conversion requires proper calibration.
- This code assumes a 3.3V logic level on the Raspberry Pi.
