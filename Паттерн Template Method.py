from abc import ABC, abstractmethod


# Класс заказа
class Order:
    def __init__(self, order_id, items, total_amount):
        self.order_id = order_id
        self.items = items
        self.total_amount = total_amount
        self.status = "Создан"


# Абстрактный класс обработки заказа с шаблонным методом
class OrderProcessing(ABC):
    def process_order(self, order):
        """Шаблонный метод - определяет общий алгоритм обработки заказа"""
        print(f"\n=== Обработка заказа #{order.order_id} ===")

        self.select_items(order)
        self.validate_order(order)
        self.process_payment(order)
        self.arrange_delivery(order)
        self.send_confirmation(order)

        print(f"Заказ #{order.order_id} успешно обработан!")
        return order

    def select_items(self, order):
        """Общий шаг - выбор товаров (не требует переопределения)"""
        print(f"Выбраны товары: {', '.join(order.items)}")
        order.status = "Товары выбраны"

    def validate_order(self, order):
        """Общий шаг - проверка заказа (не требует переопределения)"""
        print("Проверка заказа пройдена")
        order.status = "Проверен"

    @abstractmethod
    def process_payment(self, order):
        """Абстрактный метод - обработка оплаты (требует реализации)"""
        pass

    @abstractmethod
    def arrange_delivery(self, order):
        """Абстрактный метод - организация доставки (требует реализации)"""
        pass

    def send_confirmation(self, order):
        """Общий шаг - отправка подтверждения (может быть переопределен)"""
        print("Отправлено подтверждение заказа клиенту")
        order.status = "Завершен"


# Конкретные реализации обработки заказов
class StandardOrderProcessing(OrderProcessing):
    def process_payment(self, order):
        """Оплата при получении"""
        print(f"Оформлена оплата при получении на сумму {order.total_amount} руб.")
        order.status = "Ожидает оплаты при получении"

    def arrange_delivery(self, order):
        """Стандартная доставка"""
        print("Организована стандартная доставка (5-7 дней)")
        order.status = "Передан в службу доставки"


class ExpressOrderProcessing(OrderProcessing):
    def process_payment(self, order):
        """Мгновенная онлайн-оплата"""
        print(f"Списана сумма {order.total_amount} руб. с карты клиента")
        order.status = "Оплачен онлайн"

    def arrange_delivery(self, order):
        """Экспресс-доставка"""
        print("Организована экспресс-доставка (1-2 дня)")
        order.status = "Передан в экспресс-доставку"

    def send_confirmation(self, order):
        """Расширенное подтверждение для экспресс-заказов"""
        super().send_confirmation(order)
        print("Отправлено SMS с номером отслеживания")


# Новая реализация для заказов с предоплатой
class PrepaidOrderProcessing(OrderProcessing):
    def __init__(self, prepaid_amount=0):
        self.prepaid_amount = prepaid_amount

    def process_payment(self, order):
        """Обработка предоплаты"""
        remaining_amount = order.total_amount - self.prepaid_amount
        print(f"Внесена предоплата: {self.prepaid_amount} руб.")
        print(f"Оставшаяся сумма к оплате при получении: {remaining_amount} руб.")
        order.status = "Частично оплачен"

    def arrange_delivery(self, order):
        """Доставка с проверкой предоплаты"""
        print("Организована доставка с проверкой предоплаты")
        order.status = "Доставляется после предоплаты"

    def validate_order(self, order):
        """Дополнительная проверка для предоплаченных заказов"""
        super().validate_order(order)
        print("Проверка наличия предоплаты пройдена")


# Класс для управления заказами
class OrderManager:
    def __init__(self):
        self.orders = []

    def create_order(self, order_id, items, total_amount, processing_type):
        order = Order(order_id, items, total_amount)
        processor = processing_type
        processed_order = processor.process_order(order)
        self.orders.append(processed_order)
        return processed_order


# Демонстрация работы
if __name__ == "__main__":
    manager = OrderManager()

    print("=== Демонстрация паттерна Template Method для обработки заказов ===\n")

    # Стандартный заказ
    manager.create_order(
        order_id=1001,
        items=["Ноутбук", "Мышка"],
        total_amount=75000,
        processing_type=StandardOrderProcessing()
    )

    # Экспресс-заказ
    manager.create_order(
        order_id=1002,
        items=["Смартфон", "Чехол"],
        total_amount=45000,
        processing_type=ExpressOrderProcessing()
    )

    # Заказ с предоплатой
    manager.create_order(
        order_id=1003,
        items=["Планшет", "Клавиатура"],
        total_amount=35000,
        processing_type=PrepaidOrderProcessing(prepaid_amount=10000)
    )

"""
Расширение системы для нового типа заказа (предоплата):

1. Создание нового класса-наследника:
   - Создаем класс PrepaidOrderProcessing, наследуемый от OrderProcessing
   - Реализуем абстрактные методы process_payment() и arrange_delivery()

2. Изменения в коде:
   - НЕ требуется изменять базовый класс OrderProcessing
   - НЕ требуется изменять существующие классы StandardOrderProcessing и ExpressOrderProcessing
   - Можно добавить новый класс без модификации существующего кода

3. Реализация функционала предоплаты в ProcessOrder():
   - В методе process_payment() обрабатываем частичную оплату
   - В arrange_delivery() добавляем логику проверки предоплаты перед доставкой
   - При необходимости переопределяем другие методы (например, validate_order() для дополнительных проверок)
"""