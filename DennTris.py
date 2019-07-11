#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
DennTris -- The Software from the Demonstrator of the Research Group "Intelligente Netze"
            at the "Deutsches Forschungszentrum für künstliche Intelligenz (DFKI)" location Kaiserslautern.

DennTris further description
    (Known before: There should be interchangable production-step-stations and some
     'transport-units' carry 'to-produce-units' between them. Many Transportation-Robots together.
     Many production-stations. Robots can visit stations in arbitrary order. Robots have to
     coordinate themselves together)
    - Idea to model the industrial production line like a Tetris-Block Collector:
                >>Christoph Fischer<<
          (Christoph: Instead of do something like "Drill", "Glue", "Cut" at the stations, let the
           Products collect colored Blocks and Display them like Tetris. When a line is completed the
           Robot drives to one unique Finalization-Station and this line gets cleared)
          Nice Visualization-Concept!
    - Hardware/Software Architecture:
                >>Dennis Krummacker<<
    - On Hand Python Script:
                >>Dennis Krummacker<<
    - Software Interfaces:
                >>Dennis Krummacker<<
    - Interacting other Softwares:
                >>Dennis Krummacker<<
                
Notes:
    - GUI: Tkinter

It defines:
    - Data-Holding and -Handling of the Tetris-like Block
    - Hardware-Handling:
        - Display-Control and GUI
        - Input Control to contact with the Interface for Block-Changes (Get Blocks, Clear completed Line)
            -> RFID-Tags?
            -> Light-Sensor?
    - Interaction with another live-running C-Programm
        -> The one who controls the driving Robot

@author:     Dennis Krummacker

@copyright:  2016 DFKI, Kaiserlautern. All rights reserved.

@license:    license

