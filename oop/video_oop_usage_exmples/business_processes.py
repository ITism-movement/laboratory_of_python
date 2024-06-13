class Department:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"Employee {employee.name} added to {self.name}")

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.description}' added to {self.name}")

    def execute_tasks(self):
        print(f"{self.name} is executing its tasks:")
        for task in self.tasks:
            assigned_employee = task.assigned_to
            if assigned_employee:
                try:
                    task.perform()
                    task.status = "Completed"
                    print(f"Task '{task.description}' completed by {assigned_employee.name}")
                except Exception as e:
                    task.status = "Failed"
                    print(f"Failed to perform task '{task.description}': {str(e)}")
            else:
                print(f"No employee assigned for task '{task.description}'")
                task.status = "Pending"


class Employee:
    def __init__(self, name):
        self.name = name


class Task:
    def __init__(self, description, assigned_to=None):
        self.description = description
        self.assigned_to = assigned_to
        self.status = "Not Started"

    def perform(self):
        raise NotImplementedError("Each task must implement a perform method.")


class ReportTask(Task):
    def perform(self):
        print("Preparing and sending reports...")


class DevelopmentTask(Task):
    def perform(self):
        print("Developing new software features...")


class MarketingTask(Task):
    def perform(self):
        print("Launching a new marketing campaign...")


# Создание департаментов и сотрудников
it_department = Department("IT Department")
hr_department = Department("HR Department")
john = Employee("John")
alice = Employee("Alice")

# Назначение сотрудников в департаменты
it_department.add_employee(john)
hr_department.add_employee(alice)

# Создание и назначение задач
report_task = ReportTask("Monthly Financial Report", alice)
development_task = DevelopmentTask("New Product Development", john)
marketing_task = MarketingTask("Social Media Campaign", john)

it_department.add_task(development_task)
hr_department.add_task(report_task)
it_department.add_task(marketing_task)

# Выполнение задач
it_department.execute_tasks()
hr_department.execute_tasks()
