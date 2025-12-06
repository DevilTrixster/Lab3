from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int, status: str):
        pass

class ClientNotification(Observer):
    def update(self, order_id: int, status: str):
        print(f"Клиент: Заказ #{order_id} сменил статус на '{status}'")


class ManagerNotification(Observer):
    def update(self, order_id: int, status: str):
        print(f"Менеджер: Заказ #{order_id} сменил статус на '{status}'")


class AnalyticsSystem(Observer):
    def update(self, order_id: int, status: str):
        print(f"Аналитика: Заказ #{order_id} -> статус '{status}'")

class Order:
    def __init__(self, order_id: int):
        self.order_id = order_id
        self._status = "Оформлен"
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self.order_id, self._status)

    def set_status(self, new_status: str):
        valid_statuses = ["Оформлен", "В обработке", "Отправлен", "Доставлен"]
        if new_status in valid_statuses:
            self._status = new_status
            self.notify_observers()
        else:
            raise ValueError(f"Недопустимый статус. Допустимые: {valid_statuses}")

if __name__ == "__main__":
    order = Order(12345)

    client = ClientNotification()
    manager = ManagerNotification()
    analytics = AnalyticsSystem()

    order.add_observer(client)
    order.add_observer(manager)
    order.add_observer(analytics)

    order.set_status("В обработке")
    order.set_status("Отправлен")

    order.remove_observer(manager)
    order.set_status("Доставлен")

'''Да, для обеспечения безопасности рекомендуется:
1. Добавить валидацию статусов (реализовано) для предотвращения некорректных состояний.
2. Инкапсулировать список наблюдателей (сделать приватным) и методы работы с ним.
3. Реализовать проверку прав доступа при добавлении/удалении наблюдателей.
4. Использовать шифрование при передаче уведомлений вне системы.
5. Ввести аутентификацию наблюдателей при подписке.
Это предотвратит несанкционированный доступ, подмену статусов и утечку данных.'''