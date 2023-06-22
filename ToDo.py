from datetime import datetime

class Task:
    def __init__(self, name, deadline, priority):
        self.name = name
        self.deadline = deadline
        self.priority = priority
        self.completed = False

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def complete_task(self, task):
        task.completed = True

    def sort_by_deadline(self):
        self.tasks.sort(key=lambda x: x.deadline)

    def sort_by_priority(self):
        self.tasks.sort(key=lambda x: x.priority, reverse=True)

    def print_tasks(self):
        if not self.tasks:
            print("タスクはありません。")
        else:
            for i, task in enumerate(self.tasks):
                status = "済" if task.completed else "未"
                print(f"{i+1}. [{status}] {task.name} - 期限: {task.deadline}, 優先度: {task.priority}")

def save_tasks(todo_list, filename):
    with open(filename, "w") as file:
        for task in todo_list.tasks:
            status = "1" if task.completed else "0"
            file.write(f"{status},{task.name},{task.deadline},{task.priority}\n")

def load_tasks(filename):
    todo_list = ToDoList()
    try:
        with open(filename, "r") as file:
            for line in file:
                status, name, deadline_str, priority = line.strip().split(",")
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                except ValueError:
                    print(f"無効な入力です: {deadline_str}。タスクをスキップします。")
                    continue
                task = Task(name, deadline, int(priority))
                if status == "1":
                    task.completed = True
                todo_list.add_task(task)
    except FileNotFoundError:
        pass
    return todo_list

filename = "tasks.txt"
todo_list = load_tasks(filename)

while True:
    print("==== タスク管理プログラム ====")
    print("1. タスクを追加する")
    print("2. タスクを削除する")
    print("3. タスクを完了する")
    print("4. タスクを表示する")
    print("5. タスクを期限順に並べ替える")
    print("6. タスクを優先度順に並べ替える")
    print("0. プログラムを終了する")

    choice = input("選択肢を入力してください: ")

    if choice == "1":
        name = input("タスク名を入力してください: ")
        deadline_str = input("期限を入力してください (YYYY-MM-DD形式): ")
        priority = int(input("優先度を入力してください (0から9の範囲で): "))

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            print("無効な入力です。正しい日付形式で入力してください。")
            continue

        task = Task(name, deadline, priority)
        todo_list.add_task(task)
        print("タスクを追加しました。")

    elif choice == "2":
        todo_list.print_tasks()
        if todo_list.tasks:
            try:
                index = int(input("削除するタスクの番号を入力してください: ")) - 1
                task = todo_list.tasks[index]
                todo_list.remove_task(task)
                print("タスクを削除しました。")
            except (IndexError, ValueError):
                print("無効な入力です。正しい番号を入力してください。")
        else:
            print("削除するタスクはありません。")

    elif choice == "3":
        todo_list.print_tasks()
        if todo_list.tasks:
            try:
                index = int(input("完了したタスクの番号を入力してください: ")) - 1
                task = todo_list.tasks[index]
                todo_list.complete_task(task)
                print("タスクを完了しました。")
            except (IndexError, ValueError):
                print("無効な入力です。正しい番号を入力してください。")
        else:
            print("完了するタスクはありません。")

    elif choice == "4":
        if todo_list.tasks:
            todo_list.print_tasks()
        else:
            print("表示するタスクはありません。")

    elif choice == "5":
        todo_list.sort_by_deadline()
        print("タスクを期限順に並べ替えました。")

    elif choice == "6":
        todo_list.sort_by_priority()
        print("タスクを優先度順に並べ替えました。")

    elif choice == "0":
        save_tasks(todo_list, filename)
        print("プログラムを終了します。")
        break

    else:
        print("無効な選択肢です。正しい選択肢を入力してください。")
