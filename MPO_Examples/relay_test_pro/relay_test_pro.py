# Name: relay_test_pro.py
#
# Description: The relay is connected in series with the 
# external power supply and electronic load, and set the 
# electronic load to pull current in sequence.  
# Simultaneously utilize the internal power supply of the 
# DSO to control the ON-OFF state of the NO/NC COM 
# terminals of the Relay.
#
# Author: Derek Chung
#
# Documentation:
#   https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import os
import time
import sys
import gc
import lvgl as lv

debug_lvls = {
    'off': 0,
    'param_config': 1,
    'progress': 2,
    'end': 3,
}

cfg = {
    'test_loops': 3,
    'debug_lvl': debug_lvls['off'],  # off
    # Power PFR-100M
    'pwr_serial_number': 'GER200751',
    'OCP': 2.2,  # amps
    'OVP': 55,  # volts
    'current': 1.1,  # amps.
    'voltage': 5,  # volts.
    # Load PEL-3032E
    'load_serial_number': 'GES140272',
    'nseq_memo': 'RELAY_TEST',
    'nseq_loops': 1,
    'nseq_total_step': 3,
    'nseq_range': 'IHVH',
    'step1_hrs': 0,  # hours
    'step2_hrs': 0,
    'step3_hrs': 0,
    'step1_mins': 0,  # minutes
    'step2_mins': 0,
    'step3_mins': 0,
    'step1_secs': 0,  # seconds
    'step2_secs': 6,
    'step3_secs': 24,
    'step1_ms': 100,  # milliseconds
    'step2_ms': 0,
    'step3_ms': 0,
    'step1_current': 1.2,  # amps.
    'step2_current': 0.7,
    'step3_current': 0.0,
    # DSO
    'to_coil_dso_power_ch': 1,
    'to_coil_dso_power_volt': 12.0,
    'current_probe_ch': 1,
    'probe_attenuation': 5,  # current probe range: 200mA
    'vertical_scale': 0.5,  # 500mA
    'dso_mode': 'single',  # single / roll
    'horizontal_scale_single': 0.05,  # 50ms
    'horizontal_scale_roll': 2,  # 2secs
    'trigger_level': 0.5,
}

def __str_type_chk(line):
    try:
        return int(line)
    except ValueError:
        pass
    try:
        return float(line)
    except ValueError:
        pass
    try:
        return list(map(float, line.split(',')))
    except ValueError:
        d = {'ON': True, 'OFF': False}
        return d.get(line.upper(), str(line))

def loadfile2dict(sour, dest):
    try:      
        with open(sour,'r') as f:
            for line in f:
                if line[0] != '#' and len(line.split()) != 0:
                    r = __str_type_chk(line.split('=')[1].strip())
                    dest[line.split('=')[0].strip()] = r
    except:
        dso.dsodraw.draw_poptext('Load file error')
        sys.exit()

def instruments_init() -> None:
    try:
        pwr.connect(SN=cfg['pwr_serial_number'])
        dso.dsodraw.draw_poptext(f'Connect to: {pwr.idn()}')
    except:
        dso.dsodraw.draw_poptext('Failed to connect to power!')
        raise SystemExit 

    try:
        load.connect(SN=cfg['load_serial_number'])
        dso.dsodraw.draw_poptext(f'Connect to: {load.idn()}')
    except:
        dso.dsodraw.draw_poptext('Failed to connect to load!')
        raise SystemExit 

