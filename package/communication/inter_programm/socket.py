


from socket import *  # @UnusedWildImport
from package.ansiescape import *  # @UnusedWildImport


    
#-----------------------------------------------------
SOCKET_PYTHON_C = "\0DennTrisC_SOCKET_Python_C"
MSGSIZE_WIDTH_TO_C = 2 # 2 Byte (uint16_t)
MSGTYPE_WIDTH_TO_C = 2
ENDIANESS_SEND = 'big' # 'big' or 'little'
WIDTH_TO_C_BLOCK_IDX = 1
#-----------------------------------------------------
MSG_TYPE_PY_C_MISC = b'\x00\x00'
MSG_TYPE_PY_C_GOT_BLOCK = b'\x00\x01'
MSG_TYPE_PY_C_WANT_BLOCK = b'\x00\x02'
MSG_TYPE_PY_C_DUMMY = b'\xFF\xFE'
MSG_TYPE_PY_C_ERR = b'\xFF\xFF'
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------


    
def DennTrisC_C_Connection_Loss():
    printansi(ansi_red,"Error")
    printf(": Lost Connection to C-Program.\n")
    printf("TODO: DennTrisC_C_Connection_Loss\n")
    
    
    
def Unix_Socket_C_Python_Server():
    try:
        #NOTE: UNIX-Sockets used to connect the Python and the C Programm locally.
        #Registration in the abstract namespace (Using a "String" as Adress with preceding '\0')
        sock_C_listen = socket(AF_UNIX, SOCK_STREAM)
        sock_C_listen.bind(SOCKET_PYTHON_C)
        # Create a backlog queue for up to 1 connection.
        sock_C_listen.listen(1)    
        # Blocks until a connection arrives. A tuple (connected_socket, None) is returned
        # upon connection. Note we get the first argument and throw away the rest.
        sock_C = sock_C_listen.accept()[0]#Assign the first Connection to use it
        
        # Close it
        sock_C_listen.close()
        del sock_C_listen
        
        return sock_C
    except KeyboardInterrupt:
        pass
    
    
    
    
def msgsize_to_X_Byte(msgstr,x=MSGSIZE_WIDTH_TO_C):
    """Delivers a Byte-Object Back. It contains the length of the given String.\n Second parameter determines the Bit-Width of the returned result. Default 4 Byte if not given.\n If the String-length in Byte-Representation doesn't fit into the wanted Bit-Width the return-Value is a single Byte with '00000000' as Content (i.e. b'\x00')"""
    strlen=len(msgstr)
#     max0=255 # 2^8-1
#     max1=65535 # 2^16-1
#     max2=16777215 # 2^24-1
#     max3=4294967295 # 2^32-1
#     if strlen>max3:
#         #Error: To large
#         return -1
#     elif strlen>max2:
#         return (b'\xstrlen%max0')
#     elif strlen>max1:
#         return (b'\xstrlen%max0')
#     elif strlen>max0:
#         return (b'\xstrlen%max0')
#     else:
    try:
        return (strlen).to_bytes(x, byteorder=ENDIANESS_SEND)
    except OverflowError:
        print("ERROR: Bad Msg-Size Calculation (Size too large)")
        return b"\x00"
    
    
    
def sendCMsg(sock,msg,msgtyp):
    """Pass it a string and it sends it nicely to the C-Program. Inclusive proper msgsize, Byte-Order and this all."""
    #In Python2.x you send a String
    #But Python3 wants to work on byte-objectc. (Thank Godness ;o) )
    #So convert your Msg, say if you want to send a String, to this format
    #    e.g.: socket.send(bytes(<String>,'UTF-8'))
    #    e.g. 2: con_C.send(bytes(sendmsg,'UTF-8'))
#     if type(msg)==int:
#         sendmsg=sendmsg+bytes(msg,'UTF-8')
#     elif type(msg)==int:
#         sendmsg=sendmsg+bytes(msg,'UTF-8')
    if msgtyp==MSG_TYPE_PY_C_GOT_BLOCK:
        sendmsgsiz = WIDTH_TO_C_BLOCK_IDX.to_bytes(MSGTYPE_WIDTH_TO_C, byteorder=ENDIANESS_SEND)
        sendmsg=sendmsgsiz+msgtyp+msg.to_bytes(1, byteorder=ENDIANESS_SEND)
    elif msgtyp==MSG_TYPE_PY_C_MISC:
        sendmsgsiz=msgsize_to_X_Byte(msg)
        sendmsg=sendmsgsiz+msgtyp+bytes(msg,'UTF-8')
    #print(sendmsg)
    sock.send(sendmsg)
    
    
    
def recvCMsg(sock):
    try:
        recv_msg = sock.recv(MSGSIZE_WIDTH_TO_C)
        if not recv_msg:
            print("DennTrisC closed connection")
            return (MSG_TYPE_PY_C_ERR,"")
#         print(recv_msg)
        recvmsgsiz = 0
        recvmsgsiz=recvmsgsiz.from_bytes(recv_msg,byteorder=ENDIANESS_SEND)
        recvmsgtyp = 0
        recvmsgtyp = sock.recv(MSGTYPE_WIDTH_TO_C)
        if not recv_msg:
            print("DennTrisC closed connection")
            return (MSG_TYPE_PY_C_ERR,"")
        if recvmsgsiz==0:
            printansi(ansi_yellow, "WARNING: ")
            print("Received a Msg-Size of 0. This is most propably a Error.")
            return (MSG_TYPE_PY_C_ERR,"")
#         printf("msgsiz: "+str(recvmsgsiz)+"\n")
        recv_msg = sock.recv(recvmsgsiz)
        # When the socket is closed cleanly, recv unblocks and returns ""
        if not recv_msg:
            print("DennTrisC closed connection")
            return (MSG_TYPE_PY_C_ERR,"")
            
        returnmsg = ""
        returntype = MSG_TYPE_PY_C_ERR
        if recvmsgtyp==MSG_TYPE_PY_C_WANT_BLOCK:
            returntype = MSG_TYPE_PY_C_WANT_BLOCK
            returnmsg = 0
            returnmsg = returnmsg.from_bytes(recv_msg,byteorder=ENDIANESS_SEND)
        elif recvmsgtyp==MSG_TYPE_PY_C_MISC:#MSG_TYPE_MISC, Misceleanous Stuff, not classified. Use to send "anything"
            #recv delivers a byte-object back in Python3 (b'<Content>')
            #you could simply use it as that or decode it with
            #    unicode_string = recv_msg.decode('utf-8')
            #Than you get a String ("<Content>")
            recv_msg_unicode_string = recv_msg.decode('utf-8')
            returnmsg = recv_msg_unicode_string
            returntype = MSG_TYPE_PY_C_MISC
        elif recvmsgtyp==MSG_TYPE_PY_C_GOT_BLOCK:# MSG_TYPE_GOT_BLOCK
            "Nothing to do here. Python sends this Msg. Never gets it"
            "ERR_TYPE already set from Preamble"
        else:
            printansi(ansi_yellow, "WARNING: ")
            print("Received Msg of completely unknown Type. (Not even Misc...) Deliver back as raw Byte-Object")
            returnmsg = recv_msg
        
        return (returntype, returnmsg)
    except ConnectionResetError:
        DennTrisC_C_Connection_Loss()
    except ConnectionAbortedError:
        DennTrisC_C_Connection_Loss()
    except KeyboardInterrupt:
        pass
    except UnboundLocalError:
        pass

