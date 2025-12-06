import copy

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Добавлен товар: {item}")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Удален товар: {item}")
        else:
            print("Товар не найден в корзине")

    def create_memento(self):
        return Memento(copy.deepcopy(self.items))

    def restore_from_memento(self, memento):
        self.items = memento.get_state()
        print("Состояние корзины восстановлено")

    def __str__(self):
        return f"Текущая корзина: {self.items}"


class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return copy.deepcopy(self._state)


class Caretaker:
    def __init__(self, cart):
        self.cart = cart
        self.history = []
        self.current_index = -1

    def save(self):
        # Удаляем все состояния после текущей точки (если была отмена)
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]

        memento = self.cart.create_memento()
        self.history.append(memento)
        self.current_index = len(self.history) - 1
        print("Сохранено состояние корзины")

    def undo(self):
        if self.current_index <= 0:
            print("Нет предыдущих состояний для восстановления")
            return False

        self.current_index -= 1
        memento = self.history[self.current_index]
        self.cart.restore_from_memento(memento)
        return True

    def redo(self):
        if self.current_index >= len(self.history) - 1:
            print("Нет более новых состояний для восстановления")
            return False

        self.current_index += 1
        memento = self.history[self.current_index]
        self.cart.restore_from_memento(memento)
        return True


if __name__ == "__main__":
    cart = ShoppingCart()
    caretaker = Caretaker(cart)

    caretaker.save()
    cart.add_item("Книга")
    caretaker.save()

    cart.add_item("Ручка")
    caretaker.save()

    cart.add_item("Блокнот")
    print(cart)

    caretaker.undo()
    print(cart)

    caretaker.undo()
    print(cart)

    caretaker.redo()
    print(cart)

    cart.remove_item("Книга")
    caretaker.save()
    print(cart)

    caretaker.undo()
    print(cart)

'''
1. Для хранение нескольких точек используется список (или стек) в классе Caretaker для хранения последовательности снимков (Memento). 
   Для реализации многократной отмены/повтора поддерживается указатель на текущее состояние в истории.

2. Ограничения паттерна:
   - Потребление памяти: Каждый снимок содержит полную копию состояния, что может быть ресурсоемко для больших объектов.
   - Производительность: Глубокое копирование сложных объектов может быть медленным.
   - Раскрытие внутренней структуры: Memento может нарушить инкапсуляцию, если требует доступа к приватным полям.
   - Управление временем жизни: Необходимо предусмотреть очистку истории для избежания утечек памяти.
   - Линейная история: Стандартная реализация не поддерживает ветвление состояний (как в системах контроля версий).
'''