
import dso_gui
import dso_colors as color
import time

if __name__ == '__main__':
    # Initialize the GUI
    gui = dso_gui.DrawObject()
    gui.set_bg_color(color.BLACK)

    # Draw four "Hello World" labels with different colors and angles
    font = gui.set_font(28)
    label1 = gui.draw_text(400, 220, "Hello World", color.LTCYAN, font=font)
    label2 = gui.draw_text(400, 220, "Hello World", color.LTRED, 90, font=font)
    label3 = gui.draw_text(400, 220, "Hello World", color.YELLOW, 180, font=font)
    label4 = gui.draw_text(400, 220, "Hello World", color.LTGREEN, 270, font=font)
    
    time.sleep(0.5)