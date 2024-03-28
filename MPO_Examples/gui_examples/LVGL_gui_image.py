
import os
import sys
import dso_gui
import time

if __name__ == '__main__':
    # Initialize the GUI
    gui = dso_gui.DrawObject()
    
    # Set the current working directory to the directory where the script is located
    os.chdir(sys.path[0])
    
    # Display the PNG image on the screen
    gui.draw_png(0, 0, 'LVGL_Image.png')
    
    time.sleep(0.5)
    