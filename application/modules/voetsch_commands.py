import socket
from datetime import datetime
import logging

#
class log_data():
    '''
    All Actions to perform logging of the script
    '''

    def __init__(self) -> None:
        self.logging_enabled:bool = False

    def enable_logging(self, file: str = 'climate.log', encoding: str = 'utf-8', logging_level: int = logging.DEBUG):

        '''
        Enable the logging for the communiocation script

            Parameters:
                file (str): Path and filename to store the logged data
                encoding (str): The encoding used to store the data

                logging_level (logging._Level) = Level of messages logged

        '''
        self.logging_enabled = True

        logging.basicConfig(filename=file, encoding=encoding, level=logging_level, format='%(asctime)s %(levelname)s: %(message)s')

    def log_data(self, level: str, message: str, *varibles):

        '''
        If logging is enable log the given data to the log file

            Parameters:
                level (str): The level of the log data valid inputs are: \n - debug, \n - info, \n - warning, \n - error \n
                message (str): The message that should be logged
                *varibles: Any type of data that should be logged
                
        '''

        if self.logging_enabled == True:
            pass
        else:
            return

        for data in varibles:
            message += f", {data}"

        match level:
            
            case 'debug':
                logging.debug(message)
            case 'info':
                logging.info(message)
            case 'warning':
                logging.warning(message)
            case 'error':
                logging.error(message)    
#
class var_data_class():

    '''
    Storing the constants and internalie used Variables
    '''

    def __init__(self) -> None:
        self.DELIM = b'\xb6'
        self.CR = b'\r'
        self.GOOD_COMMAND = b'1\r\n'
        self.BAD_COMMAND = ""

        self.client_socket: socket.socket
#
class connection_class():

    '''
    Manage all LAN-Connection related actions


    Methods
    -------

    connect_to_chamber(self, adress: str, port: int) -> socket.socket:
        creates a connection to the controll unit

    '''

    def __init__(self) -> None:
        pass

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

        var_data.client_socket = client_socket

        if result == None:
            log.log_data('info', 'Connected to chamber with IP', adress, port)
            return True
        else:
            log.log_data('error', "Could not connect to set IP-Adress", adress, port)
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

        command = format_data.format_SimServ_Cmd(command_number, arglist)
        var_data.client_socket.send(command.encode())
        result = var_data.client_socket.recv(512)

        if result == var_data.GOOD_COMMAND:
            log.log_data('info', 'Command send successful', command_number, result)
            return True
        else:
            log.log_data('warning', 'Command send not successful', command_number, arglist)
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

        command = format_data.format_SimServ_Cmd(command_number, arglist)
        var_data.client_socket.send(command.encode())
        result = var_data.client_socket.recv(512)
        output = format_data.format_SimServ_Data(result, 1)

        if output == var_data.BAD_COMMAND:
            log.log_data('error', 'Data could not be read from control unit', command_number, arglist)
            raise ConnectionError ('Data couldnt be read from control unit')
        else:
            log.log_data('info', 'Data read succesful', command_number, output)
            return output
