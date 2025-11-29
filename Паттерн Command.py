from abc import ABC, abstractmethod
from typing import List


# Абстрактный класс команды
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# Конкретные команды
class MoveUpCommand(Command):
    def __init__(self, lift_control):
        self.lift_control = lift_control
        self.previous_floor = 0

    def execute(self):
        self.previous_floor = self.lift_control.current_floor
        self.lift_control.move_up()

    def undo(self):
        self.lift_control.current_floor = self.previous_floor
        print(f"Отмена: лифт возвращен на {self.previous_floor} этаж")


class MoveDownCommand(Command):
    def __init__(self, lift_control):
        self.lift_control = lift_control
        self.previous_floor = 0

    def execute(self):
        self.previous_floor = self.lift_control.current_floor
        self.lift_control.move_down()

    def undo(self):
        self.lift_control.current_floor = self.previous_floor
        print(f"Отмена: лифт возвращен на {self.previous_floor} этаж")


class OpenDoorCommand(Command):
    def __init__(self, lift_control):
        self.lift_control = lift_control
        self.previous_state = False

    def execute(self):
        self.previous_state = self.lift_control.door_open
        self.lift_control.open_door()

    def undo(self):
        if self.previous_state == False:
            self.lift_control.close_door()
            print("Отмена: дверь закрыта")


class CloseDoorCommand(Command):
    def __init__(self, lift_control):
        self.lift_control = lift_control
        self.previous_state = False

    def execute(self):
        self.previous_state = self.lift_control.door_open
        self.lift_control.close_door()

    def undo(self):
        if self.previous_state == True:
            self.lift_control.open_door()
            print("Отмена: дверь открыта")


# Класс для хранения истории команд
class CommandHistory:
    def __init__(self):
        self.history: List[Command] = []

    def push(self, command: Command):
        self.history.append(command)

    def pop(self) -> Command:
        if self.history:
            return self.history.pop()
        return None

    def is_empty(self) -> bool:
        return len(self.history) == 0

    def get_history_size(self) -> int:
        return len(self.history)


# Контроллер лифта
class LiftControl:
    def __init__(self):
        self.current_floor = 1
        self.door_open = False
        self.max_floor = 10
        self.history = CommandHistory()

    def move_up(self):
        if self.current_floor < self.max_floor:
            self.current_floor += 1
            print(f"Лифт поднялся на {self.current_floor} этаж")
        else:
            print("Достигнут максимальный этаж")

    def move_down(self):
        if self.current_floor > 1:
            self.current_floor -= 1
            print(f"Лифт опустился на {self.current_floor} этаж")
        else:
            print("Достигнут минимальный этаж")

    def open_door(self):
        if not self.door_open:
            self.door_open = True
            print("Дверь открыта")
        else:
            print("Дверь уже открыта")

    def close_door(self):
        if self.door_open:
            self.door_open = False
            print("Дверь закрыта")
        else:
            print("Дверь уже закрыта")

    def execute_command(self, command: Command):
        command.execute()
        self.history.push(command)

    def undo_last_command(self):
        if not self.history.is_empty():
            command = self.history.pop()
            command.undo()
        else:
            print("История команд пуста")

    def undo_multiple_commands(self, count: int):
        actual_count = min(count, self.history.get_history_size())
        print(f"Отмена {actual_count} последних команд:")

        for i in range(actual_count):
            self.undo_last_command()

    def get_status(self):
        door_status = "открыта" if self.door_open else "закрыта"
        return f"Текущий этаж: {self.current_floor}, Дверь: {door_status}"


# Демонстрация работы
if __name__ == "__main__":
    lift = LiftControl()

    print("=== Демонстрация паттерна Command для управления лифтом ===\n")

    # Выполняем команды
    lift.execute_command(MoveUpCommand(lift))
    lift.execute_command(MoveUpCommand(lift))
    lift.execute_command(OpenDoorCommand(lift))
    lift.execute_command(CloseDoorCommand(lift))
    lift.execute_command(MoveDownCommand(lift))

    print(f"\nТекущее состояние: {lift.get_status()}")

    # Отменяем несколько команд
    lift.undo_multiple_commands(3)

    print(f"\nПосле отмены: {lift.get_status()}")

"""
Вопрос: Как вы реализуете отмену нескольких последних команд? Какие ограничения могут возникнуть в вашей системе?

Ответ:

Реализация отмены нескольких команд:
1. В классе CommandHistory храним полную историю выполненных команд
2. Метод undo_multiple_commands(count) отменяет указанное количество последних команд
3. Каждая команда должна сохранять состояние для возможности отмены

Ограничения системы:
1. Потребление памяти: хранение полной истории может требовать много памяти
2. Сложность отмены составных операций: некоторые команды могут зависеть друг от друга
3. Ограничение глубины отмены: при большом количестве команд может потребоваться ограничение истории
4. Невозможность отмены физических действий: реальное движение лифта нельзя "отменить", только компенсировать
5. Проблемы с состоянием: если между командами изменились внешние условия, отмена может привести к некорректному состоянию

Дополнительные улучшения:
- Ограничение максимального размера истории
- Группировка команд в макрокоманды
- Проверка возможности отмены перед выполнением
- Система повтора (redo) для отмененных команд
"""