@contact:    dennis.krummacker@gmail.com
@deffield    updated: 16.06.2016
'''

 


from package.ansiescape import *  # @UnusedImport @UnusedWildImport
from package.communication.inter_programm.socket import *  # @UnusedWildImport
from package.WindowManager_XServer import *  # @UnusedImport @UnusedWildImport
import sys  # @UnusedImport
from tkinter import Canvas
# import math
# import time

import RPi.GPIO as GPIO

#from timeit import Timer
#import re
#from ctypes import *
try:
    import tkinter
except ImportError:
    try:
        import Tkinter as tkinter
    except ImportError:
        pass

try:
    tkinter.tk = tkinter.Tk  # @UndefinedVariable @ReservedAssignment
except NameError:
    pass


try:
    input = raw_input  # @UndefinedVariable @ReservedAssignment
except NameError:
    pass
##Or Alternative:
# try:
#     import __builtin__
#     input = getattr(__builtin__, 'raw_input')
# except (ImportError, AttributeError):
#     pass



if sys.version_info < (3,):#Compatibility, because xrange has changed to range from Python 2.x to 3
    range = xrange  # @UndefinedVariable @ReservedAssignment
    
    



    
    
#-----------------------------------------------------
SOCKET_TR = "as"
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
    






#Some Display Stuff
#-----------------------------------------------------
#COLOR          R    G    B
WHITE       = (255, 255, 255)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
BLACK       = (  0,   0,   0)
CYAN        = (  0, 255, 255)
#Colors of the blocks
#-----------------------------------------------------
BLOCK_COLOR=(
             "#%02x%02x%02x" % (  0,   0, 255),
             "#%02x%02x%02x" % (  0, 255,   0),
             "#%02x%02x%02x" % (255,   0,   0),
             "#%02x%02x%02x" % (  0, 255, 255),
             "#%02x%02x%02x" % (255,   0, 255),
             "#%02x%02x%02x" % (255, 255,   0),
             "#%02x%02x%02x" % (255, 255, 255),
             "#%02x%02x%02x" % (  0,   0,   0)
             )
BLOCK_COLOR_MID=(
             "#%02x%02x%02x" % (  0,   0, 200),
             "#%02x%02x%02x" % (  0, 200,   0),
             "#%02x%02x%02x" % (200,   0,   0),
             "#%02x%02x%02x" % (  0, 200, 200),
             "#%02x%02x%02x" % (200,   0, 200),
             "#%02x%02x%02x" % (200, 200,   0),
             "#%02x%02x%02x" % (200, 200, 200),
             "#%02x%02x%02x" % (  0,   0,   0)
             )
BLOCK_COLOR_DARK=(
             "#%02x%02x%02x" % (  0,   0,  70),
             "#%02x%02x%02x" % (  0,  70,   0),
             "#%02x%02x%02x" % ( 70,   0,   0),
             "#%02x%02x%02x" % (  0,  70,  70),
             "#%02x%02x%02x" % ( 70,   0,  70),
             "#%02x%02x%02x" % ( 70,  70,   0),
             "#%02x%02x%02x" % ( 70,  70,  70),
             "#%02x%02x%02x" % (  0,   0,   0)
             )
#-----------------------------------------------------
SCR_WIDTH = 320
SCR_HEIGHT = 240
SCR_SIZE = (SCR_WIDTH, SCR_HEIGHT)
#-----------------------------------------------------
#The 'real' Size of the actual connected Display. Could differ from the initial intended used Display
SCR_WIDTH_ACT = 0
SCR_HEIGHT_ACT = 0
SCR_SIZE_ACT = (0, 0)
#-----------------------------------------------------
SCR_FPS = 5 #Frames Per Second (Not really important to set it high in this App...)
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------


#The Tetris Blocks
#-----------------------------------------------------
#Values of the Container, if we already own the Block
BLOCK_PRESENT = 1
BLOCK_ABSENT = 0
#-----------------------------------------------------
#'Error-Code' for return of Block-Collection-Function
BLOCK_ALREADY_IN = 1
BLOCK_INSERTED = 0
#-----------------------------------------------------
#Number of Blocks and their Measures at the Display
BLOCK_NUMBER = 4
BLOCK_WIDTH = int(SCR_WIDTH/BLOCK_NUMBER)
BLOCK_HEIGHT = BLOCK_WIDTH
BLOCK_ACTIVE_BORDER = int(BLOCK_WIDTH*0.1)
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------



#-----------------------------------------------------


#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------


DEBOUNCE_TIME = 200 # De: Schalter entprellen


    
#PIN_BLOCK0 = 29
#PIN_BLOCK1 = 31
#PIN_BLOCK2 = 33
#PIN_BLOCK3 = 35
    
PIN_BLOCK0 = 32
PIN_BLOCK1 = 36
PIN_BLOCK2 = 38
PIN_BLOCK3 = 40








class Block_Container(object):
    instance_counter = 0 # should always stay '1' during runtime
    #------------------------------------------------------------------------------------------
    def __init__(self,gui):
        self.__gui_instance = gui
        self._block0 = BLOCK_ABSENT
        self._block1 = BLOCK_ABSENT
        self._block2 = BLOCK_ABSENT
        self._block3 = BLOCK_ABSENT
        self.__block_n = 4
        Block_Container.instance_counter += 1
    #------------------------------------------------------------------------------------------
    def __del__(self):
        Block_Container.instance_counter -= 1
    #------------------------------------------------------------------------------------------
    def block_input(self,btype):
        """Block of Type btype was fetched at it's station. Pass only the Idx"""
        #If btype !present: memoize it, call Block_Display
        #If btype present: throw error
        btype="_block"+str(btype)
        if (getattr(self, btype)==BLOCK_PRESENT):
            btype = btype[1:]
            print("""ERROR: '"""+btype+"""' was already collected""")
            self.__gui_instance.print("""ERROR: '"""+btype+"""' was already collected""")
            err = BLOCK_ALREADY_IN
        else:
            setattr(self, btype, BLOCK_PRESENT)
            err = BLOCK_INSERTED
        self.update_block_display()
        return err
    #------------------------------------------------------------------------------------------
    def block_state(self):
        """Call this to display the current state"""
        #Read Memoization and return
#         print("Display ("+str(self._block0)+" "+str(self._block1)+" "+str(self._block2)+")")
        return (self._block0, self._block1, self._block2, self._block3)
#        state = ()
#        for i in range(self.__block_n)
#            l.append()
    #------------------------------------------------------------------------------------------
    def update_block_display(self):
        """"""
        state=self.block_state()
        for idx,elem in enumerate(state,start=0):
            if elem:
                self.__gui_instance.draw_present_block(self.__gui_instance._blocks_disp[idx], idx)
            else:
                self.__gui_instance.draw_absent_block(self.__gui_instance._blocks_disp[idx], idx)
        print("Current Block State: "+str(state))
        #print("##==------------------------------------------------------==##")
        del state
    #------------------------------------------------------------------------------------------
    def blocks_clear(self):
        """Gets called at the final station. Clears the lowest line, if it is filled fully"""
        state=self.block_state()
        for i in state:
            if not i:
                self.__gui_instance.print("""Can't reset! Not all Stations visited!""")
                break;
        else:
            for j in range(len(state)):
                block="_block"+str(j)
                setattr(self, block, BLOCK_ABSENT)
            self.update_block_display()
            self.__gui_instance.print("""Collected every Block. Finally cleared!""")
            del block
        del state
    #------------------------------------------------------------------------------------------
    def blocks_reset(self):
        state=self.block_state()
        for j in range(len(state)):
            block="_block"+str(j)
            setattr(self, block, BLOCK_ABSENT)
        self.update_block_display()
        self.__gui_instance.print("""Forced Memo Reset!""")
    #------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------



class GUI_DennTris(object):
    instance_counter = 0 # should always stay '1' during runtime
    #------------------------------------------------------------------------------------------
    def __init__(self):
        """The 'Main'-Layer is the .window"""
        GUI_DennTris.instance_counter += 1
        self.root = tkinter.tk()
        #self.root.resizable(width=False, height=False)
        self.root.title('DennTris')
        init_x = (self.root.winfo_screenwidth() - SCR_WIDTH) / 2
        init_y = (self.root.winfo_screenheight() - SCR_HEIGHT) / 2
        self.root.geometry('%dx%d+%d+%d' % (SCR_WIDTH, SCR_HEIGHT, init_x, init_y))
        self.root.bind_all('<Escape>', lambda event: event.widget.quit())

        global SCR_WIDTH_ACT
        global SCR_HEIGHT_ACT
        global SCR_SIZE_ACT
        SCR_WIDTH_ACT = self.root.winfo_screenwidth()
        SCR_HEIGHT_ACT = self.root.winfo_screenheight()
        SCR_SIZE_ACT = (SCR_WIDTH_ACT, SCR_HEIGHT_ACT)
        print(SCR_SIZE_ACT)

        self.__init_full_screen_capability()

        self.window_back = tkinter.Canvas(self.root, width=SCR_WIDTH_ACT, height=SCR_HEIGHT_ACT, background='black',highlightthickness=0)
        self.window_back.place(in_=self.root, relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        self.window = tkinter.Canvas(self.window_back, width=SCR_WIDTH, height=SCR_HEIGHT, background='black',highlightthickness=0)
        #self.window.pack()
        self.window.place(in_=self.window_back, relx=0.5,rely=0.5,anchor=tkinter.CENTER)
        
        self.__block0_disp=Canvas(self.window,width=BLOCK_WIDTH,height=BLOCK_HEIGHT,highlightthickness=0)
        self.__block0_disp.place(x=0, y=0)
        self.__block1_disp=Canvas(self.window,width=BLOCK_WIDTH,height=BLOCK_HEIGHT,highlightthickness=0)
        self.__block1_disp.place(in_=self.__block0_disp, relx=1, y=0, bordermode="outside")
        self.__block2_disp=Canvas(self.window,width=BLOCK_WIDTH,height=BLOCK_HEIGHT,highlightthickness=0)
        self.__block2_disp.place(in_=self.__block1_disp, relx=1, y=0, bordermode="outside")
        self.__block3_disp=Canvas(self.window,width=BLOCK_WIDTH,height=BLOCK_HEIGHT,highlightthickness=0)
        self.__block3_disp.place(in_=self.__block2_disp, relx=1, y=0, bordermode="outside")
        self._blocks_disp = (self.__block0_disp, self.__block1_disp, self.__block2_disp, self.__block3_disp)
        
        for idx,block_obj in enumerate(self._blocks_disp,start=0):
            self.draw_absent_block(block_obj,idx)
#         self.update_block_display()
        
        self.quitbutton = tkinter.Button(self.window,text="QUIT", fg="red",command=self.root.quit)
        self.quitbutton.place(in_=self.__block3_disp, relx=0.5, rely=1, y=10, bordermode="outside",anchor=tkinter.N, width=0.75*BLOCK_WIDTH, height=0.75*BLOCK_HEIGHT)
        
        '''
        self.t_btn_1_state = 0
        toggle1button = tkinter.Button(self.window,text="Toggle1", bg='gray', fg="green", relief="raised", command=lambda:self.toggle_block_and_button(self.__block1_disp,1))
        toggle1button.place(in_=self.__block1_disp, relx=0.5, rely=1, y=10, bordermode="outside",anchor=tkinter.N, width=0.75*BLOCK_WIDTH, height=0.75*BLOCK_HEIGHT)
        '''
        
        
        self.console_frame_without_border = tkinter.Frame(self.window,width=SCR_WIDTH,height=int(0.3*SCR_HEIGHT)+3,bg='black')
        self.console_frame_without_border.place(x=0,y=int(0.7*SCR_HEIGHT)-3)
        self.console_frame_border=Canvas(self.console_frame_without_border,highlightthickness=0,width=SCR_WIDTH,height=3,bg='gray')
        self.console_frame_border.place(in_=self.console_frame_without_border)
#         self.temp.create_line(0,0,SCR_WIDTH,0,fill='red',width=3)
        self.console_frame = tkinter.Frame(self.console_frame_without_border,width=SCR_WIDTH,height=int(0.3*SCR_HEIGHT),bg='black')
        self.console_frame.place(in_=self.console_frame_without_border,y=3)

        self.console_output = tkinter.Text(self.console_frame,bg='black',fg='white',font=("Times", 11),highlightthickness=0,highlightbackground='black',pady=0,padx=0)
        self.console_output_scrollbar = tkinter.Scrollbar(self.console_frame,orient="vertical",command=self.console_output.yview)
        self.root.update()
        self.console_output_scrollbar.place(in_=self.console_frame,height=self.console_frame.winfo_height(),anchor=tkinter.NE,relx=1)
        self.console_output.config(yscrollcommand=self.console_output_scrollbar.set)
        self.root.update()
        self.console_output.place(in_=self.console_frame, height=int(0.3*SCR_HEIGHT),width=(SCR_WIDTH-self.console_output_scrollbar.winfo_width()))
        self.console_output.configure(state=tkinter.DISABLED)
#         self.console_output_scrollbar.configure(command=self.console_output.yview)
        self.console_output.see("end")
        
        # make sure the widget gets focus when clicked
        # on, to enable highlighting and copying to the
        # clipboard.
        self.console_output.bind("<1>", lambda event: self.console_output.focus_set())
        
#         self.root.update()
#         print("console_frame: "+
#                    str(self.console_frame.winfo_width())+" "+
#                    str(self.console_frame.winfo_height()))
#         print("console_output: "+
#                    str(self.console_output.winfo_width())+" "+
#                    str(self.console_output.winfo_height()))
    #------------------------------------------------------------------------------------------
    def __init_full_screen_capability(self):
        #self.root.attributes('-zoomed', True)
        self.fscr_state = True
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.leave_fullscreen)
        self.root.attributes("-fullscreen", self.fscr_state)
    #------------------------------------------------------------------------------------------
    def toggle_fullscreen(self, event=None):
        self.fscr_state = not self.fscr_state
        self.root.attributes("-fullscreen", self.fscr_state)
        return "break"
    #------------------------------------------------------------------------------------------
    def leave_fullscreen(self, event=None):
        self.fscr_state = False
        self.root.attributes("-fullscreen", False)
        return "break"
    #------------------------------------------------------------------------------------------
    def __del__(self):
        GUI_DennTris.instance_counter -= 1
    #------------------------------------------------------------------------------------------
    def __gui_loop__(self):
        self.root.mainloop()
    #------------------------------------------------------------------------------------------
    def print(self,s):
        self.console_output.configure(state=tkinter.NORMAL)
        self.console_output.insert(tkinter.END, s+"\n")
        self.console_output.configure(state=tkinter.DISABLED)
        self.console_output.see("end")
    #------------------------------------------------------------------------------------------
    def draw_present_block(self,canvas,color):
        """"""
        canvas.delete("all")
        canvas.create_rectangle(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, fill=BLOCK_COLOR_DARK[color])
        canvas.create_line(0, 0, 5+BLOCK_ACTIVE_BORDER, 5+BLOCK_ACTIVE_BORDER, fill=BLOCK_COLOR_MID[color], width=3)
        canvas.create_line(BLOCK_WIDTH, 0, BLOCK_WIDTH-5-BLOCK_ACTIVE_BORDER, 5+BLOCK_ACTIVE_BORDER, fill=BLOCK_COLOR_MID[color], width=3)
        canvas.create_line(0, BLOCK_HEIGHT, 5+BLOCK_ACTIVE_BORDER, BLOCK_HEIGHT-5-BLOCK_ACTIVE_BORDER, fill=BLOCK_COLOR_MID[color], width=3)
        canvas.create_line(BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_WIDTH-5-BLOCK_ACTIVE_BORDER, BLOCK_HEIGHT-5-BLOCK_ACTIVE_BORDER, fill=BLOCK_COLOR_MID[color], width=3)
        canvas.create_rectangle(0+BLOCK_ACTIVE_BORDER, 0+BLOCK_ACTIVE_BORDER, BLOCK_WIDTH-BLOCK_ACTIVE_BORDER, BLOCK_HEIGHT-BLOCK_ACTIVE_BORDER, fill=BLOCK_COLOR[color])
    #------------------------------------------------------------------------------------------
    def draw_absent_block(self,canvas,color):
        """"""
        canvas.delete("all")
        canvas.create_rectangle(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, fill=BLOCK_COLOR_DARK[color])
    #------------------------------------------------------------------------------------------
    '''
    def toggle_block_and_button(self,canvas,color):
        self.print("Block_1 just optically toggled")
        if self.t_btn_1_state == 0:
            self.draw_absent_block(canvas,color)
        else:
            self.draw_present_block(canvas,color)
        self.t_btn_1_state = not self.t_btn_1_state
    '''
    #------------------------------------------------------------------------------------------
    def update_block_display(self):
        """"""
        state=self.__block_container.block_state()
        for idx,elem in enumerate(state,start=0):
            if elem:
                self.__gui_instance.draw_present_block(self.__gui_instance._blocks_disp[idx], idx)
            else:
                self.__gui_instance.draw_absent_block(self.__gui_instance._blocks_disp[idx], idx)
        del state
    #------------------------------------------------------------------------------------------
    def config(self,attr,val):
        """Use this to 'connect' the Block_Container or it won't work.\n Use it after both 'Block_Container' and 'GUI' are instanced"""
        if attr == "__block_container":
            self.__block_container=val
        
            self.clearallbutton = tkinter.Button(self.window,text="Clear\nall", fg="red",relief="sunken", command=lambda:self.__block_container.blocks_clear())
            self.clearallbutton.place(in_=self.__block0_disp, relx=0.5, rely=1, y=10, bordermode="outside",anchor=tkinter.N, width=0.75*BLOCK_WIDTH, height=0.75*BLOCK_HEIGHT)
            
            self.button_input0 = tkinter.Button(self.window,text="Catch\n0", fg="blue",relief="raised", command=lambda:self.__block_container.block_input(0))
            self.button_input0.place(in_=self.__block2_disp, relx=0, rely=1, y=7, bordermode="outside",anchor=tkinter.NW, width=0.5*BLOCK_WIDTH, height=0.45*BLOCK_HEIGHT)
            
            self.button_input1 = tkinter.Button(self.window,text="Catch\n1", fg="blue",relief="raised", command=lambda:self.__block_container.block_input(1))
            self.button_input1.place(in_=self.button_input0, relx=1, rely=0, y=0, bordermode="outside",anchor=tkinter.NW, width=0.5*BLOCK_WIDTH, height=0.45*BLOCK_HEIGHT)
            
            self.button_input2 = tkinter.Button(self.window,text="Catch\n2", fg="blue",relief="raised", command=lambda:self.__block_container.block_input(2))
            self.button_input2.place(in_=self.button_input0, relx=0, rely=1, y=0, bordermode="outside",anchor=tkinter.NW, width=0.5*BLOCK_WIDTH, height=0.45*BLOCK_HEIGHT)
            
            self.button_input3 = tkinter.Button(self.window,text="Catch\n3", fg="blue",relief="raised", command=lambda:self.__block_container.block_input(3))
            self.button_input3.place(in_=self.button_input0, relx=1, rely=1, y=0, bordermode="outside",anchor=tkinter.NW, width=0.5*BLOCK_WIDTH, height=0.45*BLOCK_HEIGHT)

            self.button_forcereset = tkinter.Button(self.window,text="Force\nReset", bg='white', fg="green", relief="raised", command=lambda:self.__block_container.blocks_reset())
            self.button_forcereset.place(in_=self.__block1_disp, relx=0.5, rely=1, y=10, bordermode="outside",anchor=tkinter.N, width=0.75*BLOCK_WIDTH, height=0.75*BLOCK_HEIGHT)
    #------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------

    
# def toggle_block_and_button(canvas,color):
#     print("a")
#     if toggle1button.config('relief')[-1] == 'sunken':
#         print("b")
#         draw_absent_block(canvas,color)
#         toggle1button.config(relief="raised")
#     else:
#         print("c")
#         draw_present_block(canvas,color)
#         toggle1button.config(relief="sunken")

    
    
def callback_collect_block0(channel):
    global got_blocks
    got_blocks.block_input(0)
    
def callback_collect_block1(channel):
    global got_blocks
    got_blocks.block_input(1)
    
def callback_collect_block2(channel):
    global got_blocks
    got_blocks.block_input(2)
    
def callback_collect_block3(channel):
    global got_blocks
    got_blocks.block_input(3)
    
    
    
    
def DennTris_Main():
    err=0  # @UnusedVariable
    global got_blocks
#     global window
    global gui
    
    #GPIO-Settings:
    ## RPi.GPIO Layout
    GPIO.setmode(GPIO.BOARD) # Pin Numbers
    #GPIO.setmode(GPIO.BCM) # Broadcom GPIO Numbers
    
    ##Output-Pins
#    GPIO.setup( 7, GPIO.OUT)
#    GPIO.setup(11, GPIO.OUT)
#    GPIO.setup(13, GPIO.OUT)
#    GPIO.setup(15, GPIO.OUT)
    
    ##Input-Pins
    GPIO.setup(PIN_BLOCK0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BLOCK1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BLOCK2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BLOCK3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(PIN_BLOCK0, GPIO.RISING, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_callback(PIN_BLOCK0, callback=callback_collect_block0)
    GPIO.add_event_detect(PIN_BLOCK1, GPIO.RISING, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_callback(PIN_BLOCK1, callback=callback_collect_block1)
    GPIO.add_event_detect(PIN_BLOCK2, GPIO.RISING, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_callback(PIN_BLOCK2, callback=callback_collect_block2)
    GPIO.add_event_detect(PIN_BLOCK3, GPIO.RISING, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_callback(PIN_BLOCK3, callback=callback_collect_block3)
    
    
    '''
    sock_C=Unix_Socket_C_Python_Server()
    
    
    
    send_msg=2
    sendCMsg(sock_C,send_msg,MSG_TYPE_PY_C_GOT_BLOCK)
        
    recv_msg_type,recv_msg = recvCMsg(sock_C)
    print(recv_msg_type)
    print(str(recv_msg))
    '''

    
    
    #Display/GUI (Tkinter):
    gui = GUI_DennTris()
    #Block_Container Instance
    got_blocks = Block_Container(gui)
    #Connect the Block_Container also with the GUI (Button-Functionality)
    gui.config("__block_container", got_blocks)
    
#     running=1
    try:
#         while running:
            gui.__gui_loop__()
#             keyboard_input = input("Type 'exit' to quit: ")
#             if keyboard_input == "exit":
#                 running=0
#                 break
    except KeyboardInterrupt:
        sock_C.close()
        GPIO.cleanup() # clean up GPIO on CTRL+C exit
        
    sock_C.close()
    GPIO.cleanup() # clean up GPIO on normal exit
    
    
    
def main(argv):
    print('Number of arguments:', len(argv), 'arguments.')
    print('Argument List:', str(argv))
    SET_ansi_escape_use()
    enable_GUI_capability()
    DennTris_Main()
    
    
if __name__ == '__main__': main(sys.argv[1:])
