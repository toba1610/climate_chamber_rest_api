from flask import current_app
from datetime import datetime
import logging

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    
    from ...data.voetsch_data import defines



class Format_Data_Class():

    '''
    Format the input data in useful data for the programm

    Methods
    -------

    format_SimServ_Cmd(self, cmdID: str, arglist: list) -> str:
        Returns an SimServ compatible string to control the chamber control unit
    format_SimServ_Data (self, data: bytes, parameter: int = 1) -> float:
        Returns the Payload Value of the input string
    '''

    def __init__(self, logger: logging.Logger, defines_data) -> None:

        self.log = logger
        self.defines = defines_data#cast(defines ,current_app.config['COMMAND_DATA'])

    def format_SimServ_Cmd(self, cmdID: str, arglist: list) -> bytes:

        '''
        Format the needed command with the given inputs

            Parameters:
                cmdID (str): The five digits number provided by the documentation
                arglist (list): List of the needed parameters for the command

            Returns:
                cmd (str): The assembled command ready to use

        '''
        cmd = cmdID.encode('ascii')

        # for arg in arglist:
        #     cmd = cmd + self.defines.DELIM
        #     arg = str(arg)
        #     cmd = cmd + arg.encode('ascii')
        # cmd = cmd + self.defines.CR

        cmd = cmdID.encode('ascii') # command ID
        cmd = cmd + self.defines.DELIM + b'1'    # Chb Id
        for arg in arglist:
                cmd = cmd + self.defines.DELIM
                cmd = cmd + arg.encode('ascii')
        cmd = cmd + self.defines.CR
        return cmd

    def format_SimServ_Data(self, data: bytes, parameter: int = 1) -> float:

        '''
        Formats the Input Data from Bytestream to float

            Parameters:
                data (bytes): Input Data from socket.recv()
                parameter (int): Index which return value is needed

            Returns:
                output (float): The choosen item formated as float
        '''

        list = data.split(self.defines.DELIM)
        output = 0.0

        for index, element in enumerate(list):
            if index == parameter:
                output = float(element)
                output = round(output,1)
                return output
   
        return output
    
    def format_SimServ_Message(self, data: bytes, parameter: int = 1) -> str:

        '''
        Formats the Input Data from Bytestream to string

            Parameters:
                data (bytes): Input Data from socket.recv()
                parameter (int): Index which return value is needed

            Returns:
                output (float): The choosen item formated as float
        '''

        list = data.split(self.defines.DELIM)
        output = ''

        for index, element in enumerate(list):
            if index == parameter:
                output = element.decode().strip()
                return output
   
        return output
 

    def format_date_string(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> str:


        try:

            datetime(year, month, day, hour, minute, second)
            output = f"{year}-{month}-{day}-{hour}-{minute}-{second}"
            return output

        except ValueError:
            self.log.error(f'The given date is not valid, {year}, {month}, {day}, {hour}, {minute}, {second}')
            raise ValueError("The given date is not valid")