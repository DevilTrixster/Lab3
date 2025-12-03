from abc import ABC, abstractmethod


# Абстрактный класс стратегии оплаты
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


# Конкретные стратегии оплаты
class CashPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Обработка наличного платежа на сумму {amount} руб.")


class BankTransferPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Обработка безналичного платежа на сумму {amount} руб.")


class CashOnDeliveryPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Заказ оформлен с оплатой при получении на сумму {amount} руб.")


# Класс заказа, использующий стратегию оплаты
class Order:
    def __init__(self):
        self._payment_strategy = None

    def set_payment_strategy(self, strategy):
        self._payment_strategy = strategy

    def process_order(self, amount):
        if self._payment_strategy:
            self._payment_strategy.process_payment(amount)
        else:
            print("Метод оплаты не выбран!")


# Демонстрация работы
if __name__ == "__main__":
    order = Order()

    # Оплата наличными
    order.set_payment_strategy(CashPayment())
    order.process_order(1500)

    # Оплата картой
    order.set_payment_strategy(BankTransferPayment())
    order.process_order(2000)

    # Оплата при получении
    order.set_payment_strategy(CashOnDeliveryPayment())
    order.process_order(3000)

"""
Инструкция по добавлению нового метода оплаты (например, криптовалюты):

1. Создать новый класс-стратегию, унаследованный от PaymentStrategy
2. Реализовать метод process_payment с конкретной логикой обработки платежа
"""