# Import the required libraries
import win32gui
import win32com.client
import keyboard
import threading
import psutil
import screeninfo

from tkinter import Tk, Button
from pystray import MenuItem as item
from pystray import Icon
from PIL import Image


TABBER_WINDOW_WIDTH = 900
TABBER_WINDOW_HEIGHT = 300


# if this bool turns to True, all tabber windows close
# workaround as thread.kill() is not implemented in python
# instead every thread will poll this boolean
closed = False

class TabberManager():

    def __init__(self):

        # ALT Q was pressed
        print("New TabberManager Instance created")

        # get list of running programs:
        def callback(hwnd, win_list):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)

                if "pytabber" in window_title: #ignore pytabber window itself
                    return True

                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                if window_title and right-left and bottom-top: #if window has coordinates its open (also works if minimized)
                    win_list[window_title] = hwnd

            return True

        win_list = dict() # dict of window name to process handler id
        win32gui.EnumWindows(callback, win_list)  # populate list 
        print("Collected Running Programs")
        print(win_list)

        global closed
        closed = False

        self.tabberWindows = list()

        for m in screeninfo.get_monitors():
            print(str(m))

            screen_width = m.width
            screen_height = m.height

            monitor_offset_width = m.x
            monitor_offset_height = m.y

            x = ((screen_width/2)+monitor_offset_width) - (TABBER_WINDOW_WIDTH/2)
            y = ((screen_height/2)+monitor_offset_height) - (TABBER_WINDOW_HEIGHT/2)

            t = threading.Thread(target=self.spawn_tabber_window, args=(x,y, win_list))

            self.tabberWindows.append(t)
        
        for tw in self.tabberWindows:
            tw.start()

    def destroy_all_tabber_windows(self):
        global closed
        closed = True

    def spawn_tabber_window(self, x, y, win_list):
        global closed

        # spawn window:
        win = Tk()
        win.title("Pytabber Selection")
        win.attributes("-topmost", True)
        win.attributes('-alpha', 0.8)
        win.configure(bg='white')
        win.geometry('%dx%d+%d+%d' % (TABBER_WINDOW_WIDTH, TABBER_WINDOW_HEIGHT, x, y))
        win.protocol('WM_DELETE_WINDOW', self.destroy_all_tabber_windows)
        def check_if_closed():
            global closed
            if closed:
                win.destroy()
            win.after(0, check_if_closed)  # reschedule
        win.after(2000, check_if_closed)
        
        for window_name, handler in win_list.items():
            b = Button(master=win, text= window_name, command=lambda handler_id=handler: self.bring_to_front(handler_id))
            b.pack()
        
        win.mainloop()

    def bring_to_front(self, handler_id):
        global closed
        # need to send alt key first for some reason
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # now set foregroundwindow:
        print("Setting to Foreground:", handler_id)
        win32gui.SetForegroundWindow(int(handler_id))
        closed = True

class TrayIcon(Tk):

    # Define a function for quit the selfdow
    def quit_window(self, icon, item):
        icon.stop()
        self.destroy()


    # Define a function to show the window again
    def show_window(self, icon, item):
        if icon:
            icon.stop()
        self.after(0,self.deiconify())


    # Hide the window and show on the system taskbar
    def hide_window(self):
        self.withdraw()
        image=Image.open("./tab-key.ico")
        menu=(item('Quit', self.quit_window), item('Settings', self.show_window))
        icon=Icon("Pytabber", image, "Pytabber", menu)
        icon.run()


    def __init__(self):
        super().__init__()

        self.geometry('500x200')

        # make only close button appear in top:
        self.attributes('-toolwindow', True)
        self.title("pyTabber Settings")

        # change what happens on close
        self.protocol('WM_DELETE_WINDOW', self.hide_window)

        # create listeners for q press:
        keyboard.on_press_key("q", self.on_q_press)
        keyboard.on_release_key("alt", self.on_alt_release)

        # start as tray icon
        self.after(0, self.hide_window)


    def on_q_press(self, event):
        print("pressed q")
        if not keyboard.is_pressed('alt'):
            print("not holding alt") 
            return

        TabberManager()
        # self.after(1, self.deiconify)
        #self.tabberwindow = Toplevel(self)
        #self.tabberwindow.title("Child Window")


    def on_alt_release(self, event):
        # hide window
        print("Released ALT")



if __name__ == "__main__":
    
    for p in psutil.process_iter():
        if "pytabber" in p.name().lower():
            quit() # process already running

    print([p.name().lower() for p in psutil.process_iter()])

    app = TrayIcon()
    app.mainloop()
