from abc import ABC, abstractmethod
from typing import Dict, Any, List
import datetime


# Абстрактный класс посредника
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str, data: Dict[str, Any] = None):
        pass


# Абстрактный класс компонента
class BaseComponent(ABC):
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator):
        self._mediator = mediator

    def send(self, event: str, data: Dict[str, Any] = None):
        if self._mediator:
            self._mediator.notify(self, event, data)


# Конкретные компоненты системы
class Client(BaseComponent):
    def __init__(self, client_id: str, name: str, mediator: Mediator = None):
        super().__init__(mediator)
        self.client_id = client_id
        self.name = name
        self.order_history = []

    def place_order(self, order_details: Dict[str, Any]):
        print(f"Клиент {self.name} размещает заказ: {order_details}")
        self.send("order_placed", {
            "client_id": self.client_id,
            "client_name": self.name,
            "order_details": order_details,
            "timestamp": datetime.datetime.now()
        })

    def cancel_order(self, order_id: str):
        print(f"Клиент {self.name} отменяет заказ: {order_id}")
        self.send("order_cancelled", {
            "client_id": self.client_id,
            "order_id": order_id,
            "timestamp": datetime.datetime.now()
        })

    def receive_notification(self, message: str):
        print(f"Уведомление для клиента {self.name}: {message}")
        # В реальной системе здесь могла бы быть отправка email/SMS

    def handle_event(self, event: str, data: Dict[str, Any]):
        if event == "order_processed":
            self.order_history.append(data["order_id"])
            self.receive_notification(f"Ваш заказ {data['order_id']} обработан менеджером")
        elif event == "order_shipped":
            self.receive_notification(f"Ваш заказ {data['order_id']} отправлен со склада")
        elif event == "order_delivered":
            self.receive_notification(f"Ваш заказ {data['order_id']} доставлен")


class Manager(BaseComponent):
    def __init__(self, manager_id: str, name: str, mediator: Mediator = None):
        super().__init__(mediator)
        self.manager_id = manager_id
        self.name = name
        self.pending_orders = []

    def process_order(self, order_id: str):
        print(f"Менеджер {self.name} обрабатывает заказ: {order_id}")
        if order_id in self.pending_orders:
            self.pending_orders.remove(order_id)

        self.send("order_processed", {
            "manager_id": self.manager_id,
            "order_id": order_id,
            "timestamp": datetime.datetime.now()
        })

    def reject_order(self, order_id: str, reason: str):
        print(f"Менеджер {self.name} отклоняет заказ: {order_id}. Причина: {reason}")
        if order_id in self.pending_orders:
            self.pending_orders.remove(order_id)

        self.send("order_rejected", {
            "manager_id": self.manager_id,
            "order_id": order_id,
            "reason": reason,
            "timestamp": datetime.datetime.now()
        })

    def handle_event(self, event: str, data: Dict[str, Any]):
        if event == "order_placed":
            order_id = data["order_details"].get("order_id", "unknown")
            self.pending_orders.append(order_id)
            print(f"Менеджер {self.name}: получен новый заказ {order_id}")


class Warehouse(BaseComponent):
    def __init__(self, warehouse_id: str, location: str, mediator: Mediator = None):
        super().__init__(mediator)
        self.warehouse_id = warehouse_id
        self.location = location
        self.inventory = {}
        self.shipped_orders = []

    def check_inventory(self, product_id: str, quantity: int) -> bool:
        return self.inventory.get(product_id, 0) >= quantity

    def reserve_items(self, order_id: str, items: List[Dict[str, Any]]) -> bool:
        # Проверяем наличие всех товаров
        for item in items:
            if not self.check_inventory(item["product_id"], item["quantity"]):
                return False

        # Резервируем товары
        for item in items:
            self.inventory[item["product_id"]] -= item["quantity"]

        print(f"Склад {self.location}: товары зарезервированы для заказа {order_id}")
        return True

    def ship_order(self, order_id: str):
        print(f"Склад {self.location}: отправляет заказ {order_id}")
        self.shipped_orders.append(order_id)

        self.send("order_shipped", {
            "warehouse_id": self.warehouse_id,
            "order_id": order_id,
            "timestamp": datetime.datetime.now()
        })

    def handle_event(self, event: str, data: Dict[str, Any]):
        if event == "order_processed":
            order_id = data["order_id"]
            # В реальной системе здесь была бы логика получения деталей заказа
            items = [{"product_id": "prod1", "quantity": 2}]  # Пример

            if self.reserve_items(order_id, items):
                self.ship_order(order_id)
            else:
                self.send("insufficient_inventory", {
                    "warehouse_id": self.warehouse_id,
                    "order_id": order_id,
                    "timestamp": datetime.datetime.now()
                })


