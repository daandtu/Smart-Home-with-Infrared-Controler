# Micropython Smart-Home with IR Controller

This project is a small Smart Home system which uses multiple Micropython-capable microcontrollers as peripheral IOT devices. They can be controlled from a PC or mobile app. All components are connected via server.  
Furthermore, the microcontrollers can be used to send IR signals to different devices.  
The structure is shown in the following image:
![System structure](Server/structure.png)

### Protocol
All devices connect to the server via a ssl websocket. After the connection is established the peripheral device authenticates itself with a password. Afterwards it can subscribe to multiple topics. When one device in the network sends a message to a certain topic all other devices which subscribed to that topic receive the message.  
Each message to the server consists of a string where the first character defines the message type (i.e. authentication, subscription, unsubscription, normal message, or termination of the connection).
The idea is to have multiple microcontroller which can have various different smart home functionalities (e.g. switching on some light or tv). The commands for the according actions are sent via the server from different controlling devices like an Android app. Furthermore, it is possible to receive status updates from the microcontrollers on the controlling devices. Depending on the server, it is possible to control all actions from anywhere in the world.  
The ssl websocket and the password authentication creates a (weak) security layer.

### IR controls
The system includes functions to receive and send different infrared codes based on the [NEC Infrared Transmission Protocol](https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol) to various devices. With the reciver feature it is possible to first record the infrared code from an IR remote and than simulate it to control the respective device via the simulated commands.  
Because regular micropython is too slow to generate the required 38kHz signal bursts the code uses some [viper code](http://docs.micropython.org/en/latest/reference/speed_python.html#the-viper-code-emitter) for the frequency generation.

### Unimplemented features
The number of implemented features for the microcontrollers is limited and focuses on the control of IR devices. Although the connection to the server requires a password for authentication, the security of the system should be definitely improved.