
import dso_gui
import dso_colors as color
from dso_const import *
import gds_info as gds

if __name__ == '__main__':
    # Initialize the DSO
    dso = gds.Dso()
    dso.connect()
    dso.default()
    dso.channel.set_on(kCH1)
    dso.channel.set_on(kCH2)
    
    # Initialize the AWG
    dso.awg.set_on(kCH1, 'SINE')
    dso.awg.set_on(kCH2, 'SINE')
    dso.awg.set_phase(kCH1, 0)
    dso.awg.set_phase(kCH2, 90)
    dso.opc()
    
    # Initialize the GUI
    gui = dso_gui.DrawObject()
    gui_chart = gui.Draw_Chart(gui)
    gui_chart.set_chart_style()
    
    # Plot the chart
    info = gui_chart.ch_info()
    info.x_data = dso.get_waveform_num(kCH1, real_value=False, pos_consider=True)
    info.y_data = dso.get_waveform_num(kCH2, real_value=False, pos_consider=True)
    info.x_scale = dso.channel.get_scale(kCH1)
    info.y_scale = dso.channel.get_scale(kCH2)
    info.x_pos = dso.channel.get_pos(kCH1)
    info.y_pos = dso.channel.get_pos(kCH2)
    info.color = color.LTGREEN
    gui_chart.draw_chart(info)

    