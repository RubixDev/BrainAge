from random import randint as rn
import time

empty = ''
for line in range(100):
    empty += '\n'

tasks = []
solutions = {}
correct = 0


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


def main(shift_count, task_count):
    global correct, tasks

    # Countdown
    for second in range(3):
        print(3 - second)
        time.sleep(1)

    # Tasks before answering
    for shift in range(shift_count):
        generate()

        print(empty)
        print(tasks[-1])

        time.sleep(1.5)

    # Start timer
    t1 = time.time()

    # Tasks while answering
    for task in range(task_count - shift_count):
        generate()

        print(empty)
        print(tasks[-1])

        answer = int(input())
        if answer == solutions[tasks[-1 - shift_count]]:
            correct += 1

    # Answering without Tasks
    for shift in range(shift_count):
        print(empty)

        answer = int(input())
        if answer == solutions[tasks[-(shift_count - shift)]]:
            correct += 1

    # Stop timer
    t2 = time.time()
    time_count = t2 - t1

    # Print results
    print('\nYour time is ' + str(round(time_count, 2)) + 's')
    print('You answered ' + str(correct) + ' of ' + str(len(tasks)) + ' correct.')
    print('Score: ' + str(round(correct / len(tasks) / time_count * 1000)))

    correct = 0
    tasks = []


if __name__ == '__main__':
    while 1:
        shift_count_want = int(input('How many steps do you want the tasks to get shifted?\n'))
        task_count_want = int(input('How many tasks do you want to solve?\n'))
        print('\n---------------------------------------------------------------\n')
        main(shift_count_want, task_count_want)
        print('\n---------------------------------------------------------------\n')
