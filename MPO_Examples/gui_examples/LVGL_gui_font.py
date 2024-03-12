
import dso_gui
import dso_colors as color
import time

if __name__ == '__main__':
    # Initialize the GUI
    gui = dso_gui.DrawObject()
    gui.set_bg_color(color.BLACK)
    
    # Set different font sizes using built-in fonts
    for i in range(12, 37, 4):
        font = gui.set_font(i)
        if font:
            label = gui.draw_text(150, 100+(i/4-3)*40, 'Hello', color=color.WHITE, font=font)

    # Set font for specific languages using Terminus font
    font = gui.set_font(fnt_path='/home/upypr/lv_font/Terminus_24.fnt')
    if font:
        label = gui.draw_text(550, 100, 'Cześć', color=color.WHITE, font=font)
        label = gui.draw_text(550, 140, 'Bonjour', color=color.WHITE, font=font)
        label = gui.draw_text(550, 180, 'Hola', color=color.WHITE, font=font)
        
    # Set bold font for specific languages using Terminus-Bold font
    font = gui.set_font(fnt_path='/home/upypr/lv_font/TerminusB_24.fnt')
    if font:
        label = gui.draw_text(550, 220, 'Привет', color=color.WHITE, font=font)
        label = gui.draw_text(550, 260, 'Hallo', color=color.WHITE, font=font)
        label = gui.draw_text(550, 300, 'Olá', color=color.WHITE, font=font)
        label = gui.draw_text(550, 340, 'Ciao', color=color.WHITE, font=font)

    time.sleep(0.5)