def create_textarea() -> lv.textarea:
    # Draw a rectangle on the canvas
    RECT_X_POS = 25
    RECT_Y_POS = 230
    RECT_WIDTH = 240
    RECT_HEIGHT = 165
    gui.draw_fillrect_ex(RECT_X_POS, RECT_Y_POS, RECT_WIDTH, RECT_HEIGHT, color=color.MIDGRAY)

    # Create a label above the text box
    label = lv.label(lv.scr_act())
    label.set_text('Screen max current :')
    label.align(lv.ALIGN.OUT_TOP_LEFT, RECT_X_POS + 10, RECT_Y_POS + 5)

    # Create the text area
    ta: lv.textarea = lv.textarea(lv.scr_act())
    ta.set_one_line(False)
    ta.align(lv.ALIGN.OUT_TOP_LEFT, RECT_X_POS + 10, RECT_Y_POS + 25)
    ta.set_size(RECT_WIDTH - 20, RECT_HEIGHT - 35)
    ta.set_max_length(1000)  # The maximum number of characters
    return ta

def configure_relay_test_parameters() -> None:
    dso.stop()
    # Set parameters of the current probe.
    dso.channel.set_probe_type(ch=cfg['current_probe_ch'], type='CURRENT')
    dso.channel.set_probe_ratio(ch=cfg['current_probe_ch'], ratio=cfg['probe_attenuation'])  # current probe range: 200mA
    dso.channel.set_scale(ch=cfg['current_probe_ch'], scale=cfg['vertical_scale'])
    horizontal_scale = cfg['horizontal_scale_single'] if cfg['dso_mode'] == 'single' else cfg['horizontal_scale_roll']
    dso.timebase.set_timebase(hdiv=horizontal_scale)
    dso.trigger.set_level(value=cfg['trigger_level'])
    if cfg['debug_lvl'] == debug_lvls['param_config']:
        print(f"Probe type={dso.channel.get_probe_type(ch=cfg['current_probe_ch'])}, probe ratio={dso.channel.get_probe_ratio(ch=cfg['current_probe_ch'])}")
        print(f"Vertical scale:{dso.channel.get_scale(ch=cfg['current_probe_ch'])}, horizontal scale:{dso.timebase.get_timebase()}")

    # Set the dso power supply connected to coil terminals of relay.
    dso.power.set_voltage(ch=cfg['to_coil_dso_power_ch'], volt=cfg['to_coil_dso_power_volt'])

    # Set the power connected to the common terminal of relay.
    pwr.set_off()
    pwr.set_mode(mode=1)  # CCHS
    pwr.set_ocp(current=cfg['OCP'])
    pwr.set_ovp(voltage=cfg['OVP'])
    pwr.set_current(value=cfg['current'])
    pwr.set_voltage(value=cfg['voltage'])

    # Set the Load connected to the NO terminal of relay.
    load.set_off()
    load.set_mode(mode=2)  # Normal sequence
    load.delete_all_nseq()
    load.set_nseq_para(start=1, seq_no=1, memo=cfg['nseq_memo'], mode='CC', range=cfg['nseq_range'], loop=cfg['nseq_loops'], last_load='OFF', last_value=0.0, chain='OFF')
    load.set_nseq_data_edit(step=1, total_step=cfg['nseq_total_step'], load_value=cfg['step1_current'], hours=cfg['step1_hrs'], minutes=cfg['step1_mins'], seconds=cfg['step1_secs'], milliseconds=cfg['step1_ms'], load_state='ON', RAMP='OFF', trig_out='OFF', pause='OFF')
    load.set_nseq_data_edit(step=2, total_step=cfg['nseq_total_step'], load_value=cfg['step2_current'], hours=cfg['step2_hrs'], minutes=cfg['step2_mins'], seconds=cfg['step2_secs'], milliseconds=cfg['step2_ms'], load_state='ON', RAMP='OFF', trig_out='OFF', pause='OFF')
    load.set_nseq_data_edit(step=3, total_step=cfg['nseq_total_step'], load_value=cfg['step3_current'], hours=cfg['step3_hrs'], minutes=cfg['step3_mins'], seconds=cfg['step3_secs'], milliseconds=cfg['step3_ms'], load_state='OFF', RAMP='OFF', trig_out='OFF', pause='OFF')
    load.save_nseq()
    load.set_nseq_state('ON')

    if cfg['debug_lvl'] == debug_lvls['param_config']:
        time.sleep(1.5)
        print(f"Normal Sequence parameters: {load.get_nseq_para()}")
        for i in range(3):
            load.set_nseq_edit_point(point=i + 1)
            time.sleep(0.5)
            print(f"Step{load.get_nseq_edit_point()}: {load.get_nseq_data_edit()}")