#
class format_data_class():

    '''
    Format the input data in useful data for the programm

    Methods
    -------

    format_SimServ_Cmd(self, cmdID: str, arglist: list) -> str:
        Returns an SimServ compatible string to control the chamber control unit
    format_SimServ_Data (self, data: bytes, parameter: int = 1) -> float:
        Returns the Payload Value of the input string
    '''

    def __init__(self) -> None:
        pass

    def format_SimServ_Cmd(self, cmdID: str, arglist: list) -> str:

        '''
        Format the needed command with the given inputs

            Parameters:
                cmdID (str): The five digits number provided by the documentation
                arglist (list): List of the needed parameters for the command

            Returns:
                cmd (str): The assembled command ready to use

        '''
        cmd = cmdID.encode('ascii')

        for arg in arglist:
            cmd = cmd + var_data.DELIM
            arg = str(arg)
            cmd = cmd + arg.encode('ascii')
        cmd = cmd + var_data.CR

        return str(cmd)

    def format_SimServ_Data(self, data: bytes, parameter: int = 1) -> float:

        '''
        Formats the Input Data from Bytestream to float

            Parameters:
                data (bytes): Input Data from socket.recv()
                parameter (int): Index which return value is needed

            Returns:
                output (float): The choosen item formated as float
        '''

        list = data.split(var_data.DELIM)
        output = 0.0

        for index, element in enumerate(list):
            if index == parameter:
                output = float(element)
                output = round(output,1)
                return output
   
        return output
 

    def format_date_string(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> str:


        try:

            datetime(year, month, day, hour, minute, second)
            output = f"{year}-{month}-{day}-{hour}-{minute}-{second}"
            return output

        except ValueError:
            log.log_data('error', 'The given date is not valid', year, month, day, hour, minute, second)
            raise ValueError("The given date is not valid")
#
class get_data_class():

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
        pass

    def get_min_temperature_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11016", [str(chamber_number), '1'])

        return output

    def get_max_temperature_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11017", [str(chamber_number), '1'])

        return output

    def get_min_temperature_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11014", [str(chamber_number), '1'])

        return output

    def get_max_temperature_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11015", [str(chamber_number), '1'])

        return output

    def get_min_humidity_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11016", [str(chamber_number), '2'])

        return output

    def get_max_humidity_warning_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11017", [str(chamber_number), '2'])

        return output

    def get_min_humidity_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11014", [str(chamber_number), '2'])

        return output

    def get_max_humidity_alarm_limit(self, chamber_number: int = 1) -> float:

        '''
        Returns the value of the choosen parameter set in the chamber controll\n

            Parameters:
                chamber_number (int): Variable to Control which chamber is used preset = 1\n

            Returns:\n
                formated_value (float): The read value of the chamber
        '''
        output = connection.send_read_command("11015", [str(chamber_number), '2'])

        return output

    def get_current_temperature(self, chamber_number: int = 1) -> float:

        '''
        Get the current temperature

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                output (float): The current temperature of the chamber
        '''
        output = connection.send_read_command("11004", [str(chamber_number), '1'])

        return output

    def get_current_humidity(self, chamber_number: int = 1) -> float:

        '''
        Get the current humidity

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                output (float): The current humidity of the chamber
        '''
        output = connection.send_read_command("11004", [str(chamber_number), '2'])

        return output
#
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
        pass

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

        if get_data.get_min_temperature_warning_limit() > value:
            log.log_data('warning', 'The given value is to high for warning levels', value)
            raise ValueError("Min warning level to high")
        elif get_data.get_max_temperature_warning_limit() < value:
            log.log_data('warning', 'The given value is to high for warning levels', value)
            raise ValueError("Max warning level to low")
        elif get_data.get_min_temperature_alarm_limit() > value:
            log.log_data('warning', 'The given value is to high for alarm levels', value)
            raise ValueError("Min alarm level to high")
        elif get_data.get_max_temperature_alarm_limit() < value:
            log.log_data('warning', 'The given value is to high for alarm levels', value)
            raise ValueError("Max alarm level to low")
        else:

            output = connection.send_write_command('11001', [str(chamber_number), "1", str(value)])
            log.log_data('info', 'Send new temperature setpoint succesful')
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

        if get_data.get_min_humidity_warning_limit() > value:
            log.log_data('warning', 'The given value is to high for warning levels', value)
            raise ValueError("Min warning level to high")
        elif get_data.get_max_humidity_warning_limit() < value:
            log.log_data('warning', 'The given value is to high for warning levels', value)
            raise ValueError("Max warning level to low")
        elif get_data.get_min_humidity_alarm_limit() > value:
            log.log_data('warning', 'The given value is to high for alarm levels', value)
            raise ValueError("Min alarm level to high")
        elif get_data.get_max_humidity_alarm_limit() < value:
            log.log_data('warning', 'The given value is to high for alarm levels', value)
            raise ValueError("Max alarm level to low")
        else:

            output = connection.send_write_command('11001', [str(chamber_number), "2", str(value)])
            log.log_data('info', 'Send new humidity setpoint succesful')
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
        output = connection.send_write_command('11068', [str(chamber_number), "1", str(gradient)])
        log.log_data('info', 'Send new positiv temperatur gradient succesful')
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
        output = connection.send_write_command('11072', [str(chamber_number), "1", str(gradient)])
        log.log_data('info', 'Send new negativ temperatur gradient succesful')
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
        output = connection.send_write_command('11068', [str(chamber_number), "2", str(gradient)])
        log.log_data('info', 'Send new positiv humidity gradient succesful')
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
        output = connection.send_write_command('11072', [str(chamber_number), "2", str(gradient)])
        log.log_data('info', 'Send new negativ humidity gradient succesful')
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

        act_temp = get_data.get_current_temperature(chamber_number)
        status = self.set_setpoint_temperature(act_temp, chamber_number)

        if status == True:
            if gradient > 0:
                status = self.set_positiv_gradient_temperature(gradient, chamber_number)
            elif gradient < 0:
                status = self.set_negativ_gradient_temperature(gradient, chamber_number)
            else:
                log.log_data('error', 'Gradient can not be 0', gradient)
                raise ValueError("Gradient can not be 0")
        else:
            log.log_data('error', 'Gradient mode could not be started, start point = act_temp could not be set')
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

        act_humi = get_data.get_current_humidity(chamber_number)
        status = self.set_setpoint_humidity(act_humi, chamber_number)

        if status == True:
            if gradient > 0:
                status = self.set_positiv_gradient_humidity(gradient, chamber_number)
            elif gradient < 0:
                status = self.set_negativ_gradient_humidity(gradient, chamber_number)
            else:
                log.log_data('error', 'Gradient can not be 0', gradient)
                raise ValueError("gradient can not be 0")
        else:
            log.log_data('error', 'Gradient mode could not be started, start point = act_humi could not be set')
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
            log.log_data('error', 'Gradient mode couldnt be stopped')
            raise ConnectionError("Could not change Gradient")

    def start_man_mode(self, chamber_number: int = 1) -> bool:
        '''
        Start the choosen chamber in manuel mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = connection.send_write_command('14001', [str(chamber_number), "1", "1"])
        log.log_data('info', 'Manual mode started')
        return output

    def stop_man_mode(self, chamber_number: int = 1) -> bool:
        '''
        Stop the choosen chamber in manuel mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''
        output = connection.send_write_command('14001', [str(chamber_number), "1", "0"])
        log.log_data('info', 'Manual mode stoped')
        return output
#
class automatic_mode_class():

    '''
        All commands to start predefient programms

        Methodes
        --------

        start_programm(self, programm_number: int, number_of_runthrough: int, chamber_number: int = 1) -> bool:
            Start the choosen programm immediately
        pause_programm(self, chamber_number: int = 1) -> bool:
            Pause the running programm
        return_programm(self, chamber_number: int = 1) -> bool:
            Return to running state

        change_number_of_repetition(self, number_of_repitition: int, chamber_number: int = 1) -> bool:
            Change the number of times the choosen program is repeated

        start_programm_at_given_date(self, date: str, chamber_number: int = 1) -> bool:
            The program is started at the given date
        start_programm_after_give_time(self, time: int, chamber_number: int = 1) -> bool:
            The program is started after the given time expired
        '''

    def __init__(self) -> None:
        pass

    def start_programm(self, programm_number: int, number_of_runthrough: int, chamber_number: int = 1) -> bool:

        '''
        Start the choosen programm in automatic mode

            Parameters:
                programm_number (int): The number of the programm in the internal storage of the chamber
                number_of_runthrough (int): The number how often the programm is run through
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        if number_of_runthrough == 0:
            number_of_runthrough = 1

        output = connection.send_write_command('19014', [str(chamber_number), str(programm_number), str(number_of_runthrough)])
        log.log_data('info', 'Programm started', programm_number)
        return output

    def pause_programm(self, chamber_number: int = 1) -> bool:
        '''
        Pauses the choosen programm in automatic mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = connection.send_write_command('19209', [str(chamber_number), str(1), str(2)])
        log.log_data('info', 'Programm paused')
        return output

    def return_programm(self, chamber_number: int = 1) -> bool:
        '''
        Continues the started programm in automatic mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = connection.send_write_command('19209', [str(chamber_number), str(1), str(4)])
        log.log_data('info', 'Programm returned')
        return output

    def change_number_of_repetition(self, number_of_repitition: int, chamber_number: int = 1) -> bool:
        '''
        Changes the numer of repetition

            Parameters:
                number_of_repitition (int): The number how often the programm is run through
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = connection.send_write_command('19003', [str(chamber_number), str(number_of_repitition), str(0)])
        log.log_data('info', 'Changed Number of repetition to', number_of_repitition)
        return output

    def start_programm_at_given_date(self, date: str, chamber_number: int = 1) -> bool:
        '''
        Start the Programm at a given date

            Parameters:
                date (str): formated string for the start date
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = connection.send_write_command('19207', [str(chamber_number), date])
        log.log_data('info', 'Programm will start at', date)
        return output

    def start_programm_after_give_time(self, time: int, chamber_number: int = 1) -> bool:
        '''
        Start programm after the given time is up

            Parameters:
                time (int): Time till start in seconds
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = connection.send_write_command('19009', [str(chamber_number), str(time)])
        log.log_data('info', 'Programm will start in', time)
        return output
#
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
        pass

    def get_status(self, chamber_number: int = 1) -> str:

        '''
        Read the status of the chamber

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (str): Returns a string with the status Message
        '''

        status_index = connection.send_read_command('10012', [str(chamber_number)])

        match status_index:

            case 1:
                log.log_data('info', 'System is not running')
                return 'System is not running'
            case 3:
                log.log_data('info', 'System is running')
                return 'System is running'
            case 5:
                log.log_data('warning', 'System is not running with warning')
                return 'System is not running with warnings'
            case 7:
                log.log_data('warning', 'System is running with warning')
                return 'System is running with warnings'
            case 9:
                log.log_data('warning', 'System is not running with alarms')
                return 'System is not running with alarms'
            case 11:
                log.log_data('warning', 'System is running with alarms')
                return 'System is running with alarms'
            case 13:
                log.log_data('warning', 'System is not running with errors and alarms')
                return 'System is not running with errors and alarms'
            case 15:
                log.log_data('warning', 'System is running with errors and alarms')
                return 'System is running with errors and alarms'
            case _:
                log.log_data('warning', 'No status found')
                return 'No status found'

    def get_program_status(self, chamber_number: int =1) -> str:
            
            '''
            Read the status of the running program

                Parameters:
                    chamber_number (int): Number of the chamber to control

                Returns:
                    status (str): Returns a string with the program status Message
            '''

            status_index = connection.send_read_command('19210', [str(chamber_number)])

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
            
            log.log_data('info', message)
            return message

    def get_actual_loops(self, chamber_number: int =1) -> int:

        '''
        Read the actual number of program loops

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Number of loops already passed
        '''


        status = connection.send_read_command('19006', [str(chamber_number), '0'])
        log.log_data('info', 'Read actual loops')
        return int(status)

    def get_program_active_time(self, chamber_number: int =1) -> int:

        '''
        Read the actual number of program loops

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Time passed in seconds
        '''


        status = connection.send_read_command('19021', [str(chamber_number)])
        log.log_data('info', 'Read the passed time in the program')
        return int(status)

    def get_program_number(self, chamber_number: int =1) -> int:

        '''
        Read the number of the running program

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (int): Number of the running program
        '''


        status = connection.send_read_command('19204', [str(chamber_number)])
        log.log_data('info', 'Read number of the running program')
        return int(status)

    def reset_errors(self, chamber_number: int = 1) -> bool:

        '''
        Read the status of the chamber

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        status = connection.send_read_command('17012', [str(chamber_number)])
        log.log_data('info', 'Error reseted')
        return bool(status)

    def get_number_of_messages(self, chamber_number: int = 1) -> int:

        '''
        Read the number of message configured in the control unit

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                number_of_messages (int): Returns the number of configured messages
        '''

        number = connection.send_read_command('17002', [str(chamber_number)])
        log.log_data('info', 'Number of Messages', number)
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

        status = connection.send_read_command('17009', [str(chamber_number), str(number_of_message)])

        if status == 1:
            log.log_data('info', 'Message is active', number_of_message)
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

        status = connection.send_read_command('17007', [str(chamber_number), str(number_of_message)])
        log.log_data('info', 'Message read', status)
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

        log.log_data('info', 'These messages are active', temp_list_of_messages)
        return temp_list_of_messages

var_data = var_data_class()
connection = connection_class()
format_data = format_data_class()
get_data = get_data_class()
manual_mode = manual_mode_class()
automatic_mode = automatic_mode_class()
status = status_class()
log = log_data()