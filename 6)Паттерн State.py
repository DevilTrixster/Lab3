from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def process_order(self, order):
        pass

    @abstractmethod
    def get_status(self):
        pass


class NewState(OrderState):

    def process_order(self, order):
        order.set_state(ProcessingState())
        print("Заказ переведен в состояние: В обработке")

    def get_status(self):
        return "Новый"


class ProcessingState(OrderState):

    def process_order(self, order):
        order.set_state(ShippedState())
        print("Заказ переведен в состояние: Отправлен")

    def get_status(self):
        return "В обработке"


class ShippedState(OrderState):

    def process_order(self, order):
        order.set_state(DeliveredState())
        print("Заказ переведен в состояние: Доставлен")

    def get_status(self):
        return "Отправлен"


class DeliveredState(OrderState):
    def process_order(self, order):
        print("Заказ уже доставлен. Дальнейшие изменения невозможны")

    def get_status(self):
        return "Доставлен"


class CancelledState(OrderState):
    def process_order(self, order):
        print("Заказ отменен. Дальнейшие изменения невозможны")

    def get_status(self):
        return "Отменен"


class Order:
    def __init__(self):
        self._state = NewState()

    def set_state(self, state):
        """Метод для изменения состояния заказа"""
        self._state = state

    def process_order(self):
        """Обработать заказ (перевести в следующее состояние)"""
        self._state.process_order(self)

    def cancel_order(self):
        """Метод для отмены заказа (доступен не из всех состояний)"""
        if isinstance(self._state, (NewState, ProcessingState)):
            self._state = CancelledState()
            print("Заказ отменен")
        elif isinstance(self._state, (DeliveredState, CancelledState)):
            print(f"Невозможно отменить заказ в состоянии '{self._state.get_status()}'")
        else:
            print("Отмена возможна только для заказов в состояниях 'Новый' или 'В обработке'")

    def get_status(self):
        """Получить текущий статус заказа"""
        return self._state.get_status()


if __name__ == "__main__":
    order = Order()
    print(f"Текущий статус: {order.get_status()}")

    order.process_order()  # Новый → В обработке
    print(f"Текущий статус: {order.get_status()}")

    order.process_order()  # В обработке → Отправлен
    print(f"Текущий статус: {order.get_status()}")

    order.process_order()  # Отправлен → Доставлен
    print(f"Текущий статус: {order.get_status()}")

    order.process_order()  # Попытка изменить доставленный заказ
    order.cancel_order()  # Попытка отменить доставленный заказ

    print("\n--- Пример с отменой ---")
    order2 = Order()
    print(f"Текущий статус: {order2.get_status()}")

    order2.cancel_order()  # Отмена нового заказа
    print(f"Текущий статус: {order2.get_status()}")

    order2.process_order()  # Попытка изменить отмененный заказ

    '''
    Корректность переходов между состояниями обеспечивается следующими способами:

    1. Логика переходов инкапсулирована в самих классах состояний. Каждый класс состояния
       определяет, в какое следующее состояние можно перейти, предотвращая недопустимые переходы.

    2. Метод process_order() в конечных состояниях (DeliveredState, CancelledState)
       блокирует дальнейшие изменения, выводя сообщение об ошибке.

    3. Добавлены специальные методы для управления состояниями:
       - set_state() - для установки конкретного состояния (используется классами состояний)
       - cancel_order() - для отмены заказа с проверкой допустимости из текущего состояния
       - process_order() - для перехода к следующему состоянию по workflow
       - get_status() - для получения текущего статуса

    4. Конечные состояния не содержат логики перехода в другие состояния, что делает
       переходы из них невозможными.

    Для предотвращения перехода из "Доставлен" в "В обработке":
    - DeliveredState.process_order() не вызывает order.set_state(), а только выводит сообщение
    - Нет других механизмов изменения состояния из DeliveredState
    '''