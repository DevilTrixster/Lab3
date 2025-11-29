from abc import ABC, abstractmethod
from typing import List


# Абстрактный класс наблюдателя
class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int, status: str):
        pass


# Конкретные наблюдатели
class ClientNotification(Observer):
    def update(self, order_id: int, status: str):
        print(f"Уведомление клиенту: Заказ #{order_id} - статус: {status}")


class ManagerNotification(Observer):
    def update(self, order_id: int, status: str):
        print(f"Уведомление менеджеру: Заказ #{order_id} - статус: {status}")


class AnalyticsSystem(Observer):
    def update(self, order_id: int, status: str):
        print(f"Аналитическая система: Заказ #{order_id} - новый статус: {status}")


# Класс заказа (Subject)
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
        old_status = self._status
        self._status = new_status
        print(f"Заказ #{self.order_id}: {old_status} -> {new_status}")
        self.notify_observers()

    def get_status(self):
        return self._status


# Демонстрация работы
if __name__ == "__main__":
    # Создаем заказ
    order = Order(12345)

    # Создаем наблюдателей
    client_notification = ClientNotification()
    manager_notification = ManagerNotification()
    analytics_system = AnalyticsSystem()

    # Подписываем наблюдателей на заказ
    order.add_observer(client_notification)
    order.add_observer(manager_notification)
    order.add_observer(analytics_system)

    # Меняем статусы заказа
    order.set_status("В обработке")
    order.set_status("Отправлен")

    # Отписываем менеджера от уведомлений
    order.remove_observer(manager_notification)

    order.set_status("Доставлен")

"""
Вопрос: Есть ли необходимость добавления дополнительных классов или методов для обеспечения безопасности? Почему?

Ответ: Да, для обеспечения безопасности рекомендуется добавить:

1. Валидацию данных:
   - Проверка корректности статусов заказа
   - Валидация order_id на положительное число

2. Контроль доступа:
   - Аутентификация наблюдателей перед подпиской
   - Авторизация для определенных типов уведомлений

3. Защита от злоупотреблений:
   - Ограничение частоты уведомлений
   - Проверка на циклические вызовы

4. Безопасность данных:
   - Шифрование конфиденциальной информации в уведомлениях
   - Логирование изменений статусов для аудита

5. Обработка ошибок:
   - try-catch блоки при уведомлении наблюдателей
   - Механизм повторных попыток при сбоях

Пример дополнительных мер безопасности:

class SecureOrder(Order):
    VALID_STATUSES = {"Оформлен", "В обработке", "Отправлен", "Доставлен", "Отменен"}

    def set_status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Недопустимый статус: {new_status}")

        # Логирование изменения статуса
        self._log_status_change(new_status)
        super().set_status(new_status)

    def _log_status_change(self, new_status: str):
        # Логирование для аудита
        print(f"[AUDIT] Order #{self.order_id} status changed to: {new_status}")
"""