# Name: dso_basic.py
#
# Description: 
#
# Author: GW Instek
#
# Documentation:
# https://github.com/OpenWave-GW/Python_APP
#
# License: GW Python APP License
# Copyright (c) 2023 GOOD WILL INSTRUMENT CO., LTD.
# https://github.com/OpenWave-GW/Python_APP/blob/main/LICENSE.txt

import socket
import sys
import gc
import struct
import os
import time
try:
    import dso_colors as color
except:
    pass

class DsoBasic():
    def __init__(self):
        self.key_flag = False
        self.key_cnt = ''
        self.key_code = ''
        self.__ModelName = ''
        self.__Chnum = 0
        if sys.implementation.name == "micropython":
            self.__micropython = True
        else:
            self.__micropython = False
        
    def write(self, cmd:str):
        """SCPI command write

        Args:
            cmd (str): SCPI command

        .. note::
            You can write "RUN" SCPI command, set DSO to RUN by yourself. Try use:
            
            .write('RUN')

            You can write "STOP" SCPI command, set DSO to STOP by yourself. Try use:

            .write('STOP')

        """
        if cmd[-1] == '\n':
            pass
        else:
            cmd += '\n'
        if self.__micropython:
            self.s.write(cmd)
        else:
            self.s.sendall(cmd.encode())
    
    def __fill_Model(self):
        data = self.idn()
        self.__ModelName = data.split(',')[1]
        for i in reversed(range(0,len(self.__ModelName))):
            try:
                self.__Chnum = int(self.__ModelName[i])
                break
            except:
                pass

    def connect(self, host:str='localhost',port:int=32767):
        """

        Args:
            port (int, optional): port number. Defaults to 32767 is internal connection.

        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s.settimeout(5.0)
        addr = socket.getaddrinfo(host,port)[0][-1]
        try:
            self.s.connect(addr)
        except:
            return -1
        try:
            self.dsodraw.__set_py_flag("ON")
            #__ShmThread()
        except:
            pass
        self.__fill_Model()
        return 0
    
    def close(self):
        """
        close connection
        """
        try:
            self.dsodraw.__set_py_flag("OFF")
        except:
            pass
        self.s.close()
    
    def readline(self) -> str:
        """

        Returns:
            str: return string
        """
        if self.__micropython:
            str=self.s.readline().decode()
        else:
            tmp=b''
            while True:
                try:
                    tmp += self.s.recv(1)
                    if tmp.endswith(b'\n'):
                        break
                except:
                    break
            str=tmp.decode()
        if(str == ''):
            return ''
        elif(str[-1] == '\n'):
            return str[:-1]
        else:
            return str

    def query(self, cmd:str) -> str:
        """SCPI command query

        Args:
            cmd (str): SCPI command

        Returns:
            str: SCPI return

        .. note::
            You can query "*IDN?" SCPI command, to query return value by yourself. Try use:
            
            .query('*IDN?')
        """
        if cmd[-1] == '\n':
            pass
        else:
            cmd += '\n'
        self.write(cmd)
        return self.readline()

    def __read_block(self):
        info = self.s.recv(1)
        if (info == b'#'):
            head = self.s.recv(1)
            head_d = int(head.decode('utf-8'))
            length = self.s.recv(head_d).decode('utf-8')
            length = int(length) + 1
            cnt = 0
            data = b''
            while (1):
                data += self.s.recv(8192)
                cnt = len(data)
                # print("%d/%d"%(cnt,length))
                if (cnt == length):
                    break
        else:
            data = None
        return data

    def __read_block_waveform(self):
        data = self.__read_block()
        data_out_size = int((len(data) - 1) / 2)
        data_out=list(struct.unpack(f'>{data_out_size}h', data[0:-1]))
        del data
        return data_out

    def get_waveform_num(self, ch:int, real_value:bool=True, pos_consider:bool=True) -> list:
        """This function can get waveform data as numbertic array

        Args:
            ch (int): channel
            real_value (bool, optional): True will return real world value or it will return dso value. Defaults to True.
            pos_consider (bool, optional): The DSO value consider position or not. Defaults to True.

        Returns:
            list: waveform data
        """
        if self.is_ch_support(ch):
            pass
        else:
            return None
        # check header
        cmd = ":header?"
        header = self.query(cmd + "\n")
        # print(header)
        if ('ON' in header):
            pass
        else:
            cmd = ":header ON"
            self.write(cmd + "\n")
        info = {}
        # --------
        cmd = ":acq%d:mem?" % (ch)
        self.write(cmd + "\n")
        if (cmd[-1] == '?'):
            header_buffer = b''
            while True:
                info_b = self.s.recv(1)
                header_buffer += info_b
                if (info_b == b'\n'):
                    # Parsing header_buffer
                    header_buffer = header_buffer.decode('utf-8').split(';')
                    for i in range(len(header_buffer)):
                        tmp = header_buffer[i].split(',')
                        try:
                            info.update({tmp[0]:tmp[1]})
                        except:
                            pass
                    # print(databit)
                    # read block data waveform
                    data_out = self.__read_block_waveform()
                    break
        else:
            self.query('SYST:ERR?\n')
            return None
        try:
            databit=int(info['Data Bit'])
        except:
            databit=8
        vscale = float(info['Vertical Scale'])
        vpos = float(info['Vertical Position'])
        wave_len = int(info['Memory Length'])
        if real_value:
            tmp_s = vscale/25
            for i in range(wave_len):
                data_out[i] = data_out[i]*tmp_s
        else:
            if pos_consider:
                shift = vpos/vscale*25
                for i in range(wave_len):
                    data_out[i]+=int(shift)
            else:
                pass
        gc.collect()
        return data_out

    def autoset(self):
        """Set DSO Autoset
        """
        cmd='AUTOS\n'
        self.write(cmd)

    def stop(self):
        """Set DSO STOP
        """
        cmd=':STOP\n'
        self.write(cmd)

    def run(self):
        """Set DSO RUN
        """
        cmd=':RUN\n'
        self.write(cmd)
    
    def is_run(self) -> bool:
        """Check now DSO status

        Returns:
            bool: 
        """
        cmd=':RUN?\n'
        ret = self.query(cmd)
        if(int(ret)):
            return True
        else:
            return False 
    
    def single(self):
        """Set SINGLE
        """
        cmd=':SINGle\n'
        self.write(cmd)

    def default(self):
        """Set DSO Default
        """
        cmd='*RST\n'
        self.write(cmd)

    def force(self):
        """Forces an acquisition.
        """
        cmd=':FORCe'
        self.write(cmd)

    def idn(self) -> str:
        """Get *IDN

        Returns:
            str: *IDN string
        """
        cmd='*IDN?\n'
        self.write(cmd)
        return self.readline()

    def opc(self) -> str:
        """

        Returns:
            str: 
        """
        cmd='*OPC?\n'
        self.write(cmd)
        return self.readline()

    def is_ch_support(self, ch:int) -> bool:
        """Check the channel is valid or not.

        Args:
            ch (int): channel number

        Returns:
            bool: True or False
        """
        if ch <= 0:
            return False
        elif ch > self.__Chnum:
            return False
        else:
            return True
    
    def get_samplerate(self) -> float:
        """Get samplerate

        Returns:
            float: samplerate
        """
        cmd=':ACQuire:SAMPlerate?\n'
        ret = self.query(cmd)
        return float(ret)

    def load_waveform_csv(self, file:str, real_value:bool=True, checklen:bool=True, pos_consider:bool=True) -> tuple[dict, list]:
        """You can read dso waveform csv file.

        Args:
            file (str): Waveform file full path.
            real_value (bool, optional): True will return real world value or it will return dso value. Defaults to True.
            checklen (bool, optional): False will ignore waveform length check. Defaults to True.
            pos_consider (bool, optional): The DSO value consider position or not. Defaults to True.

        Returns:
            tuple[dict, list]: The waveform header info and value.

            .. note:: For single channel file :
            
                - They both 1-D.

                For all channel file :
                
                - They both Multi-D.

                    First channel's will be info[0] and waveform[0].

                    Second channel's will be info[1] and waveform[1]. and so on.


        """
        gc.collect()
        if checklen:
            return self.__load_waveform_csv(file, real_value, pos_consider)
        
        with open(file,'r') as f:
            data=f.read().splitlines()
        i=0
        info={}
        all_channels = 1
        # Update header info
        # 1. Update format
        tmp=data[i].strip(',').split(',')
        info.update({tmp[0]:tmp[1]})
        i+=1
        # 2. Update header
        tmp=data[i].strip(',').split(',')
        if len(tmp) > 2:
            # CSV file include more than one channel.
            all_channels = len(tmp)//2
            for idx in range(all_channels):
                info[idx] = {}
                info[idx].update({tmp[2*idx]:tmp[2*idx+1]}) 
            while True:
                tmp = data[i].strip(',').split(',')
                i+=1
                for idx in range(all_channels):
                    try:
                        info[idx].update({tmp[2*idx]:tmp[2*idx+1]}) 
                        read_end = False
                    except:
                        read_end = True
                        break
                if read_end:
                    break
        else:
            # CSV file is one channel.
            info.update({tmp[0]:tmp[1]})
            i+=1
            while True:
                tmp=data[i].strip(',').split(',')
                i+=1
                try:
                    info.update({tmp[0]:tmp[1]})
                except:
                    break
        # Get waveform info
        if all_channels == 1:
            the_info = info
        else:
            the_info = info[0]
        try:
            databit=int(the_info['Data Bit'])
        except:
            databit=8
        wave_len = int(the_info['Memory Length'])
        if the_info['Mode'] == 'Detail':
            detail=True
        else:
            detail=False

        _idx=len(the_info)+1
        for i in range(_idx):
            del data[0]
        # Get waveform data
        if all_channels == 1:
            vscale = float(info['Vertical Scale'])
            vpos = float(info['Vertical Position'])
            waveform = [0]*wave_len
            if detail:
                for i in range(wave_len):
                    waveform[i] = float(data[i].strip(',').split(',')[1])
                if real_value:
                    pass
                else:
                    for i in range(wave_len):
                        waveform[i] = int((waveform[i] - vpos)/vscale*25)
            else:
                for i in range(wave_len):
                    waveform[i]=int(data[i].strip(','))
                if real_value:
                    for i in range(wave_len):
                        waveform[i] = waveform[i]*vscale/25
                else:
                    if pos_consider:
                        tmp_s = int(vpos/vscale*25)
                        for i in range(wave_len):
                            waveform[i] += tmp_s

        else:
            waveform = [[0]*wave_len for _ in range(all_channels)]
            if detail:
                for i in range(wave_len):
                    tmp2 = data[i].strip(',').split(',')
                    for idx in range(all_channels):
                        waveform[idx][i] = float(tmp2[2*idx+1])
                if real_value:
                    pass
                else:
                    for idx in range(all_channels):
                        vscale = float(info[idx]['Vertical Scale'])
                        vpos = float(info[idx]['Vertical Position'])
                        for i in range(wave_len):
                            waveform[idx][i] = int((waveform[idx][i] - vpos)/vscale*25)
            else:
                for i in range(wave_len):
                    tmp2 = data[i].strip(',').split(',')
                    for idx in range(all_channels):
                        waveform[idx][i]=int(tmp2[2*idx])
                if real_value:
                    for idx in range(all_channels):
                        vscale = float(info[idx]['Vertical Scale'])
                        vpos = float(info[idx]['Vertical Position'])
                        for i in range(wave_len):
                            waveform[idx][i] = waveform[idx][i]*vscale/25
                else:
                    if pos_consider:
                        for idx in range(all_channels):
                            vscale = float(info[idx]['Vertical Scale'])
                            vpos = float(info[idx]['Vertical Position'])
                            tmp_s = int(vpos/vscale*25)
                            for i in range(wave_len):
                                waveform[idx][i] += tmp_s

        del data
        gc.collect()
        return info,waveform

    def __load_waveform_csv(self, file:str, real_value:bool=True, pos_consider:bool=True) -> tuple[dict, list]:
        info={}
        all_channels = 1
        f=open(file,'r')
        # Read Header info
        # 1. Update format
        tmp = f.readline().rstrip().strip(',').split(',')
        info.update({tmp[0]:tmp[1]})
        # 2. Update header
        tmp = f.readline().rstrip().strip(',').split(',')
        if len(tmp) > 2:
            # CSV file include more than one channel.
            all_channels = len(tmp)//2
            for idx in range(all_channels):
                info[idx] = {}
                info[idx].update({tmp[2*idx]:tmp[2*idx+1]}) 
            while True:
                tmp = f.readline().rstrip().strip(',').split(',')
                for idx in range(all_channels):
                    try:
                        info[idx].update({tmp[2*idx]:tmp[2*idx+1]}) 
                        read_end = False
                    except:
                        read_end = True
                        break
                if read_end:
                    break
        else:
            # CSV file is one channel.
            info.update({tmp[0]:tmp[1]})
            while True:
                tmp = f.readline().rstrip().strip(',').split(',')
                try:
                    info.update({tmp[0]:tmp[1]})
                except:
                    break
        # Get waveform info
        if all_channels == 1:
            the_info = info
        else:
            the_info = info[0]
        try:
            databit=int(the_info['Data Bit'])
        except:
            databit=8
        wave_len = int(the_info['Memory Length'])
        if the_info['Mode'] == 'Detail':
            detail=True
        else:
            detail=False

        if wave_len > 10e4:
            f.close()
            raise ValueError('Waveform length too large!')

        # Get waveform data
        if all_channels == 1:
            vscale = float(info['Vertical Scale'])
            vpos = float(info['Vertical Position'])
            waveform = [0]*wave_len
            if detail:
                tmp = f.read().splitlines()
                for i in range(wave_len):
                    waveform[i] = float(tmp[i].strip(',').split(',')[1])
                if real_value:
                    pass
                else:
                    for i in range(wave_len):
                        waveform[i] = int((waveform[i] - vpos)/vscale*25)
            else:
                tmp = f.read().splitlines()
                for i in range(wave_len):
                    waveform[i]=int(tmp[i].strip(','))
                if real_value:
                    for i in range(wave_len):
                        waveform[i] = waveform[i]*vscale/25+vpos
                else:
                    if pos_consider:
                        tmp_s = int(vpos/vscale*25)
                        for i in range(wave_len):
                            waveform[i] += tmp_s
        else:
            waveform = [[0]*wave_len for _ in range(all_channels)]
            if detail:
                tmp = f.read().splitlines()
                for i in range(wave_len):
                    tmp2 = tmp[i].strip(',').split(',')
                    for idx in range(all_channels):
                        waveform[idx][i]=int(tmp2[2*idx+1])
                if real_value:
                    pass
                else:
                    for idx in range(all_channels):
                        vscale = float(info[idx]['Vertical Scale'])
                        vpos = float(info[idx]['Vertical Position'])
                        for i in range(wave_len):
                            waveform[idx][i] = int((waveform[idx][i] - vpos)/vscale*25)
            else:
                tmp = f.read().splitlines()
                for i in range(wave_len):
                    tmp2 = tmp[i].strip(',').split(',')
                    for idx in range(all_channels):
                        waveform[idx][i]=int(tmp2[2*idx])
                if real_value:
                    for idx in range(all_channels):
                        vscale = float(info[idx]['Vertical Scale'])
                        for i in range(wave_len):
                            waveform[idx][i] = waveform[idx][i]*vscale/25
                else:
                    if pos_consider:
                        for idx in range(all_channels):
                            vscale = float(info[idx]['Vertical Scale'])
                            vpos = float(info[idx]['Vertical Position'])
                            tmp_s = int(vpos/vscale*25)
                            for i in range(wave_len):
                                waveform[idx][i] += tmp_s
        f.close()
        del tmp
        gc.collect()
        return info, waveform
    
    def __shm_thread(self, popup_delay=0.5):
        import _thread
        _thread.start_new_thread(self.__popup_shm, ("Thread1",popup_delay))

    def __popup_shm(self, thread_name, delay):
        import array
        import dso_gui as gui
        
        shm_name = "/dev/shm/upy/shm_popup"
        cp_shm_name =  "/dev/shm/upy/copy_shm_popup"
        shm_size = 1024
        
        while True:
            try:
                fd = os.stat(shm_name)
                #print(fd)
            except:
                time.sleep(delay)
                gc.collect()
                continue

            if fd:# shm_fd = 'total 0' 
                #print(fd)
                os.system(f"mv {shm_name} {cp_shm_name}")
                try:
                    shm_fd = os.open(cp_shm_name, os.O_RDONLY)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(delay)
                    continue
                try:
                    # Read data into a shared memory view
                    shared_memory = array.array('B', os.read(shm_fd, shm_size))
                    # Read data
                    message = shared_memory.decode().strip()
                    if message:
                        #print("Received:", message)
                        pop = gui.DrawObject()
                        pop.draw_popup(message,1.5)
                        message = ''
                    else:
                        print('No message!')
                        #break
                except Exception as e:
                    print(f"Read Error: {e}")
                    pass 
                # Close file descriptor
                os.close(shm_fd)
                
                # Remove shared memory
                os.remove(cp_shm_name)
            else:
                pass
            time.sleep(delay)
            gc.collect()

    def __key_shm_thread(self, key_delay=0.1):
        import _thread
        _thread.start_new_thread(self.__dso_key_shm, ("Thread1",key_delay))

    def get_key(self):
        key_out = ''
        key_cnt_out = '' 
        try:
            if self.key_flag == True:
                key_out = int(self.key_code)
                key_cnt_out = int(self.key_cnt)
                if key_cnt_out > 128:
                    key_cnt_out = key_cnt_out - 256
                self.key_code = ''
                self.key_cnt = ''
                self.key_flag = False
                return key_out,key_cnt_out
        except:
            pass
        return 0,0
    
    def __dso_key_shm(self, thread_name, delay):
        import array
        shm_name = "/dev/shm/upy/shm_key"
        cp_shm_name =  "/dev/shm/upy/copy_shm_key"
        shm_size = 10
        flag = False
        
        while True:
            try:
                fd = os.stat(shm_name)
                #print(fd)
            except:
                if self.key_code == False:
                    self.key = ''
                time.sleep(delay)
                gc.collect()
                continue

            if fd and self.key_flag == False:
                os.system(f"mv {shm_name} {cp_shm_name}")
                try:
                    shm_fd = os.open(cp_shm_name, os.O_RDONLY)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(delay)
                    continue
                try:
                    # Read data into a shared memory view
                    shared_memory = array.array('B', os.read(shm_fd, shm_size))
                    # Read data
                    message = shared_memory.decode().strip()
                    if message:
                        #print("Received:", message)
                        self.key_flag = True
                        for i in range(shm_size):
                            if message[i] != ',' and flag == False:
                                self.key_code += message[i]
                            elif message[i] == ',':
                                flag = True
                            elif message[i] != '\x00' and flag == True:
                                self.key_cnt += message[i]
                            elif message[i] == '\x00':
                                flag = False
                                break
                        #self.key_code = message
                        
                        message = ''
                    else:
                        print('No message!')
                        #break
                except Exception as e:
                    print(f"Read Error: {e}")
                    pass 
                # Close file descriptor
                os.close(shm_fd)
                
                # Remove shared memory
                os.remove(cp_shm_name)
            else:
                pass
            if self.key_code == False:
                self.key = ''
            time.sleep(delay)
            gc.collect()

class ScreenBasic():
    """The general screen information.

    Depending on the DSO, the value may be different.
    """
    def __init__(self) -> None:
        self.width = 800
        self.height = 480

class ThemeBasic():
    """The general theme color setting.
    
    Depending on the DSO, the color hex value may be different.
    """
    def __init__(self) -> None:
        try:
            #self.bg_color = 0xFFFFFF
            self.bg_color = color.DKGRAY
            self.grid_color = color.GRAY
            self.text_color = color.LTGRAY
        except:
            pass
    