Welcome to mpo_api's documentation!
===================================
The MPO-2000 supports the execution of Python scripts, which is based on MicroPython V1.19.1. Users can place Python scripts on a USB flash disk and insert it into the USB slot of the MPO-2000, or copy the Python scripts to the internal disk for execution. Here we have compiled the documentation for the Python API of the main functions of the MPO, as well as the documentation for the Python API of several external devices.

Important Considerations for Using MPO's API
--------------------------------------------
   * Please ensure your MPO-2000 is version V1.04 or newer before starting Python programming.
   * Please refer to the `MicroPython standard library documentation for version V1.19.1 <https://docs.micropython.org/en/v1.19.1/library/index.html>`_.
   * The Python GUI Library for MPO is based on LVGL version 8.3. Users who need to utilize graphics and UI design features can refer to the `LVGL documentation for version 8.3 <https://docs.lvgl.io/8.3/_downloads/39cea4971f327964c804e4e6bc96bfb4/LVGL.pdf>`_ on the LVGL official website.
   * Most MicroPython standard library modules implement a subset of the functionality of their equivalent Python 3 modules.
   * When calling multiple API functions consecutively, it is important to include some delay to ensure that the previous control commands have been fully executed. Additionally, at lower speed timebase, the oscilloscope sampling may take more time. Avoid querying the oscilloscope for automatic measurement data before the sampling is complete, as this may result in incorrect data.

Usage for mpo_api
-----------------
.. code-block:: python

    try:
        # This module is a built-in module
        import gds_info as gds
    except ImportError:
        # Or you can import specific module
        import dso2kp as gds
    
    dso = gds.Dso()
    dso.connect() # connect as internal port
    
    # Now you should control your DSO, add your code below.
    # ========
    dso.channel.set_on(2) # Set CH2 to ON
    dso.channel.set_off(2) # Set CH2 to OFF
    dso.awg.set_on(1, wave='SQUAre', freq=10e3) # Set AWG1 ON and waveform is SQUARE, frequency is 10e3
    dso.awg.set_off(1) # Set AWG1 OFF
    # ========
    
    # Don't forget to close the connection.
    dso.close()

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dso2kp
   dso_acquire
   dso_awg
   dso_basic
   dso_bus
   dso_channel
   dso_colors
   dso_const
   dso_display
   dso_dmm
   dso_draw
   dso_gonogo
   dso_gui
   dso_hardcopy
   dso_math
   dso_meas
   dso_power_supply
   dso_ref
   dso_sns
   dso_spectrum
   dso_timebase
   dso_trigger
   load
   psw
   gdm
   asr

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

