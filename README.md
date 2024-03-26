# Python_APP
<a href="http://www.youtube.com/watch?v=BNPRGuqg0ew
" target="_blank"><img src="/image/YT_screenshot.jpg" 
alt="IMAGE ALT TEXT HERE" width="400" height="220" border="10" /></a>

## Introduction of MPO-2000
The MPO series are the first oscilloscopes from GW Instek capable of __executing Python scripts__ directly on the device. Under the control of Python scripts, the MPO can control external USB devices for collaborative testing, enabling the realization of __small-scale automation and semi-automation testing systems__.
<img src="/image/automation_test_system2.png" alt="Image Description" width="500" height="360">

The MPO-2000 series combines multiple measuring instruments into one unit, making it particularly suitable for educational applications. Under the control of Python scripts, it can achieve various functions that were previously impossible with standalone oscilloscopes, such as __plotting BJT I-V characteristic curves__ (The use of __GDP-025__ is required to convert the current value).
<img src="/image/automation_test_system1.png" alt="Image Description" width="500" height="360">
<img src="/image/bjt01.png" alt="Image Description" width="400" height="300">
<img src="/image/bjt_I_V_curve.png" alt="Image Description" width="400" height="240">

We have compiled various __Python modules__ required for writing MPO Python scripts(such as vertical division/positions, horizontal division/positions, trigger modes, Arbitrary Waveform Generators, Digital Multimeters, Programmable DC Power Supplies, and other commonly used control functions)here for user reference and modification as needed.

The MPO-2000 comes with various __pre-installed Python apps__, and their source code can be directly copied from the menu functions. Users can modify them according to their testing requirements.

Here we also provide some Python example scripts that are not available on the MPO machine for users to reference.

### The MPO-2000 Can Control External USB Devices Through Python Scripts
Under Python script control, MPO-2000 can communicate with external USB devices through the USB interface using the __USB CDC-ACM__ protocol for collaborative testing.

Connectable devices include the __PSW__, __PFR__, __PPX__, __PEL__, __GDM__ series, and MPO can also control external devices via __LAN__ using the __socket__ protocol.

This feature makes MPO suitable for small-scale automation and semi-automation testing applications, saving engineers considerable time and effort.

### MPO-2000 Is Suitable for Educational and Industrial Applications
MPO-2000's five-in-one functionality combined with Python scripts enables various applications, such as:
   * BJT I-V characteristic curves
   * LED I-V characteristic curve
   * MQTT data uploading to the cloud
   * MQTT subscriber for remote control
   * Event notifications with community software like WeChat
   * Component endurance testing
   * Automatic data collection in experiments
   * Measurement of circuit frequency vs. temperature characteristics
   * Measurement applications combined with barcode scanners.

### Other features
MPO-2000 also features:
   * Simultaneous display of spectrum analysis for two channels, with simultaneous __spectrogram plot__.
   * Signal decoding functions for __UART__, __I2C__, __SPI__, __CAN__ and __LIN__ serial bus, as well as for __CAN-FD__, __USB 2.0 Full Speed__, __FlexRay__, __I2S__ and __USB Power Delivery__ communication protocols.
   * __Web Server__ and __Web Control__ functions, enabling dynamic waveform observation and remote control within the same local network using a PC or smartphone browser.

## Feature Limitation
If you need to write Python scripts on the MPO-2000 to __control external USB devices__ or utilize __Python plotting libraries__ for menu design or charting, you must purchase the Professional version. The Professional version also includes the capability to package .py files into Python __APP installation files__.

Although the Basic version has limited Python capabilities, Python APPs that utilize GUI libraries and control external USB devices can still run on machines with the Basic version.

## Related Information
For further information about the product, you can visit the [MPO product page](https://www.gwinstek.com/en-global/products/detail/MPO-2000) on the GW Instek website.

If you want to learn more about Python programming on MPO, you can check out the document below. => [MPO-2000 Python Tutorial and Application Handbook](https://www.gwinstek.com/en-global/products/detail/MPO-2000) (on the download page)

```MPO-2000B users can upgrade to full MPO-2000P functionality with the optional MP2-PRO package```
