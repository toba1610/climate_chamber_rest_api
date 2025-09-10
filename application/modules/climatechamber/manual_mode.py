import socket
from flask import current_app

from typing import TYPE_CHECKING, cast
from .format import Format_Data_Class
from.get_data import Get_Data_Class

if TYPE_CHECKING:
    import logging
    from ...data.voetsch_data import defines
    from ...data.voetsch_data import connection


class manual_mode_class():

    '''
    All commands to controll the chamber in manuel mode

    Methodes
    --------

    change_setpoint_temperature(self, value: float, chamber_number: int = 1) -> bool:
        Change the temperature setpoint to the specified Value
    change_setpoint_humidity(self, value: float, chamber_number: int = 1) -> bool:
        Change the humidity setpoint to the specified Value

    set_positiv_gradient_temperature(self, gradient: float, chamber_number: int = 1) -> bool:
        Set up an gradient for an rising temperature °C/min
    set_negativ_gradient_temperature(self, gradient: float, chamber_number: int = 1) -> bool:
        Set up an gradient for an decreasing temperatur °C/min
    set_positiv_gradient_humidity(self, gradient: float, chamber_number: int = 1) -> bool:
        Set up an gradient for an rising humidity °C/min
    set_negativ_gradient_humidity(self, gradient: float, chamber_number: int = 1) -> bool:
        Set up an gradient for an decreasing humidity °C/min

    start_man_mode(self, chamber_number: int = 1) -> bool:
        Start the manuell mode
    stop_man_mode(self, chamber_number: int = 1) -> bool:
        Stop the manuell mode
    '''

    def __init__(self) -> None:
        
        self.log = current_app.config['LOGGER']
        self.defines = cast('defines' ,current_app.config['COMMAND_DATA'])
        self.connection = cast('connection', current_app.config['CONNECT_DATA'])
        self.get_data = Get_Data_Class()
        self.formater = Format_Data_Class()

    def set_setpoint_temperature(self, value: float, chamber_number: int = 1) -> bool:

        '''
        Set a new temperature setpoint in the chamber controll

            Parameters:
                value (float): New value for the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        #Check if the warning and alarm values match the new setpoint

        if self.get_data.get_min_temperature_warning_limit() > value:
            self.log.warning(f'The given value is to high for warning levels: {value}')
            raise ValueError("Min warning level to high")
        elif self.get_data.get_max_temperature_warning_limit() < value:
            self.log.warning(f'The given value is to high for warning levels: {value}')
            raise ValueError("Max warning level to low")
        elif self.get_data.get_min_temperature_alarm_limit() > value:
            self.log.warning(f'The given value is to high for alarm levels: {value}')
            raise ValueError("Min alarm level to high")
        elif self.get_data.get_max_temperature_alarm_limit() < value:
            self.log.warning(f'The given value is to high for alarm levels: {value}')
            raise ValueError("Max alarm level to low")
        else:

            output = self.connection.client_socket.send_write_command('11001', [str(chamber_number), "1", str(value)])
            self.log.info('Send new temperature setpoint succesful')
            return output

    def set_setpoint_humidity(self, value: float, chamber_number: int = 1) -> bool:

        '''
        Set a new humidity setpoint in the chamber controll

            Parameters:
                value (float): New value for the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        #Check if the warning and alarm values match the new setpoint

        if self.get_data.get_min_humidity_warning_limit() > value:
            self.log.warning(f'The given value is to high for warning levels: {value}')
            raise ValueError("Min warning level to high")
        elif self.get_data.get_max_humidity_warning_limit() < value:
            self.log.warning(f'The given value is to high for warning levels: {value}')
            raise ValueError("Max warning level to low")
        elif self.get_data.get_min_humidity_alarm_limit() > value:
            self.log.warning(f'The given value is to high for alarm levels: {value}')
            raise ValueError("Min alarm level to high")
        elif self.get_data.get_max_humidity_alarm_limit() < value:
            self.log.warning(f'The given value is to high for alarm levels: {value}')
            raise ValueError("Max alarm level to low")
        else:

            output = self.connection.client_socket.send_write_command('11001', [str(chamber_number), "2", str(value)])
            self.log.info('info', 'Send new humidity setpoint succesful')
            return output

    def set_positiv_gradient_temperature(self, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set the positiv gradient value for temperatur

            Parameters:
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('11068', [str(chamber_number), "1", str(gradient)])
        self.log.info('Send new positiv temperatur gradient succesful')
        return output

    def set_negativ_gradient_temperature(self, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set the positiv gradient value for temperatur

            Parameters:
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('11072', [str(chamber_number), "1", str(gradient)])
        self.log.info('Send new negativ temperatur gradient succesful')
        return output

    def set_positiv_gradient_humidity(self, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set the positiv gradient value for humidity

            Parameters:
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('11068', [str(chamber_number), "2", str(gradient)])
        self.log.info('Send new positiv humidity gradient succesful')
        return output

    def set_negativ_gradient_humidity(self, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set the positiv gradient value for humidity

            Parameters:
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('11072', [str(chamber_number), "2", str(gradient)])
        self.log.info('Send new negativ humidity gradient succesful')
        return output

    def set_gradient_temperature(self, setpoint: float, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set up the data to controll the chamber in the manuel gradient mode

            Parameters:
                setpoint (float): Setpoint to be reached by the gradient value
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        #Set the Start point for the gradient mode

        act_temp = self.get_data.get_current_temperature(chamber_number)
        status = self.set_setpoint_temperature(act_temp, chamber_number)

        if status == True:
            if gradient > 0:
                status = self.set_positiv_gradient_temperature(gradient, chamber_number)
            elif gradient < 0:
                status = self.set_negativ_gradient_temperature(gradient, chamber_number)
            else:
                self.log.error(f'Gradient can not be 0: {gradient}')
                raise ValueError("Gradient can not be 0")
        else:
            self.log.error(f'Gradient mode could not be started, start point = act_temp could not be set')
            raise ConnectionError('Command could not be transfered to chamber')

        if status == True:
            status = self.set_setpoint_temperature(setpoint, chamber_number)
        else:
            raise ConnectionError('Command could not be transfered to chamber')

        return status

    def set_gradient_humidity(self, setpoint: float, gradient: float, chamber_number: int = 1) -> bool:
        '''
        Set up the data to controll the chamber in the manuel gradient mode

            Parameters:
                setpoint (float): Setpoint to be reached by the gradient value
                gradient (float): Gradient to rech the setpoint
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        act_humi = self.get_data.get_current_humidity(chamber_number)
        status = self.set_setpoint_humidity(act_humi, chamber_number)

        if status == True:
            if gradient > 0:
                status = self.set_positiv_gradient_humidity(gradient, chamber_number)
            elif gradient < 0:
                status = self.set_negativ_gradient_humidity(gradient, chamber_number)
            else:
                self.log.error('Gradient can not be 0: {gradient}')
                raise ValueError("gradient can not be 0")
        else:
            self.log.error(f'Gradient mode could not be started, start point = act_humi could not be set')
            raise ConnectionError('Command could not be transfered to chamber')

        if status == True:
            status = self.set_setpoint_humidity(setpoint, chamber_number)
        else:
            raise ConnectionError('Command could not be transfered to chamber')

        return status

    def stop_gradient_mode(self, chamber_number: int = 1) -> bool:
        '''
        Set the gradien to 0 and stops the gradient mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        status = self.set_positiv_gradient_humidity(0.0, chamber_number)

        if status== True:
            status = self.set_positiv_gradient_temperature(0.0, chamber_number)

        if status== True:
            status = self.set_negativ_gradient_humidity(0.0, chamber_number)

        if status== True:
            status = self.set_negativ_gradient_temperature(0.0, chamber_number)

        if status == True:
            return True
        else:
            self.log.error('Gradient mode couldnt be stopped')
            raise ConnectionError("Could not change Gradient")

    def start_man_mode(self, chamber_number: int = 1) -> bool:
        '''
        Start the choosen chamber in manuel mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('14001', [str(chamber_number), "1"])
        self.log.info('Manual mode started')
        return output

    def stop_man_mode(self, chamber_number: int = 1) -> bool:
        '''
        Stop the choosen chamber in manuel mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = self.connection.client_socket.send_write_command('14001', [str(chamber_number), "0"])
        self.log.info('Manual mode stoped')
        return output
