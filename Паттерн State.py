from abc import ABC, abstractmethod


# Абстрактный класс состояния заказа
class OrderState(ABC):
    @abstractmethod
    def process_order(self, order) -> 'OrderState':
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    def can_transition_to(self, new_state: str) -> bool:
        """Проверяет, возможен ли переход в указанное состояние"""
        valid_transitions = self._get_valid_transitions()
        return new_state in valid_transitions

    @abstractmethod
    def _get_valid_transitions(self) -> list:
        """Возвращает список допустимых переходов из текущего состояния"""
        pass


# Конкретные состояния заказа
class NewState(OrderState):
    def process_order(self, order) -> OrderState:
        print("Обработка нового заказа: проверка наличия товаров")
        return ProcessingState()

    def get_status(self) -> str:
        return "Новый"

    def _get_valid_transitions(self) -> list:
        return ["В обработке", "Отменен"]


class ProcessingState(OrderState):
    def process_order(self, order) -> OrderState:
        print("Обработка заказа: подтверждение платежа и сборка")
        return ShippedState()

    def get_status(self) -> str:
        return "В обработке"

    def _get_valid_transitions(self) -> list:
        return ["Отправлен", "Отменен"]


class ShippedState(OrderState):
    def process_order(self, order) -> OrderState:
        print("Заказ отправлен: отслеживание доставки")
        return DeliveredState()

    def get_status(self) -> str:
        return "Отправлен"

    def _get_valid_transitions(self) -> list:
        return ["Доставлен"]


class DeliveredState(OrderState):
    def process_order(self, order) -> OrderState:
        print("Заказ уже доставлен. Дальнейшая обработка невозможна")
        return self

    def get_status(self) -> str:
        return "Доставлен"

    def _get_valid_transitions(self) -> list:
        return []  # Нет допустимых переходов из доставленного состояния


class CancelledState(OrderState):
    def process_order(self, order) -> OrderState:
        print("Заказ отменен. Обработка невозможна")
        return self

    def get_status(self) -> str:
        return "Отменен"

    def _get_valid_transitions(self) -> list:
        return []  # Нет допустимых переходов из отмененного состояния


# Класс заказа
class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self._state: OrderState = NewState()
        self._state_history = [self._state.get_status()]

    def process_order(self):
        """Обрабатывает заказ, переходя к следующему состоянию"""
        print(f"\n--- Обработка заказа #{self.order_id} ---")
        print(f"Текущий статус: {self.get_status()}")

        new_state = self._state.process_order(self)

        if self._validate_transition(new_state):
            old_status = self._state.get_status()
            self._state = new_state
            new_status = self._state.get_status()

            self._state_history.append(new_status)
            print(f"Статус изменен: {old_status} -> {new_status}")
        else:
            print(f"Недопустимый переход: {self._state.get_status()} -> {new_state.get_status()}")

    def get_status(self) -> str:
        return self._state.get_status()

    def get_state_history(self) -> list:
        return self._state_history.copy()

    def set_state(self, new_state: OrderState):
        """Прямая установка состояния с проверкой корректности перехода"""
        if self._validate_transition(new_state):
            old_status = self._state.get_status()
            self._state = new_state
            new_status = self._state.get_status()

            self._state_history.append(new_status)
            print(f"Статус изменен: {old_status} -> {new_status}")
        else:
            print(f"Недопустимый переход: {self._state.get_status()} -> {new_state.get_status()}")

    def cancel_order(self):
        """Отмена заказа"""
        if self._state.can_transition_to("Отменен"):
            self._state = CancelledState()
            self._state_history.append("Отменен")
            print("Заказ отменен")
        else:
            print(f"Невозможно отменить заказ в статусе: {self.get_status()}")

    def _validate_transition(self, new_state: OrderState) -> bool:
        """Проверяет корректность перехода в новое состояние"""
        current_status = self._state.get_status()
        new_status = new_state.get_status()

        # Не проверяем переход, если состояние не изменилось
        if current_status == new_status:
            return True

        return self._state.can_transition_to(new_status)


# Демонстрация работы
if __name__ == "__main__":
    # Создаем заказ
    order = Order("12345")

    print("=== Демонстрация паттерна State для управления заказом ===")

    # Обрабатываем заказ по стандартному workflow
    order.process_order()  # Новый -> В обработке
    order.process_order()  # В обработке -> Отправлен
    order.process_order()  # Отправлен -> Доставлен

    # Пытаемся обработать доставленный заказ
    order.process_order()  # Доставлен -> Доставлен (не меняется)

    print(f"\nИстория статусов: {order.get_state_history()}")

    # Создаем другой заказ и пробуем отменить
    print("\n--- Другой заказ с отменой ---")
    order2 = Order("67890")
    order2.process_order()  # Новый -> В обработке
    order2.cancel_order()  # В обработке -> Отменен

    # Пытаемся обработать отмененный заказ
    order2.process_order()  # Отменен -> Отменен (не меняется)

    print(f"\nИстория статусов: {order2.get_state_history()}")

"""
Обеспечение корректности переходов:

1. Метод _get_valid_transitions() в каждом состоянии определяет допустимые переходы
2. Метод can_transition_to() проверяет возможность перехода в указанное состояние
3. Метод _validate_transition() проверяет корректность перехода перед его выполнением
4. Запрещенные переходы блокируются с выводом сообщения об ошибке

Дополнительные методы для управления состояниями:

1. set_state() - прямая установка состояния с проверкой корректности
2. cancel_order() - специализированный метод для отмены заказа
3. get_state_history() - получение истории изменений состояния
4. _validate_transition() - внутренняя проверка валидности перехода
"""