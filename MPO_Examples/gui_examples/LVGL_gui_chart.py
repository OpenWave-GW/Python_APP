import dso_gui
import gds_info as gds
import dso_colors as color
import time

if __name__ == '__main__':
    # Initialize the GUI
    gui = dso_gui.DrawObject()
    gui.set_bg_color(gds.Theme().bg_color)

    # Create figure object
    fig = gui.Plot(x=120, y=43, width=630, height=350)
    fig.grid(x_major=12, y_major=10, line_color=gds.Theme().grid_color,bg_color=gds.Theme().bg_color, x_minor=5, y_minor=5)
    fig.set_x_axis_on(text_color=gds.Theme().text_color,line_color=gds.Theme().grid_color, fmt='%d')
    fig.set_y_axis_on(text_color=gds.Theme().text_color,line_color=gds.Theme().grid_color, fmt='%.1f')

    # Add axis labels
    gui.draw_text(400, 440, "Time(h)", gds.Theme().text_color)
    gui.draw_text(30, 300, f"Temperature({chr(176)}C)", gds.Theme().text_color, 270)

    # Add legend
    gui.draw_text(310, 15, "Sample A", gds.Theme().text_color)
    gui.draw_line(270,25,300,25, color.LTGREEN)
    gui.draw_text(460, 15, "Sample B", gds.Theme().text_color)
    gui.draw_line(420,25,450,25, color.YELLOW)

    # Draw data point for Sample A
    valx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    valy = [20.0, 23.4, 26.8, 29.5, 33.2, 37.6, 41.2, 45.7, 50.0, 56.1, 62.7, 62.5, 62.8]
    fig.plot(valx, valy, color=color.LTGREEN)

    # Draw data point for Sample B
    valy = [20.0, 26.2, 32.5, 38.3, 45.7, 52.4, 59.3, 67.8, 75.4, 75.1, 75.2, 75.6, 75.3]
    fig.plot(valx, valy, color=color.YELLOW)
    time.sleep(0.1)
