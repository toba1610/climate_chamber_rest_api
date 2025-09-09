from flask import current_app
from datetime import datetime

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import logging
    from ...data.voetsch_data import defines
    from ...data.voetsch_data import connection


class Get_Data_Class():

    '''
    All commands to read Data from the controll unit

    Methods
    -------

    get_min_temperature_warning_limit(self, chamber_number: int = 1) -> float:
        Reads the minimal warning level for temperature for the specified chamber number
    get_max_temperature_warning_limit(self, chamber_number: int = 1) -> float:
        Reads the maximum warning level for temperature for the specified chamber number
    get_min_temperature_alarm_limit(self, chamber_number: int = 1) -> float:
        Reads the minimal alarm level for temperature for the specified chamber number
    get_max_temperature_alarm_limit(self, chamber_number: int = 1) -> float:
        Reads the maximum alarm level for temperature for the specified chamber number

    get_min_humidity_warning_limit(self, chamber_number: int = 1) -> float:
        Reads the minimal warning level for humidity for the specified chamber number
    get_max_humidity_warning_limit(self, chamber_number: int = 1) -> float:
        Reads the maximum warning level for humidity for the specified chamber number
    get_min_humidity_alarm_limit(self, chamber_number: int = 1) -> float:
        Reads the minimal alarm level for humidity for the specified chamber number
    get_max_humidity_alarm_limit(self, chamber_number: int = 1) -> float:
        Reads the maximum alarm level for humidity for the specified chamber number

    get_current_temperature(self, chamber_number: int = 1) -> float:
        Reads the current temperature for the specified chamber number

    get_current_humidity(self, chamber_number: int = 1) -> float:
        Reads the current humidity for the specified chamber number
    '''

    def __init__(self) -> None:

        self.log = current_app.config['LOGGER']
        self.connection = cast('connection', current_app.config['CONNECT_DATA'])

    def get_min_temperature_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11016", [str(chamber_number), '1'])

        return output

    def get_max_temperature_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11017", [str(chamber_number), '1'])

        return output

    def get_min_temperature_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11014", [str(chamber_number), '1'])

        return output

    def get_max_temperature_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11015", [str(chamber_number), '1'])

        return output

    def get_min_humidity_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11016", [str(chamber_number), '2'])

        return output

    def get_max_humidity_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11017", [str(chamber_number), '2'])

        return output

    def get_min_humidity_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11014", [str(chamber_number), '2'])

        return output

    def get_max_humidity_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11015", [str(chamber_number), '2'])

        return output

    def get_current_temperature(self, chamber_number: int = 1) -> float:

        '''
        Get the current temperature

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                output (float): The current temperature of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11004", [str(chamber_number), '1'])

        return output

    def get_current_humidity(self, chamber_number: int = 1) -> float:

        '''
        Get the current humidity

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                output (float): The current humidity of the chamber
        '''
        output = self.connection.client_socket.send_read_command("11004", [str(chamber_number), '2'])

        return output
