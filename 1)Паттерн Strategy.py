from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self):
        pass

class CardPayment(PaymentStrategy):
    def process_payment(self):
        print("Оплата картой: списание средств с банковской карты")

class CashPayment(PaymentStrategy):
    def process_payment(self):
        print("Оплата наличными: курьер примет наличные при доставке")

class CODpayment(PaymentStrategy):
    def process_payment(self):
        print("Перевод при получении: оплата при получении товара")

class Order:
    def __init__(self, payment_strategy: PaymentStrategy = None):
        self._payment_strategy = payment_strategy

    def set_payment_strategy(self, payment_strategy: PaymentStrategy):
        self._payment_strategy = payment_strategy

    def process_order_payment(self):
        if self._payment_strategy:
            self._payment_strategy.process_payment()
        else:
            print("Метод оплаты не выбран")

if __name__ == "__main__":
    order = Order()

    # Выбор оплаты картой
    order.set_payment_strategy(CardPayment())
    order.process_order_payment()

    # Динамическая смена на наличные
    order.set_payment_strategy(CashPayment())
    order.process_order_payment()

    # Перевод при получении
    order.set_payment_strategy(CODpayment())
    order.process_order_payment()

'''Инструкция по добавлению криптовалюты:
1. Создать класс CryptoPayment(PaymentStrategy)
2. Реализовать метод process_payment()
3. Использовать: order.set_payment_strategy(CryptoPayment())'''