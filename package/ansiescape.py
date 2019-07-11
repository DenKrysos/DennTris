from package.printf import printf



### To enable colored Terminal-Output (ansi escape)
### in Windows:
# try:
#    import colorama
#    colorama.init()
# except:
#    try:
#        import tendo.ansiterm
#    except:
#        pass




#import sys  # @UnusedImport




ansi_escape_use=0




ansi_black = "\033[22;30m"
ansi_red = "\033[22;31m"
ansi_green = "\033[22;32m"
ansi_brown = "\033[22;33m"
ansi_blue = "\033[22;34m"
ansi_magenta = "\033[22;35m"
ansi_cyan = "\033[22;36m"
ansi_gray = "\033[22;37m"
ansi_dark_gray = "\033[01;30m"
ansi_light_red = "\033[01;31m"
ansi_light_green = "\033[01;32m"
ansi_yellow = "\033[01;33m"
ansi_light_blue = "\033[01;34m"
ansi_light_magenta = "\033[01;35m"
ansi_light_cyan = "\033[01;36m"
ansi_white = "\033[01;37m"
ansi_reset = "\x1b[0m"





#For now just hardcoded and use ANSI Escape on the Output Console
#Later on maybe something like a config File Read-In with possible Values:
# on, off, auto
#and than with the auto something like the crazy Lookup-Table Stuff, that ncurses does.
def SET_ansi_escape_use():
    global ansi_escape_use
    ansi_escape_use = 1  # @UnusedVariable


#And a func for the quick programming use of changing the Console Color
def ANSICOLORSET(ANSIcolorToSet):
    global ansi_escape_use
    if(ansi_escape_use==1):
        printf(ANSIcolorToSet)

def ANSICOLORRESET():
    global ansi_escape_use
    if(ansi_escape_use==1):
        printf(ansi_reset)
        
#And to make it still shorter:
def printansi(color,string):
    ANSICOLORSET(color)
    printf(string)
    ANSICOLORRESET()