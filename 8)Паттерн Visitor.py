from abc import ABC, abstractmethod
from typing import List

class OrderElement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Product(OrderElement):
    def __init__(self, name: str, price: float, weight: float):
        self.name = name
        self.price = price
        self.weight = weight

    def accept(self, visitor):
        visitor.visit_product(self)

class Box(OrderElement):
    def __init__(self, name: str, packaging_cost: float = 0.0):
        self.name = name
        self.packaging_cost = packaging_cost  # стоимость упаковки
        self.children: List[OrderElement] = []

    def add(self, element: OrderElement):
        self.children.append(element)

    def accept(self, visitor):
        visitor.visit_box(self)

class Visitor(ABC):
    @abstractmethod
    def visit_product(self, product: Product):
        pass

    @abstractmethod
    def visit_box(self, box: Box):
        pass

class DeliveryCostCalculator(Visitor):
    def __init__(self, price_per_kg: float = 2.5):
        self.price_per_kg = price_per_kg
        self.total = 0.0

    def visit_product(self, product: Product):
        self.total += product.weight * self.price_per_kg

    def visit_box(self, box: Box):
        # Считаем доставку для всех вложенных элементов
        for child in box.children:
            child.accept(self)
        # Добавляем стоимость упаковки (она же доставка упаковки)
        self.total += box.packaging_cost * self.price_per_kg

class TaxCalculator(Visitor):
    def __init__(self, tax_rate: float = 0.18):
        self.tax_rate = tax_rate
        self.total = 0.0

    def visit_product(self, product: Product):
        self.total += product.price * self.tax_rate

    def visit_box(self, box: Box):
        for child in box.children:
            child.accept(self)
        # Налог на упаковку не начисляем (по условию задачи)

if __name__ == "__main__":
    # Создаём товары
    laptop = Product("Ноутбук", 70990, 3.0)
    mouse = Product("Мышь", 350, 0.2)
    charger = Product("Зарядное устройство", 400, 0.5)

    # Создаём коробки
    small_box = Box("Маленькая коробка", 0.1)
    big_box = Box("Большая коробка", 0.5)

    # Собираем структуру
    small_box.add(mouse)
    small_box.add(charger)
    big_box.add(laptop)
    big_box.add(small_box)

    # Считаем доставку
    delivery_calculator = DeliveryCostCalculator(price_per_kg=2.5)
    big_box.accept(delivery_calculator)
    print(f"Стоимость доставки: {delivery_calculator.total:.2f} руб")

    # Считаем налоги
    tax_calculator = TaxCalculator(tax_rate=0.18)
    big_box.accept(tax_calculator)
    print(f"Сумма налогов: {tax_calculator.total:.2f} руб")

'''
Для добавления новых типов расчетов (например, скидок) необходимо:
1. Создать нового посетителя (например, DiscountCalculator), унаследованного от Visitor.
2. Реализовать методы visit_product() и visit_box() с новой логикой расчета.
3. Никаких изменений в классах Product, Box или существующих посетителях не требуется.
4. Клиентский код будет использовать нового посетителя так же, как и существующих.
'''