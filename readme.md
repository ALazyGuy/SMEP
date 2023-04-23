# Smart Messages Exchange Protocol

---

## Message structure

| Name         | Size              |
|--------------|-------------------|
| Device Id    | 1 byte            |
| Message Type | 1 byte            |
| Fields       | (1 + n) * m bytes | 

### Device Id

**Device id** indicates which type of device is sending the message.

### Implemented device ids

| Name       | Value |
|------------|-------|
| Controller | 0x0   |
| Kettle     | 0x1   |

### Message type

**Message type** used to parse messages more effectively.

| Value | Name         | Side |
|-------|--------------|------|
| 0x0   | Initial Scan | SRV  |
| 0x1   | Online       | CL   |
| 0x2   | Accepted     | SRV  |
| 0x3   | Accepted     | CL   |
| 0x4   | Update       | SRV  |
| 0x5   | Update       | CL   |
| 0x6   | Error        | SRV  |
| 0x7   | Error        | CL   |

+ **Initial Scan** - message sent to all connected to LAN devices to identify
  which of them can be connected to the server.

  *No fields expected*


+ **Online** - message sent to the server to indicate that current
  device is online and ready to connect.

  *No fields expected*


+ **Accepted(Server/Client)** - message sent to device/server means that previous message
  has been accepted and processed successfully(has to be used as response message only).

  *No fields expected*


+ **Update(Server/Client)** - message sent to device/server means that sender's state
  has changed.

  *Fields are specific for each device*


+ **Error(Server/Client)** - message sent to device/server means that previous message
  processing was failed(has to be used as response message only).

  *Field -> ErrorType*

### Error types

| Name            | Value |
|-----------------|-------|
| UNKNOWN_DEVICE  | 0x0   |
| INVALID_MESSAGE | 0x1   |

---

## Handshake

1) Server does scan for all devices connected to specific network by sending initial scan message(0x0) to all devices
2) Every device which is available in current network respond with both accepted(0x3) and online(0x1) messages
3) Server saves each device to local storage with all provided data and sends accepted(0x2) message to all connected
   devices
