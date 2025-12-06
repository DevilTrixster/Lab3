from abc import ABC, abstractmethod

class Order:
    def __init__(self, items, total_price):
        self.items = items
        self.total_price = total_price
        self.is_paid = False
        self.is_delivered = False
        self.delivery_method = None

    def __str__(self):
        return f"Заказ: {self.items}, сумма: {self.total_price}, оплачен: {self.is_paid}, доставлен: {self.is_delivered}, доставка: {self.delivery_method}"

class OrderProcessing(ABC):
    def process_order(self, order: Order):
        """Шаблонный метод - общий алгоритм обработки заказа"""
        self.select_items(order)
        self.confirm_order(order)
        self.payment(order)
        self.delivery(order)
        self.complete_order(order)

    def select_items(self, order: Order):
        print(f"Товары выбраны: {order.items}")

    def confirm_order(self, order: Order):
        print(f"Заказ оформлен. Сумма: {order.total_price}")

    @abstractmethod
    def payment(self, order: Order):
        pass

    @abstractmethod
    def delivery(self, order: Order):
        pass

    def complete_order(self, order: Order):
        print("Заказ завершен")

class StandardOrderProcessing(OrderProcessing):
    def payment(self, order: Order):
        order.is_paid = True
        print("Оплата при получении")

    def delivery(self, order: Order):
        order.delivery_method = "Стандартная доставка (3-5 дней)"
        order.is_delivered = True
        print("Заказ передан в службу стандартной доставки")

class ExpressOrderProcessing(OrderProcessing):
    def payment(self, order: Order):
        order.is_paid = True
        print("Онлайн оплата картой")

    def delivery(self, order: Order):
        order.delivery_method = "Экспресс-доставка (1-2 дня)"
        order.is_delivered = True
        print("Заказ передан в службу экспресс-доставки")

class PrepaidOrderProcessing(OrderProcessing):
    def payment(self, order: Order):
        order.is_paid = True
        print("Предоплата 100% онлайн")

    def delivery(self, order: Order):
        order.delivery_method = "Доставка после предоплаты (2-4 дня)"
        order.is_delivered = True
        print("Заказ отправлен после подтверждения предоплаты")

if __name__ == "__main__":
    order1 = Order(["Книга", "Ручка"], 1500)

    # Обрабатываем стандартный заказ
    print("=== Стандартный заказ ===")
    processor1 = StandardOrderProcessing()
    processor1.process_order(order1)
    print(order1)
    print()

    # Создаем и обрабатываем экспресс заказ
    order2 = Order(["Ноутбук", "Мышь"], 75000)
    print("=== Экспресс заказ ===")
    processor2 = ExpressOrderProcessing()
    processor2.process_order(order2)
    print(order2)
    print()

    # Создаем и обрабатываем заказ с предоплатой
    order3 = Order(["Смартфон", "Чехол"], 45000)
    print("=== Заказ с предоплатой ===")
    processor3 = PrepaidOrderProcessing()
    processor3.process_order(order3)
    print(order3)

'''
Для расширения системы новым типом заказа (например, с предоплатой) потребуются следующие изменения:

1. Создать новый класс-наследник PrepaidOrderProcessing от абстрактного класса OrderProcessing
2. Реализовать в нем абстрактные методы payment() и delivery() с соответствующей логикой
3. При необходимости переопределить другие шаги алгоритма (хотя в данном случае достаточно только payment() и delivery())

Изменения будут минимальными благодаря паттерну Template Method:
- Не нужно изменять существующие классы (StandardOrderProcessing, ExpressOrderProcessing)
- Не нужно изменять абстрактный класс OrderProcessing
- Новый тип заказа добавляется путем создания нового класса и реализации конкретных шагов

Для реализации функционала предоплаты в методе ProcessOrder():
1. В методе payment() класса PrepaidOrderProcessing устанавливаем статус оплаты и выводим сообщение о предоплате
2. В методе delivery() добавляем проверку или особую логику доставки после предоплаты
3. При необходимости можно добавить дополнительные шаги (например, проверку подтверждения платежа) через переопределение других методов
'''