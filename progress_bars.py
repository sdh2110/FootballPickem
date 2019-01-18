from dataclasses import dataclass


MAX_TITLE_WIDTH = 16
STANDARD_WIDTH = 30


@dataclass
class ProgressBar:
    __slots__ = "title", "width", "tasks", "completed"
    title: str
    tasks: int
    width: int
    completed: int

    def __init__(self, title, tasks, width = STANDARD_WIDTH, completed = 0):
        self.title = '\r' + title + ": " + (MAX_TITLE_WIDTH - len(title)) * ' '
        self.width = width
        self.tasks = tasks
        self.completed = completed
        self.update()


    def update(self):
        percent = self.completed / self.tasks
        progress = int(self.width * percent)
        print(self.title, \
              progress * '#', (self.width - progress) * '.', \
              ' ', int(percent * 100), end = '%', sep = "")
        if self.completed == self.tasks:
            print()


    def complete_task(self, progress = 1):
        if self.completed != self.tasks:
            self.completed += progress
            self.update()