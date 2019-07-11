
import os



class DisplayDriverError(RuntimeError):
	def __init__(self, arg):
		self.args = arg



def check_running_X():
    """Checks if currently runs a X-Server (like X-11)\n It does this by checking for the DISPLAY System-Evironment Variable (aka 'env' in Terminal)\n DISPLAY gets set by a Starting X-Server"""
    #print(os.environ.get('DISPLAY'))
    if not os.environ.get('DISPLAY'):
        return False
    else:
        return True
    
    
    

def qualify_disp_for_gui():
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"
    drivers = ['directfb', 'fbcon', 'svgalib']

    found = False
    for driver in drivers:
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            testwindow = tkinter.tk()
        except tkinter.TclError:
            print("Driver: {0} failed.".format(driver))
            continue
        testwindow.destroy()
        #testwindow.quit()
        found = True
        break

    if not found:
		raise DisplayDriverError('No suitable video driver found!')
    
    
    

def start_X_Server():
    os.system("startx &")
    
    
    

def enable_GUI_capability():
    if not check_running_X():
        try:
            qualify_disp_for_gui()
        except DisplayDriverError:
            print("No working Video-Driver found. Now just start X")
            #start_X_Server()
    
    