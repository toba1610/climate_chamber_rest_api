import socket
import logging

from application.modules.climatechamber.format import Format_Data_Class

class ConnectionClass():

    '''
    Manage all LAN-Connection related actions


    Methods
    -------

    connect_to_chamber(self, adress: str, port: int) -> socket.socket:
        creates a connection to the controll unit

    '''

    def __init__(self, logger: logging.Logger, defines_data) -> None:
        
        self.log = logger
        self.defines =  defines_data
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.formater = Format_Data_Class()

    def connect_to_chamber(self, adress: str, port: int) -> bool:

        '''
        Connects to the controll unit

            Parameters:
                adress (str): The IP-Adress of the controll unit as string
                port (int): The port to controll the unit as int

            Returns:
                client_socket (socket): The connection socket to use in the programm

        '''

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client_socket.connect((adress, port))
        client_socket.settimeout(5)

        self.connection = client_socket

        # current_app.config['CONNECT_DATA'].client_socket = client_socket

        if result == None:
            self.log.info(f'Connected to chamber with IP= {adress}:{port}')
            return True
        else:
            self.log.error(f'Could not connect to set IP-Adress= {adress}:{port}')
            raise ConnectionError("Could not connect to set IP-Adress")

    def send_write_command(self, command_number: str, arglist: list) -> bool:

        '''
        Send the given command code and list of string arguments to the control unit

            Parameters:
                command_number (str): Number as string for the command to use
                arglist (list): List of string with the arguments needed for the command

            Returns:
                status (bool): Returns if commands was succesful
        '''

        command = self.formater.format_SimServ_Cmd(command_number, arglist)
        self.connection.send(command)
        result = self.connection.recv(512)

        if result == self.defines.GOOD_COMMAND:
            self.log.info(f'Command send successful: {command_number}, {result}')
            return True
        else:
            self.log.warning(f'Command was not send successfuly, {command_number}, {arglist}')
            return False

    def send_read_command(self, command_number: str, arglist: list) -> float:

        '''
        Send the given command code and list of string arguments to the control unit and receive the wanted data

            Parameters:
                command_number (str): Number as string for the command to use
                arglist (list): List of string with the arguments needed for the command

            Returns:
                status (float): Returns the wanted data
        '''

        command = self.formater.format_SimServ_Cmd(command_number, arglist)
        self.connection.send(command)
        # result = self.connection.recv(512)
        
        try:
            result = self.connection.recv(512)
        except socket.timeout:
            print("Timeout: No response received.")
            return 0.0

        output = self.formater.format_SimServ_Data(result, 1)

        if output == self.defines.BAD_COMMAND:
            self.log.error(f'Data could not be read from control unit: {command_number}, {arglist}')
            raise ConnectionError ('Data couldnt be read from control unit')
        else:
            self.log.info(f'Data read succesful, {command_number}, {output}')
            return output

    def send_read_command_message(self, command_number: str, arglist: list) -> str:

        '''
        Send the given command code and list of string arguments to the control unit and receive the wanted data

            Parameters:
                command_number (str): Number as string for the command to use
                arglist (list): List of string with the arguments needed for the command

            Returns:
                status (float): Returns the wanted data
        '''

        command = self.formater.format_SimServ_Cmd(command_number, arglist)
        self.connection.send(command)
        # result = self.connection.recv(512)
        
        try:
            result = self.connection.recv(512)
        except socket.timeout:
            print("Timeout: No response received.")
            return ''

        output = self.formater.format_SimServ_Message(result, 1)

        if output == self.defines.BAD_COMMAND:
            self.log.error(f'Data could not be read from control unit: {command_number}, {arglist}')
            raise ConnectionError ('Data couldnt be read from control unit')
        else:
            self.log.info(f'Data read succesful, {command_number}, {output}')
            return output

    def close_connection(self) -> None:

        '''
        Close the connection to the controll unit
        '''

        self.connection.close()
        self.log.info('Connection closed')