# Конкретный посредник
class OrderMediator(Mediator):
    def __init__(self):
        self.clients: Dict[str, Client] = {}
        self.managers: Dict[str, Manager] = {}
        self.warehouses: Dict[str, Warehouse] = {}
        self.security_log = []

    def register_client(self, client: Client):
        self.clients[client.client_id] = client
        client.mediator = self

    def register_manager(self, manager: Manager):
        self.managers[manager.manager_id] = manager
        manager.mediator = self

    def register_warehouse(self, warehouse: Warehouse):
        self.warehouses[warehouse.warehouse_id] = warehouse
        warehouse.mediator = self

    def _log_security_event(self, event: str, sender: object, data: Dict[str, Any]):
        log_entry = {
            "timestamp": datetime.datetime.now(),
            "event": event,
            "sender_type": sender.__class__.__name__,
            "data": data
        }
        self.security_log.append(log_entry)
        print(f"[SECURITY LOG] {log_entry}")

    def _validate_sender(self, sender: object, event: str) -> bool:
        # Проверка прав отправителя на отправку данного события
        sender_type = sender.__class__.__name__

        # Определяем разрешенные события для каждого типа компонента
        allowed_events = {
            "Client": ["order_placed", "order_cancelled"],
            "Manager": ["order_processed", "order_rejected"],
            "Warehouse": ["order_shipped", "insufficient_inventory"]
        }

        if sender_type in allowed_events and event in allowed_events[sender_type]:
            return True

        self._log_security_event("unauthorized_event", sender, {
            "event": event,
            "sender_type": sender_type
        })
        return False

    def _validate_data(self, event: str, data: Dict[str, Any]) -> bool:
        # Валидация данных в сообщении
        required_fields = {
            "order_placed": ["client_id", "order_details"],
            "order_processed": ["manager_id", "order_id"],
            "order_shipped": ["warehouse_id", "order_id"]
        }

        if event in required_fields:
            for field in required_fields[event]:
                if field not in data:
                    self._log_security_event("invalid_data", None, {
                        "event": event,
                        "missing_field": field,
                        "data": data
                    })
                    return False

        # Дополнительные проверки данных
        if event == "order_placed" and "order_details" in data:
            order_details = data["order_details"]
            if not isinstance(order_details, dict) or "items" not in order_details:
                self._log_security_event("invalid_order_details", None, {
                    "event": event,
                    "order_details": order_details
                })
                return False

        return True

    def notify(self, sender: object, event: str, data: Dict[str, Any] = None):
        if data is None:
            data = {}

        # Проверки безопасности
        if not self._validate_sender(sender, event):
            print(f"Безопасность: отклонено событие {event} от {sender.__class__.__name__}")
            return

        if not self._validate_data(event, data):
            print(f"Безопасность: невалидные данные в событии {event}")
            return

        # Логирование события
        self._log_security_event("event_processed", sender, {
            "event": event,
            "data": data
        })

        # Маршрутизация событий
        if event == "order_placed":
            # Уведомляем всех менеджеров о новом заказе
            for manager in self.managers.values():
                manager.handle_event(event, data)

        elif event == "order_processed":
            # Уведомляем клиента и склады
            client_id = data.get("client_id")
            if client_id in self.clients:
                self.clients[client_id].handle_event(event, data)

            for warehouse in self.warehouses.values():
                warehouse.handle_event(event, data)

        elif event == "order_shipped":
            # Уведомляем клиента
            # В реальной системе здесь был бы поиск client_id по order_id
            for client in self.clients.values():
                client.handle_event(event, data)

        elif event == "order_cancelled":
            # Уведомляем менеджеров и склады об отмене
            for manager in self.managers.values():
                manager.handle_event(event, data)

            for warehouse in self.warehouses.values():
                warehouse.handle_event(event, data)

        elif event == "insufficient_inventory":
            # Уведомляем менеджеров о недостатке товара
            for manager in self.managers.values():
                manager.handle_event(event, data)


