# Task Management System 
# in memory storage for task 
tasks = []

# add task
def add_task():
    task = input("Enter the task description: ")
    task.append(task)
    print(f"Task '{task} added successfully!")
# view all tasks
def view_tasks():
    if not tasks:
        print("No tasks available.")
    else:
        print("Your tasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")
# update a task
def update_task():
    view_tasks()
    try:
        task_number = int(input("Enter the task number to update: "))
        if 1 <= task_number <= len(tasks):
            new_task = input("Enter the new task description: ")
            tasks[task_number - 1] = new_task
            print(f"Task {task_number} updated successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# delete a task
def delete_task():
    view_tasks()
    try:
        task_number = int(input("Enter the task number to delete: "))
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            print(f"Task '{removed_task}' deleted successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Main menu
def main():
    while True:
        print("\nTask Management System")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Exiting Task Management System. See you soon!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()