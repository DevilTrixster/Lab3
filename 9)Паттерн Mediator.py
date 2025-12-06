from abc import ABC, abstractmethod
from typing import Dict, Any


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str, data: Dict[str, Any] = None):
        pass


class OrderMediator(Mediator):
    def __init__(self):
        self.client = None
        self.manager = None
        self.warehouse = None

    def set_components(self, client, manager, warehouse):
        self.client = client
        self.manager = manager
        self.warehouse = warehouse

    def notify(self, sender: object, event: str, data: Dict[str, Any] = None):
        data = data or {}

        # Обработка событий от клиента
        if isinstance(sender, Client):
            if event == "place_order":
                print("Посредник: Получен новый заказ от клиента")
                self.manager.receive_order(data)
            elif event == "cancel_order":
                print("Посредник: Заказ отменен клиентом")
                self.manager.receive_cancellation(data)

        # Обработка событий от менеджера
        elif isinstance(sender, Manager):
            if event == "approve_order":
                print("Посредник: Заказ одобрен менеджером")
                self.warehouse.process_order(data)
            elif event == "reject_order":
                print("Посредник: Заказ отклонен менеджером")
                self.client.notify_rejection(data)
            elif event == "order_fulfilled":
                print("Посредник: Менеджер подтвердил выполнение заказа")
                self.client.notify_completion(data)

        # Обработка событий от склада
        elif isinstance(sender, Warehouse):
            if event == "order_ready":
                print("Посредник: Склад подготовил заказ")
                self.manager.receive_order_ready(data)
            elif event == "out_of_stock":
                print("Посредник: На складе недостаточно товара")
                self.manager.receive_stock_info(data)
                self.client.notify_stock_issue(data)


class Colleague(ABC):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def send(self, event: str, data: Dict[str, Any] = None):
        self.mediator.notify(self, event, data)


class Client(Colleague):
    def place_order(self, order_details: Dict[str, Any]):
        print(f"Клиент: Размещаю заказ - {order_details['product']}")
        self.send("place_order", order_details)

    def cancel_order(self, order_id: str):
        print(f"Клиент: Отменяю заказ {order_id}")
        self.send("cancel_order", {"order_id": order_id})

    def notify_rejection(self, data: Dict[str, Any]):
        print(f"Клиент: Заказ {data.get('order_id')} отклонен. Причина: {data.get('reason')}")

    def notify_completion(self, data: Dict[str, Any]):
        print(f"Клиент: Заказ {data.get('order_id')} выполнен. Спасибо!")

    def notify_stock_issue(self, data: Dict[str, Any]):
        print(f"Клиент: Товара '{data.get('product')}' нет в наличии. Мы вас уведомим о поступлении.")


class Manager(Colleague):
    def receive_order(self, order_details: Dict[str, Any]):
        print(f"Менеджер: Получен заказ на {order_details['product']}")
        # Проверка и утверждение заказа
        if self.validate_order(order_details):
            self.send("approve_order", order_details)
        else:
            self.send("reject_order", {
                "order_id": order_details.get("order_id"),
                "reason": "Невалидный заказ"
            })

    def receive_cancellation(self, data: Dict[str, Any]):
        print(f"Менеджер: Получена отмена заказа {data.get('order_id')}")

    def receive_order_ready(self, data: Dict[str, Any]):
        print(f"Менеджер: Заказ {data.get('order_id')} готов к отгрузке")
        self.send("order_fulfilled", data)

    def receive_stock_info(self, data: Dict[str, Any]):
        print(f"Менеджер: Получена информация о недостатке товара на складе")

    def validate_order(self, order_details: Dict[str, Any]) -> bool:
        """Валидация заказа"""
        return bool(order_details.get("product") and order_details.get("quantity", 0) > 0)


class Warehouse(Colleague):

    def __init__(self, mediator: Mediator):
        super().__init__(mediator)
        self.stock = {"Ноутбук": 5, "Айфон": 3, "Планшет": 0}

    def process_order(self, order_details: Dict[str, Any]):
        product = order_details.get("product")
        quantity = order_details.get("quantity", 1)

        print(f"Склад: Обрабатываю заказ на {product}")

        if self.check_stock(product, quantity):
            print(f"Склад: Товар {product} в наличии")
            self.update_stock(product, quantity)
            self.send("order_ready", order_details)
        else:
            print(f"Склад: Товара {product} недостаточно")
            self.send("out_of_stock", order_details)

    def check_stock(self, product: str, quantity: int) -> bool:
        return self.stock.get(product, 0) >= quantity

    def update_stock(self, product: str, quantity: int):
        if product in self.stock:
            self.stock[product] -= quantity


if __name__ == "__main__":

    # Создание и настройка системы
    mediator = OrderMediator()

    client = Client(mediator)
    manager = Manager(mediator)
    warehouse = Warehouse(mediator)

    mediator.set_components(client, manager, warehouse)

    print("=" * 50)
    client.place_order({"order_id": "ORD001", "product": "Ноубук", "quantity": 1})
    print("-" * 30)
    client.place_order({"order_id": "ORD002", "product": "Планшет", "quantity": 2})
    print("-" * 30)
    client.cancel_order("ORD003")
    print("=" * 50)

    '''
    Для обеспечения безопасности при обработке сообщений между компонентами:
    1. Добавить аутентификацию компонентов через уникальные идентификаторы
    2. Реализовать проверку прав доступа для каждого типа событий
    3. Внедрить валидацию всех входящих данных
    4. Добавить логирование всех операций для аудита
    5. Использовать шифрование конфиденциальных данных
    6. Реализовать механизм подтверждений для критических операций
    
    ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ:
    
   - Лимиты на частоту запросов (rate limiting)
   - Проверка на циклические вызовы и deadlock
   - Валидация состояния системы перед выполнением операций
   - Проверка квот и лимитов для клиентов
   - Валидация бизнес-логики (например, нельзя отменить выполненный заказ)
    '''
