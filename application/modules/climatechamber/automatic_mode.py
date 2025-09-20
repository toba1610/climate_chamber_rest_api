from flask import current_app

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ...data.voetsch_data import defines
    from ...data.voetsch_data import connection

class AutomaticModeClass():

    '''
        All commands to start predefient programs

        Methodes
        --------

        start_program(self, program_number: int, number_of_runthrough: int, chamber_number: int = 1) -> bool:
            Start the choosen program immediately
        pause_program(self, chamber_number: int = 1) -> bool:
            Pause the running program
        return_program(self, chamber_number: int = 1) -> bool:
            Return to running state

        change_number_of_repetition(self, number_of_repitition: int, chamber_number: int = 1) -> bool:
            Change the number of times the choosen program is repeated

        start_program_at_given_date(self, date: str, chamber_number: int = 1) -> bool:
            The program is started at the given date
        start_program_after_give_time(self, time: int, chamber_number: int = 1) -> bool:
            The program is started after the given time expired
        '''

    def __init__(self) -> None:
        
        self.log = current_app.config['LOGGER']
        self.defines = cast('defines' ,current_app.config['COMMAND_DATA'])
        self.connection = cast('connection', current_app.config['CONNECT_DATA'])

    def start_program(self, program_number: int, number_of_repetition: int = 1, chamber_number: int = 1) -> bool:

        '''
        Start the choosen program in automatic mode

            Parameters:
                program_number (int): The number of the program in the internal storage of the chamber
                number_of_runthrough (int): The number how often the program is run through
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        if number_of_repetition == 0:
            number_of_repetition = 1

        output = self.connection.client_socket.send_write_command('19014', [str(chamber_number), str(program_number), str(number_of_repetition)])
        self.log.info('program started: {program_number}')
        return output
    
    def set_program(self, program_number:int) -> bool:

        output = self.connection.client_socket.send_write_command('19015', [str(program_number)])
        self.log.info('program set to: {program_number}')
        return output

    def pause_program(self, chamber_number: int = 1) -> bool:
        '''
        Pauses the choosen program in automatic mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = self.connection.client_socket.send_write_command('19209', [str(chamber_number), str(1), str(2)])
        self.log.info('program paused')
        return output

    def resume_program(self, chamber_number: int = 1) -> bool:
        '''
        Continues the started program in automatic mode

            Parameters:
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = self.connection.client_socket.send_write_command('19209', [str(chamber_number), str(1), str(4)])
        self.log.info('program returned')
        return output

    def change_number_of_repetition(self, number_of_repitition: int, chamber_number: int = 1) -> bool:
        '''
        Changes the numer of repetition

            Parameters:
                number_of_repitition (int): The number how often the program is run through
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = self.connection.client_socket.send_write_command('19003', [str(chamber_number), str(number_of_repitition), str(0)])
        self.log.info(f'Changed Number of repetition to: {number_of_repitition}')
        return output

    def start_program_at_given_date(self, date: str, chamber_number: int = 1) -> bool:
        '''
        Start the program at a given date

            Parameters:
                date (str): formated string for the start date
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = self.connection.client_socket.send_write_command('19207', [str(chamber_number), date])
        self.log.info(f'program will start at: {date}')
        return output

    def start_program_after_give_time(self, time: int, chamber_number: int = 1) -> bool:
        '''
        Start program after the given time is up

            Parameters:
                time (int): Time till start in seconds
                chamber_number (int): Number of the chamber to control

            Returns:
                status (bool): Answer if commands was succesful
        '''

        output = self.connection.client_socket.send_write_command('19009', [str(chamber_number), str(time)])
        self.log.info(f'program will start in: {time} seconds')
        return output