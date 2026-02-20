# Digital Out Setup in Bittium NeurOne 

<p align="center">
  <img src="https://github.com/biomaglab.png" width="100px" alt="Logo Biomag">
</p>

> Step-by-step procedure to enable real-time data acquisition from Bittium NeurOne device.

## 🚀 Quick Setup

### Step 1: Protocol Tab

The “Real-time Out” subtab provides controls for the Digital Output. To enable it, click Real-time Out in the Protocol subtab.

<p align="center">
  <img src="docs\images\digitalOut1.jpg" width="800px" alt="Protocol tab">
</p>

The amplifier must be connected to the serial port of the computer using the connection for UDP transfer (RJ45) (see pg 34 of the Bittium NeurOne User Manual)

### Step 2: Enable Digital Out

Enable Digital Output by clicking on the button to provide additional control buttons on the tool bar.

<p align="center">
  <img src="docs\images\digitalOut2.jpg" width="800px" alt="Enable Digital Out">
</p>

Cogwheel button will open setting of Digital Out.

### Step 3: Define communication parameters

<p align="center">
  <img src="docs\images\digitalOut3.jpg" width="800px" alt="Define parameters">
</p>

- Define packet frequency as 1000 Hz.
- Type in the IP address of the computer you will be using to run the Biomag TMS Dashboard.
- Define the Target UDP Port as 50000.
- Click "Send triggers as Packets"
- Enable "Send Packets MeasurmentStart and MeasurementEnd"
- Click OK.

As a trigger is detected during EMG acquisition, the MEP chart will be updated in the Biomag TMS Dashboard.