def perform_relay_test() -> None:
    dso.dsodraw.draw_poptext('Relay test start.')
    step1_duration = cfg['step1_hrs'] * 3600 + cfg['step1_mins'] * 60 + cfg['step1_secs'] + cfg['step1_ms'] / 1000
    step2_duration = cfg['step2_hrs'] * 3600 + cfg['step2_mins'] * 60 + cfg['step2_secs'] + cfg['step2_ms'] / 1000
    step3_duration = cfg['step3_hrs'] * 3600 + cfg['step3_mins'] * 60 + cfg['step3_secs'] + cfg['step3_ms'] / 1000

    load.opc()
    pwr.opc()
    if cfg['dso_mode'] == 'roll': dso.run()
    dso.opc()
    if cfg['debug_lvl'] == debug_lvls['progress']: time_info = []
    for i in range(cfg['test_loops']):
        if cfg['dso_mode'] == 'single': dso.single(), time.sleep(0.5)

        if cfg['debug_lvl'] == debug_lvls['progress']: start_time = time.time()

        load.set_on()
        pwr.set_on()

        # Turn on the DSO power supply to provide power to the coil.
        dso.power.set_on(ch=cfg['to_coil_dso_power_ch'])

        # Set the actual current draw to be one second less than the current draw set by the electronic load.
        time.sleep(step1_duration + step2_duration - 1)

        dso.power.set_off(ch=cfg['to_coil_dso_power_ch'])

        mode_prefix = 'Until loop' if cfg['dso_mode'] == 'roll' else 'Loop'
        lv.textarea.add_text(ta, f"{mode_prefix} {i + 1}:  {dso.meas.get_max(cfg['current_probe_ch']):.2f} A\n")

        time.sleep(1 + step3_duration)

        if cfg['dso_mode'] == 'single': dso.stop()
        pwr.set_off()
        load.set_off()

        if cfg['debug_lvl'] == debug_lvls['progress']:
            end_time = time.time()
            time_info.append([start_time, end_time])

        if cfg['dso_mode'] == 'single': time.sleep(0.5)
        gc.collect()
    if cfg['dso_mode'] == 'roll': dso.stop()   
    if cfg['debug_lvl'] == debug_lvls['progress']:
        for idx, info in enumerate(time_info):
            print(f"Execution time of step{idx + 1}：{info[1] - info[0]} s")

def instruments_close() -> None:
    dso.close()
    load.opc()
    if cfg['debug_lvl'] == debug_lvls['end']:
        print('pwr.is_on():', str(pwr.is_on()))
        print('load.is_on():', str(load.is_on()))

if __name__ == '__main__':
    os.chdir(sys.path[0])
    from dso_const import *
    try:
        import gds_info as gds
    except ImportError:
        import dso2kp as gds
    import dso_gui
    import dso_colors as color
    import psw
    import load

    dso = gds.Dso()
    dso.connect()
    gui = dso_gui.DrawObject()
    pwr = psw.Psw()
    load = load.Load()
    loadfile2dict('relay_test_pro.txt', cfg)
    time.sleep(1)
    instruments_init()
    time.sleep(2)
    configure_relay_test_parameters()
    time.sleep(1)
    dso.opc()
    ta: lv.textarea = create_textarea()

    test_start_time = time.time()
    perform_relay_test()
    test_end_time = time.time()
    if cfg['debug_lvl'] == debug_lvls['progress']: print(f"Total execution time: {test_end_time  - test_start_time} s")

    dso.dsodraw.draw_poptext("The demo has completed.")
    instruments_close()
    sys.exit()