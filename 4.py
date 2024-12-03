def add_task(todo_list, task):
    todo_list.append(task)
    print(f"Task '{task}' added.")

def view_tasks(todo_list):
    if not todo_list:
        print("No tasks.")
    else:
        for i, task in enumerate(todo_list, 1):
            print(f"{i}. {task}")

def remove_task(todo_list, task_number):
    try:
        task = todo_list.pop(task_number - 1)
        print(f"Task '{task}' removed.")
    except IndexError:
        print("Invalid task number.")

if __name__ == "__main__":
    todo_list = []
    while True:
        print("\nOptions: [1] Add Task [2] View Tasks [3] Remove Task [4] Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            task = input("Enter a task: ")
            add_task(todo_list, task)
        elif choice == "2":
            view_tasks(todo_list)
        elif choice == "3":
            task_number = int(input("Enter the task number to remove: "))
            remove_task(todo_list, task_number)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")