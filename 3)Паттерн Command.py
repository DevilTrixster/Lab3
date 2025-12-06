from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class MoveUpCommand(Command):
    def __init__(self, lift):
        self.lift = lift
        self.previous_floor = None

    def execute(self):
        self.previous_floor = self.lift.current_floor
        self.lift.move_up()
        print(f"Лифт поднялся на этаж {self.lift.current_floor}")

    def undo(self):
        if self.previous_floor is not None:
            self.lift.current_floor = self.previous_floor
            print(f"Отмена: лифт вернулся на этаж {self.lift.current_floor}")


class MoveDownCommand(Command):
    def __init__(self, lift):
        self.lift = lift
        self.previous_floor = None

    def execute(self):
        self.previous_floor = self.lift.current_floor
        self.lift.move_down()
        print(f"Лифт опустился на этаж {self.lift.current_floor}")

    def undo(self):
        if self.previous_floor is not None:
            self.lift.current_floor = self.previous_floor
            print(f"Отмена: лифт вернулся на этаж {self.lift.current_floor}")


class OpenDoorCommand(Command):
    def __init__(self, lift):
        self.lift = lift
        self.was_open = None

    def execute(self):
        self.was_open = self.lift.door_open
        self.lift.open_door()
        print("Двери открыты")

    def undo(self):
        if self.was_open is not None and not self.was_open:
            self.lift.door_open = False
            print("Отмена: двери закрыты")


class CloseDoorCommand(Command):
    def __init__(self, lift):
        self.lift = lift
        self.was_open = None

    def execute(self):
        self.was_open = self.lift.door_open
        self.lift.close_door()
        print("Двери закрыты")

    def undo(self):
        if self.was_open is not None and self.was_open:
            self.lift.door_open = True
            print("Отмена: двери открыты")

class Lift:
    def __init__(self):
        self.current_floor = 1
        self.door_open = False
        self.max_floor = 10

    def move_up(self):
        if not self.door_open and self.current_floor < self.max_floor:
            self.current_floor += 1
            return True
        return False

    def move_down(self):
        if not self.door_open and self.current_floor > 1:
            self.current_floor -= 1
            return True
        return False

    def open_door(self):
        self.door_open = True
        return True

    def close_door(self):
        self.door_open = False
        return True

class CommandHistory:
    def __init__(self):
        self.history = []

    def push(self, command):
        self.history.append(command)

    def pop(self):
        if self.history:
            return self.history.pop()
        return None

    def undo_last(self):
        command = self.pop()
        if command:
            command.undo()

    def undo_last_n(self, n):
        for _ in range(min(n, len(self.history))):
            self.undo_last()

class LiftControl:
    def __init__(self):
        self.lift = Lift()
        self.history = CommandHistory()

    def execute_command(self, command):
        command.execute()
        self.history.push(command)


if __name__ == "__main__":
    controller = LiftControl()

    print("--- Выполнение команд ---")
    controller.execute_command(CloseDoorCommand(controller.lift))
    controller.execute_command(MoveUpCommand(controller.lift))
    controller.execute_command(MoveUpCommand(controller.lift))
    controller.execute_command(OpenDoorCommand(controller.lift))

    print("\n--- Отмена последней команды ---")
    controller.history.undo_last()

    print("\n--- Отмена 2 последних команд ---")
    controller.history.undo_last_n(2)

'''Для отмены нескольких последних команд реализован метод undo_last_n(n) в CommandHistory, 
который последовательно вызывает undo() для n последних команд из стека истории.

Ограничения системы:
1. Невозможность отмены некоторых команд без выполнения обратных действий (например, отмена движения требует знания предыдущего этажа)
2. Ограниченная память для хранения истории команд
3. Потенциальная неконсистентность состояния при отмене команд в неправильном порядке
4. Зависимость команд от текущего состояния системы (некоторые команды могут быть невыполнимы в определенных состояниях)'''