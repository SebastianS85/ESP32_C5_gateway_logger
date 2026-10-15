# ESP32-C5 CAN FD Gateway Pinout

This document details the ESP32-C5 chip GPIO assignments compiled in `main/main.c`. 

> **Note:** GPIO numbers refer to the ESP32-C5 chip itself, not physical header pins on a development board. Verify against your board schematic before wiring.

## Master Pin Assignment

| Subsystem | Function | ESP32-C5 GPIO | Direction | Status | Connected Device / Target |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **I2C Bus** | SDA | `GPIO0` | Bidirectional | Active | OLED, DS3231MZ, PCF8574 |
| **I2C Bus** | SCL | `GPIO1` | Output | Active | OLED, DS3231MZ, PCF8574 |
| **CAN Node 1** | TWAI TX | `GPIO23` | Output | Active | Transceiver 1 `TXD` (TX input) |
| **CAN Node 1** | TWAI RX | `GPIO24` | Input | Active | Transceiver 1 `RXD` (RX output) |
| **CAN Node 2** | TWAI TX | `GPIO4` | Output | Active | Transceiver 2 `TXD` (TX input) |
| **CAN Node 2** | TWAI RX | `GPIO5` | Input | Active | Transceiver 2 `RXD` (RX output) |
| **SD Card (SPI)** | CS | `GPIO6` | Output | Reserved | `sdcard_service` (Unmounted) |
| **SD Card (SPI)** | MOSI | `GPIO8` | Output | Reserved | `sdcard_service` (Unmounted) |
| **SD Card (SPI)** | MISO | `GPIO9` | Input | Reserved | `sdcard_service` (Unmounted) |
| **SD Card (SPI)** | SCLK | `GPIO10` | Output | Reserved | `sdcard_service` (Unmounted) |

---

## CAN FD Interface & Wiring

Both TWAI channels operate using CAN FD frames with Bit-Rate Switching (BRS) enabled (`TWAI_USE_FD_FRAMES = 1`), requiring transceivers rated for up to **5 Mbit/s** in the data phase.

| Channel | TX Pin | RX Pin | Arbitration Rate | Data Phase Rate | Topology |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Node 1** | `GPIO23` | `GPIO24` | 1 Mbit/s *(typical)* | 5 Mbit/s | ESP32-C5 $\leftrightarrow$ Transceiver 1 $\leftrightarrow$ CAN Bus 1 |
| **Node 2** | `GPIO4` | `GPIO5` | 1 Mbit/s *(typical)* | 5 Mbit/s | ESP32-C5 $\leftrightarrow$ Transceiver 2 $\leftrightarrow$ CAN Bus 2 |

### Hardware Requirements
* **Transceivers:** ESP32-C5 TWAI pins are digital logic only. Connect each channel to an external 3.3 V-compatible CAN FD transceiver (or provide level shifting).
* **Grounding:** Tie the ESP32-C5 `GND` and both transceiver grounds together.
* **Termination:** Install **120 $\Omega$** resistors only at the two physical ends of each CAN bus—not at every individual node.

---

## I2C Bus Peripherals

All I2C peripherals share `GPIO0` (SDA) and `GPIO1` (SCL) at **400 kHz** using **3.3 V** logic and common `GND`.

| Device | Address | Max Bus Speed | Role / Notes |
| :--- | :---: | :---: | :--- |
| **OLED Display** | `0x3C` | 400 kHz | Status display |
| **DS3231MZ** | `0x68` | 400 kHz | Real-Time Clock (RTC) |
| **PCF8574** | `0x20` | 400 kHz | I2C I/O Expander |

* **Pull-up Resistors:** While the firmware enables internal ESP32-C5 pull-ups, external pull-up resistors (e.g., 2.2 k$\Omega$ to 4.7 k$\Omega$) sized for your total bus capacitance are strongly recommended for stable 400 kHz operation.

---

