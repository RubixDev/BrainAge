from random import randint as rn
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

empty = ''
for line in range(100):
    empty += '\n'

tasks = []
solutions = {}
correct = 0
pressed_enter = False


def generate():
    possible = False
    operation = rn(0, 1)

    first_num = 0
    second_num = 0
    task = ''
    solution = 0

    while not possible:
        first_num = rn(2, 10)
        second_num = rn(2, 10)

        if not (operation == 1 and second_num >= first_num):
            possible = True

    if operation == 0:
        solution = first_num + second_num
        task = str(first_num) + ' + ' + str(second_num)
    elif operation == 1:
        solution = first_num - second_num
        task = str(first_num) + ' - ' + str(second_num)

    tasks.append(task)
    solutions[task] = solution


def window(height=300, width=550):
    root = tk.Tk()
    root.resizable(False, False)
    root.title('BrainAge')
    root.iconbitmap(default='BrainAge.ico')
    ttk.Style().theme_use('vista')

    def start_main():
        global correct, tasks
        correct = 0
        tasks = []
        threading.Thread(target=lambda: main(int(shift_combobox.get()), int(tasks_combobox.get()))).start()

    def main(shift_count, task_count):
        global correct, pressed_enter

        current_task_label.config(state='normal')

        # Countdown
        for second in range(3):
            current_task_label.config(text=str(3 - second))
            time.sleep(1)

        # Tasks before answering
        for shift in range(shift_count):
            generate()

            current_task_label.config(text=tasks[-1])

            time.sleep(1.5)
        answer_entry.config(state='normal')
        answer_entry.focus()

        # Start timer
        t1 = time.time()

        # Tasks while answering
        for task in range(task_count - shift_count):
            generate()

            current_task_label.config(text=tasks[-1])

            while 1:
                if pressed_enter:
                    answer = int(answer_entry.get())
                    break
            pressed_enter = False
            answer_entry.delete(0, 'end')

            if answer == solutions[tasks[-1 - shift_count]]:
                correct += 1

            progress['value'] = (len(tasks) - shift_count) / int(tasks_combobox.get()) * 100

        # Answering without Tasks
        for shift in range(shift_count):
            current_task_label.config(text='')
            while 1:
                if pressed_enter:
                    answer = int(answer_entry.get())
                    break
            pressed_enter = False
            answer_entry.delete(0, 'end')

            if answer == solutions[tasks[-(shift_count - shift)]]:
                correct += 1

            progress['value'] = (len(tasks) - (shift_count - (shift + 1))) / int(tasks_combobox.get()) * 100

        # Stop timer
        t2 = time.time()
        time_count = t2 - t1

        # Print results
        current_task_label.config(text='')
        messagebox.showinfo('Congratulations!', 'Your time is ' + str(round(time_count, 2)) + 's\n'
                            'You answered ' + str(correct) + ' of ' + str(len(tasks)) + ' correct.\n\n'
                            'Score: ' + str(round(correct / len(tasks) / time_count * 1000) * (len(tasks) / 4)))

        current_task_label.config(state='disabled')
        answer_entry.config(state='disabled')
        progress['value'] = 0
        play_button.focus()

    def enter_func(_):
        global pressed_enter
        pressed_enter = True

    # window settings
    canvas = tk.Canvas(root, height=height, width=width)
    canvas.pack()

    frame = tk.Frame(root, bd=15)
    frame.place(relheight=1, relwidth=1)

    # Settings
    shift_label = ttk.Label(frame, text='Shift Amount:')
    shift_label.grid(column=0, row=0, pady=15, sticky='E')

    shift_combobox = ttk.Combobox(frame, state='readonly', values=[0, 1, 2, 3, 4, 5])
    shift_combobox.grid(column=1, row=0, padx=10, pady=15, sticky='W')
    shift_combobox.current(1)

    tasks_label = ttk.Label(frame, text='Amount of tasks:')
    tasks_label.grid(column=2, row=0, padx=10, pady=15, sticky='E')

    tasks_combobox = ttk.Combobox(frame, state='readonly', values=[5, 10, 15, 20, 50, 100])
    tasks_combobox.grid(column=3, row=0, pady=15, sticky='W')
    tasks_combobox.current(3)

    # Play button
    play_button = ttk.Button(frame, text='Play', command=start_main)
    play_button.grid(column=0, row=1, pady=20, ipadx=20, columnspan=4)
    play_button.focus()

    # Game
    current_task_label = ttk.Label(frame, state='disabled', font=("Courier", 30))
    current_task_label.grid(column=0, columnspan=2, row=2, rowspan=2, pady=30)

    answer_entry = ttk.Entry(frame, state='disabled')
    answer_entry.grid(column=2, row=2, columnspan=2, ipadx=30, pady=30)
    answer_entry.bind('<Return>', enter_func)

    progress = ttk.Progressbar(frame, length=100, mode='determinate')
    progress.grid(column=2, row=3, columnspan=2, ipadx=42)

    root.mainloop()


if __name__ == '__main__':
    window()
