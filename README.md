# TIP_Project
A simple voice communicator in python for a studies project created in teams of two

## Installing requirements
The intentional way of installing dependencies is running `pip install -r requirements.txt` command. However installation of PyAudio on Windows systems might result in error. If it does, then download appropriate binary file form [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio). For example if you have python 3.9.1 64-bit version you want to download `PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl` file.

It is highly recomended to use virtual enviroment

## Running the server
Server can be run by executing command
```
python Server/run.py <port>
```
where the port variable is optional and default port is `9999`. Port also can be set using enviroment variable named `PORT`. Server runs on all interfaces.

## Running the client
Client UI can be run from the realsed package from [here](https://github.com/Niewidzialny84/TIP_Project/releases) or using the python command
```
python Client/client.py
```

## Communication schema
The server and client communicates using both TCP and UDP sockets where TCP is used as control to the connection, the UDP is used as voice delivery. Both apps share the same package wraping utility tool. TCP packages contain json values.
### Default communication schema
By default to be allowed for proper communication some values must me established in a simple exchange:
1. Client connects to socket, sends nickname
2. Server recives nickname adds it to connected users table and sends to all clients updated client list
3. Server responds to a nickname sending sessionID 
4. Client sends binded UDP port where voice datagrams will be transfered
5. Communication can begin, voice packets are tranfered between users on UDP sockets
6. (Optionally) Server disconnects or client disconnects sending respective packages

### Table of packages
All presented packages contain `KEY` value which is used as a number describing package name.
<table>
    <tr>
      <th>Package Name</th>
      <th>Required Values</th>
      <th>Optional values</th>
      <th>JSON Example</th>  
    </tr>
    <tr>
        <td>ACK</td>
        <td></td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 0}
            </code>
        </td>
    <tr>
    <tr>
        <td>UNKNOWN_ERROR</td>
        <td></td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 1}
            </code>
        </td>
    <tr>
    <tr>
        <td>SEND_NICKNAME</td>
        <td>NAME</td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 2, "NAME": "John"}
            </code>
        </td>
    <tr>
    <tr>
        <td>SEND_NEW_USERS</td>
        <td>USERS</td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 3, "USERS": ["John","Adam"]}
            </code>
        </td>
    <tr>
    <tr>
        <td>DISCONNECT</td>
        <td></td>
        <td>REASON</td>
        <td>
            <code type='json'>
            {"KEY": 4, "REASON": "Quit"}
            </code>
        </td>
    <tr>
    <tr>
        <td>SERVER_CLOSE</td>
        <td></td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 5}
            </code>
        </td>
    <tr>
    <tr>
        <td>SESSION</td>
        <td>SESSION</td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 6, "SESSION": 2}
            </code>
        </td>
    <tr>
    <tr>
        <td>CLIENT_PORT</td>
        <td>PORT</td>
        <td></td>
        <td>
            <code type='json'>
            {"KEY": 7, "PORT": 5253}
            </code>
        </td>
    <tr>
</table>