# Демонстрация работы
if __name__ == "__main__":
    print("=== Демонстрация паттерна Mediator для системы управления заказами ===\n")

    # Создаем посредника
    mediator = OrderMediator()

    # Создаем и регистрируем компоненты
    client = Client("client1", "Виктор Иосович")
    manager = Manager("manager1", "Алесей Жарков")
    warehouse = Warehouse("warehouse1", "Смоленск")

    # Инициализируем склад
    warehouse.inventory = {"prod1": 10, "prod2": 5}

    mediator.register_client(client)
    mediator.register_manager(manager)
    mediator.register_warehouse(warehouse)

    # Клиент размещает заказ
    print("1. Клиент размещает заказ:")
    client.place_order({
        "order_id": "order123",
        "items": [
            {"product_id": "prod1", "quantity": 2, "price": 1000},
            {"product_id": "prod2", "quantity": 1, "price": 500}
        ],
        "total_amount": 2500
    })

    print("\n2. Менеджер обрабатывает заказ:")
    manager.process_order("order123")

    print("\n3. Попытка неавторизованного события:")
    # Попытка отправить неавторизованное событие
    client.send("order_shipped", {"order_id": "order123"})

"""
Вопрос: Как вы обеспечите безопасность при обработке сообщений между компонентами? 
Какие дополнительные проверки добавите?

Ответ:

Меры безопасности, реализованные в системе:

1. Валидация отправителя:
   - Проверка прав компонента на отправку определенных типов событий
   - Разрешенные события определяются для каждого типа компонента

2. Валидация данных:
   - Проверка обязательных полей для каждого типа события
   - Валидация формата и типа данных
   - Проверка бизнес-логики (например, корректность деталей заказа)

3. Логирование безопасности:
   - Запись всех событий с временными метками
   - Логирование попыток неавторизованного доступа
   - Аудит всех взаимодействий между компонентами

4. Дополнительные проверки, которые можно добавить:

   - Аутентификация: проверка подлинности компонента
   - Шифрование: защита конфиденциальных данных в сообщениях
   - Ограничение частоты: защита от спама и DoS-атак
   - Проверка целостности: гарантия, что данные не были изменены
   - Ролевая модель: разные уровни доступа для разных компонентов
   - Санкционирование: проверка прав на выполнение операций
   - Квоты: ограничение количества операций в единицу времени

Пример дополнительных улучшений безопасности:

class SecureOrderMediator(OrderMediator):
    def __init__(self):
        super().__init__()
        self.failed_attempts = {}
        self.max_attempts = 5

    def _check_rate_limit(self, sender_id: str) -> bool:
        if sender_id not in self.failed_attempts:
            return True

        if self.failed_attempts[sender_id] >= self.max_attempts:
            self._log_security_event("rate_limit_exceeded", None, {"sender_id": sender_id})
            return False

        return True

    def _authenticate_component(self, sender: object, auth_token: str) -> bool:
        # Проверка аутентификационного токена
        # В реальной системе здесь была бы проверка против базы данных или сервиса аутентификации
        return hasattr(sender, 'auth_token') and sender.auth_token == auth_token
"""