import PySimpleGUI as sg
from base import get_target_number

class NumberGuessGame:
    def __init__(self):
        self.target_number = get_target_number()
        self.attempts = 0
        self.player_name = ''
        self.history_file = 'game_history.txt'
        self.results_window = None

    def is_even(self, number):
        return number % 2 == 0

    def run_game(self):
        layout = [
            [sg.Text('Введіть ваше ім\'я:'), sg.InputText(key='-NAME-')],
            [sg.Text('Вгадайте число від 1 до 20:')],
            [sg.InputText(key='-GUESS-')],
            [sg.Button('ОК'), sg.Button('Вивести результати'), sg.Button('Вихід')],
            [sg.Text('', size=(40, 2), key='-OUTPUT-')],
            [sg.Text('', size=(40, 2), key='-EVEN-')]
        ]

        window = sg.Window('ВГАДАЙ ЧИСЛО', layout, finalize=True)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Вихід'):
                break

            if event == 'ОК':
                self.player_name = values['-NAME-']
                user_guess = values['-GUESS-']

                if user_guess.isdigit():
                    user_guess = int(user_guess)
                    self.attempts += 1

                    if user_guess < self.target_number:
                        window['-OUTPUT-'].update('Загадане число більше.')
                    elif user_guess > self.target_number:
                        window['-OUTPUT-'].update('Загадане число менше.')
                    else:
                        result_message = f"Вітаємо, {self.player_name}! Ви вгадали число {self.target_number} за {self.attempts} спроб."

                        # Додано виведення про парність числа
                        if self.is_even(self.target_number):
                            window['-EVEN-'].update('Загадане число парне!')
                            result_message += ' (парне)'
                        else:
                            window['-EVEN-'].update('Загадане число непарне!')
                            result_message += ' (непарне)'

                        window['-OUTPUT-'].update(result_message)

                        # Збереження історії гри
                        self.save_game_history(result_message)

                        event, _ = window.read()
                        break

            if event == 'Вивести результати':
                self.show_results()

        window.close()

    def save_game_history(self, result_message):
        with open(self.history_file, 'a') as file:
            file.write(f"{self.player_name}: {result_message}\n")

    def show_results(self):
        if self.results_window:
            self.results_window.close()

        layout = [
            [sg.Text('Результати гри')],
            [sg.Multiline(self.read_history(), size=(50, 10), key='-RESULTS-', disabled=True)],
            [sg.Button('Закрити')]
        ]

        self.results_window = sg.Window('Результати гри', layout, finalize=True)

        while True:
            event, values = self.results_window.read()

            if event in (sg.WIN_CLOSED, 'Закрити'):
                break

        self.results_window.close()

    def read_history(self):
        try:
            with open(self.history_file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'Історія гри порожня.'

game = NumberGuessGame()
game.run_game()
