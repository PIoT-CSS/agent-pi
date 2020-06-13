## Car Share System (CSS): Agent Pi

**Car Share System** is a full-stack car-share rental service system that runs on ***Raspberry Pi(s)*** while utilising ***IoT elements*** such as use of ***socket programming with MQTT pub/sub, facial recognition, QR generation and detection, Bluetooth technology and also Google Assistant SDK*** to complete the application suite.

![Car Share System Architecture Diagram](https://media.discordapp.net/attachments/429105317293326346/720991280699539616/Blank_Diagram.png?width=1098&height=921)

<center><strong>Car Share System Architecture Diagram</strong></center>

Skip to [Installation](#installation)

## Agent Pi Features (Console Menu)

- **User authentication system**:
  - Customers can choose to unlock the car by authenticating with either:
    - Facial recognition
    - Username/password
  - Engineers unlocks the car (*for repairing purposes only*) with his/her nominated Bluetooth device with Bluetooth MAC address matching (by ensuring device is discoverable)
- **Issue resolver system for engineers**:
  - After authentication, engineers can scan their **QR code** and enter an issue ID (that's will be marked as resolved by the engineer) and the data will be published to the Master Pi
- **MQTT pub/sub system**, allowing it to publish/receive data to/from Master Pi:
  - Receive customer's photo when customer authenticates with facial recognition option
  - Publish facial recognition result to Master Pi
  - Receive customer authentication verification result from Master Pi when customer authenticates with username/password
  - Receive all engineers' Bluetooth MAC addresses from Master Pi for unlocking car with engineer's nominated Bluetooth device
  - Publish issue ID and engineer's profile details to Master Pi to mark issue as resolved

## Installation

#### Dependencies installation:

It is recommended that you have **enabled virtual environment**. Execute the following in root folder:

```bash
pip3 install -r requirements.txt
```

#### To run:

***Modify `.env` file when required to configure MQTT config.**

Have 2 terminal windows/tabs, execute the following in root folder:

**To start MQTT subscriber in the background:**

```bash
python3 startup.py
```

**To run the Agent Pi console menu:**

```bash
python3 menu.py
```
