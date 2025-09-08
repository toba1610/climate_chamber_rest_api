import socket
from flask import current_app

from typing import TYPE_CHECKING, cast
# from .format import Format_Data_Class
# from.get_data import Get_Data_Class

if TYPE_CHECKING:
    import logging
    from ...data.voetsch_data import defines
    from ...data.voetsch_data import connection

class status_class():

    '''
        All commands to check the status of the chamber

        Methodes
        --------

        get_status(self, chamber_number: int = 1) -> str:
            Read status message

        get_program_status(self, chamber_number: int = 1) -> str:
            Read status message of the running program

        get_program_active_time(self, chamber_number: int = 1) -> str:
            Read time that the program is running

        get_program_number(self, chamber_number: int = 1) -> str:
            Read the number of the running program

        reset_errors(self, chamber_number: int = 1) -> bool:
            Reset all errors if reason for error is resolved

        get_number_of_messages(self, chamber_number: int = 1) -> int:
            Reads the number of configured messages

        get_status_of_message(self, number_of_message: str, chamber_number: int = 1) -> bool:
            Returns the status of the given message

        def get_message_text(self, number_of_message: str, chamber_number: int = 1) -> str:
            Returns the text of the given message
    '''

    def __init__(self) -> None:
        
        self.log = current_app.config['LOGGER']
        self.defines = cast('defines' ,current_app.config['COMMAND_DATA'])
        self.connection = cast('connection', current_app.config['CONNECT_DATA'])

    def get_status(self, chamber_number: int = 1) -> str:

        '''
        Read the status of the chamber

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (str): Returns a string with the status Message
        '''

        status_index = self.connection.client_socket.send_read_command('10012', [str(chamber_number)])

        match status_index:

            case 1:
                self.log.info('System is not running')
                return 'System is not running'
            case 3:
                self.log.info('System is running')
                return 'System is running'
            case 5:
                self.log.warning('System is not running with warning')
                return 'System is not running with warnings'
            case 7:
                self.log.warning('System is running with warning')
                return 'System is running with warnings'
            case 9:
                self.log.warning('System is not running with alarms')
                return 'System is not running with alarms'
            case 11:
                self.log.warning('System is running with alarms')
                return 'System is running with alarms'
            case 13:
                self.log.warning('System is not running with errors and alarms')
                return 'System is not running with errors and alarms'
            case 15:
                self.log.warning('System is running with errors and alarms')
                return 'System is running with errors and alarms'
            case _:
                self.log.warning('No status found')
                return 'No status found'

    def get_program_status(self, chamber_number: int =1) -> str:
            
            '''
            Read the status of the running program

                Parameters:
                    chamber_number (int): Number of the chamber to control

                Returns:
                    status (str): Returns a string with the program status Message
            '''

            status_index = self.connection.client_socket.send_read_command('19210', [str(chamber_number)])

            match status_index:

                case 0:
                    message = 'Program is not running'
            
                case 1:
                    message = 'Program is running'

                case 3:
                    message = 'Program is paused'

                case 5:
                    message = 'Waiting for Actual Value'

                case 8:
                    message = 'Program is finished'

                case 16:
                    message = 'Waiting for Starttime'

                case 48:
                    message = 'Paused from PLC'

                case _:
                    message = 'No status found'
            
            self.log.info(f'Running Program status: {message}')
            return message

    def get_actual_loops(self, chamber_number: int =1) -> int:

        '''
        Read the actual number of program loops

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Number of loops already passed
        '''


        status = self.connection.client_socket.send_read_command('19006', [str(chamber_number), '0'])
        self.log.info(f'Read actual loops. loops passed: {status}')
        return int(status)

    def get_program_active_time(self, chamber_number: int =1) -> int:

        '''
        Read the actual number of program loops

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Time passed in seconds
        '''


        status = self.connection.client_socket.send_read_command('19021', [str(chamber_number)])
        self.log.info('Read the passed time in the program')
        return int(status)

    def get_program_number(self, chamber_number: int =1) -> int:

        '''
        Read the number of the running program

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Number of the running program
        '''


        status = self.connection.client_socket.send_read_command('19204', [str(chamber_number)])
        self.log.info('Read number of the running program')
        return int(status)

    def reset_errors(self, chamber_number: int = 1) -> bool:

        '''
        Read the status of the chamber

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        status = self.connection.client_socket.send_read_command('17012', [str(chamber_number)])
        self.log.info('Error reseted')
        return bool(status)

    def get_number_of_messages(self, chamber_number: int = 1) -> int:

        '''
        Read the number of message configured in the control unit

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                number_of_messages (int): Returns the number of configured messages
        '''

        number = self.connection.client_socket.send_read_command('17002', [str(chamber_number)])
        self.log.info('Number of Messages', number)
        return int(number)

    def get_status_of_message(self, number_of_message: str, chamber_number: int = 1) -> bool:

        '''
        Read the status of an given message number

            Parameters:
                number_of_messages (str): The number of the message that should be read
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Returns the status of the read message
        '''

        status = self.connection.client_socket.send_read_command('17009', [str(chamber_number), str(number_of_message)])

        if status == 1:
            self.log.info('Message is active', number_of_message)
            return True
        else:
            return False

    def get_message_text(self, number_of_message: str, chamber_number: int = 1) -> str:

        '''
        Read the message text of the give number

            Parameters:
                number_of_messages (str): The number of the message that should be read
                chamber_number (int): Number of the chamber to control

            Returns:
                text (str): Returns the configured text of the read message
        '''

        status = self.connection.client_socket.send_read_command('17007', [str(chamber_number), str(number_of_message)])
        self.log.info('Message read', status)
        return str(status)

    def get_list_of_message_text(self, chamber_number: int =1) -> list:

        '''
        Ouputs an list of all active messages

        Parameters:
            chamber_number (int): Number of the chamber to control

        Returns:
            temp_list_of_messages (list): The list of strings with all active messages
        '''

        temp_list_of_messages = []

        number_of_configured_messages = self.get_number_of_messages()

        for message_number in range(0, number_of_configured_messages):

            status_of_message = self.get_status_of_message(str(message_number))

            if status_of_message == True:
                temp_list_of_messages.append(self.get_message_text(str(message_number)))

        self.log.info(f'These messages are active: {temp_list_of_messages}')
        return temp_list_of_messages