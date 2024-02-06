import tkinter as tk
from tkinter import messagebox
import random

class Game:
    def __init__(self, rows, cols, bombs):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.root = tk.Tk()

        # self.board for matrix with bombs 
        # which randomly arranged by create_bombs function
        self.board = []
        # list of bombs positions
        self.bombs_position = []

    # creating bombs in self.board list
    def create_bombs(self):
        count = 0
        while count < self.bombs:
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.cols - 1)
            if (x, y) not in self.bombs_position:
                self.bombs_position.append((x, y))
                count += 1

    # creating buttons using tkinter
    def create_buttons(self, parent, x, y, value):
        color_dict = {'1': 'blue', '2': 'green', '3': 'red', '4': 'purple', '5': 'maroon', '6': 'pink', '7': 'brown', '8': 'black'}
        if value == '*':
            btn = tk.Button(parent, text='', width=2, height=1, bg='gray', font=('Helvetica', 10, 'bold'), command=lambda x=x, y=y: self.on_click(x, y))
            btn.bind('<Button-1>', lambda event, x=x, y=y: self.on_click(x, y))
            btn.bind('<Button-3>', lambda event, x=x, y=y: self.on_right_click(x, y))
        else:
            color = color_dict.get(str(value))
            btn = tk.Button(parent, text='', width=2, height=1, bg='gray', fg=color, font=('Helvetica', 10, 'bold'), command=lambda x=x, y=y: self.on_click(x, y))
            btn.bind('<Button-1>', lambda event, x=x, y=y: self.on_click(x, y))
            btn.bind('<Button-3>', lambda event, x=x, y=y: self.on_right_click(x, y))
        btn.grid(row=x, column=y)
        return (btn, value)

    # creating on click logic, using adjacent_bombs function for knowing neighbour values
    def on_click(self, x, y):
        if self.board[x][y][0]['text'] == '':
            if self.board[x][y][1] == '*':
                messagebox.showinfo('Minesweeper', 'LOOOSER')
                self.restart_game()
                return
            elif self.board[x][y][0]["text"] == "":
                self.reveal_empty(x, y)
            else:
                count = self.adjacent_bombs(x, y)
                self.board[x][y][0].config(text=str(count if count > 0 else ' '), bg='white')
                self.check_win()
        elif self.board[x][y][0]['text'] == u"\u2691":
            return
        else:
            count = self.adjacent_bombs(x, y)
            flags_count = self.count_flags_around(x, y)
            if count == flags_count:
                self.reveal_neighbours(x, y)

    def count_flags_around(self, x, y):
        flags_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.rows and 0 <= y + j < self.cols:
                    if self.board[x + i][y + j][0]["text"] == u"\u2691":
                        flags_count += 1
        return flags_count

    def reveal_neighbours(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.rows and 0 <= y + j < self.cols:
                    if self.board[x + i][y + j][0]["text"] == '':
                        self.on_click(x + i, y + j)

    def on_right_click(self, x, y):
        btn, value = self.board[x][y]
        if btn['text'] == '':
            btn.config(text=u"\u2691", fg='red')
        elif btn['text'] == u"\u2691":
            btn.config(text='')

    def reveal_empty(self, x, y):
        if 0 <= x < self.rows and 0 <= y < self.cols and self.board[x][y][0]["text"] == "":
            count = self.adjacent_bombs(x, y)
            self.board[x][y][0].config(text=str(count if count > 0 else ' '), bg='white')

            if count == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.reveal_empty(x + i, y + j)

            self.check_win()

    # calculating neighbour bombs
    def adjacent_bombs(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x + i, y + j) in self.bombs_position:
                    count += 1
        return count
    
    # creating board using tkinder and create_buttons function
    def create_board(self):
        root = self.root
        root.title('Minesweeper')

        # Верхня панель
        self.top_panel = tk.Frame(root)
        self.top_panel.pack(side="top", fill="x")

        # Лейбл для кількості бомб
        self.remaining_bombs_label = tk.Label(self.top_panel, text="Remaining bombs: {}".format(self.bombs))
        self.remaining_bombs_label.pack(side="left", padx=10)

        # Кнопка для налаштувань
        self.settings_button = tk.Button(self.top_panel, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="right", padx=10)

        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                if (row, col) in self.bombs_position:
                    btn = self.create_buttons(root, row, col, '*')
                else:
                    count = self.adjacent_bombs(row, col)
                    btn = self.create_buttons(root, row, col, count)
                button_row.append(btn)
            # appending buttons to list, aka creating matrix of buttons
            self.board.append(button_row)

        root.mainloop()

    # function, that uses other creating funtions for starting the game
    def start_game(self):
        self.create_bombs()
        self.create_board()

    # checking if user wins the game
    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0]["text"] == '' and self.board[i][j][1] != "*":
                    return
        messagebox.showinfo('Minesweeper', 'Congratulations! You won!')
        self.restart_game()

    def restart_game(self):
        self.board = []
        self.bombs_position = []

        # Start a new game
        self.create_bombs()
        self.create_board()

    def show_settings(self):
        settings = Settings()
        settings.run()


class Settings(Game):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.level_frame = tk.Frame(self.root)
        self.level_frame.pack(pady=10)
        self.custom_frame = tk.Frame(self.root)
        self.custom_frame.pack(pady=10)

        # Level options
        self.level_label = tk.Label(self.level_frame, text="Choose level:")
        self.level_label.grid(row=0, column=0, padx=5)
        self.level_var = tk.StringVar()
        self.level_var.set("easy")
        levels = ["easy", "normal", "hard"]
        for i, level in enumerate(levels):
            rb = tk.Radiobutton(self.level_frame, text=level, variable=self.level_var, value=level)
            rb.grid(row=0, column=i+1, padx=5)

        # Custom settings
        self.height_label = tk.Label(self.custom_frame, text="Height:")
        self.height_label.grid(row=1, column=0, padx=5)
        self.height_entry = tk.Entry(self.custom_frame)
        self.height_entry.grid(row=1, column=1, padx=5)

        self.width_label = tk.Label(self.custom_frame, text="Width:")
        self.width_label.grid(row=2, column=0, padx=5)
        self.width_entry = tk.Entry(self.custom_frame)
        self.width_entry.grid(row=2, column=1, padx=5)

        self.bombs_label = tk.Label(self.custom_frame, text="Bombs:")
        self.bombs_label.grid(row=3, column=0, padx=5)
        self.bombs_entry = tk.Entry(self.custom_frame)
        self.bombs_entry.grid(row=3, column=1, padx=5)

        self.ok_button = tk.Button(self.root, text="OK", command=self.on_click)
        self.ok_button.pack(pady=10)

    def on_click(self):
        try:
            if self.level_var.get() == "easy":
                rows, cols, bombs = 9, 9, 10
            elif self.level_var.get() == "normal":
                rows, cols, bombs = 16, 16, 40
            elif self.level_var.get() == "hard":
                rows, cols, bombs = 16, 30, 99
            else:
                rows = int(self.height_entry.get())
                cols = int(self.width_entry.get())
                bombs = int(self.bombs_entry.get())

            if rows <= 0 or cols <= 0 or bombs <= 0:
                raise ValueError

            self.root.destroy()
            game = Game(rows, cols, bombs)
            game.start_game()
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for height, width, and bombs.")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    game = Settings()
    game.run()
