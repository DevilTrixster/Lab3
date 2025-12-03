from abc import ABC, abstractmethod
from typing import List


# Базовые классы из лабораторной работы №2 (иерархия товаров)
class ProductComponent(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Product(ProductComponent):
    def __init__(self, name: str, price: float, weight: float, category: str = "general"):
        self.name = name
        self.price = price
        self.weight = weight
        self.category = category

    def accept(self, visitor):
        return visitor.visit_product(self)

    def __str__(self):
        return f"{self.name} - {self.price} руб., {self.weight} кг"


class Box(ProductComponent):
    def __init__(self, name: str, packaging_cost: float = 0):
        self.name = name
        self.packaging_cost = packaging_cost
        self.children: List[ProductComponent] = []

    def add(self, component: ProductComponent):
        self.children.append(component)

    def remove(self, component: ProductComponent):
        self.children.remove(component)

    def accept(self, visitor):
        return visitor.visit_box(self)

    def get_total_weight(self):
        return sum(child.weight if isinstance(child, Product) else child.get_total_weight() for child in self.children)

    def get_total_price(self):
        return sum(child.price if isinstance(child, Product) else child.get_total_price() for child in self.children)

    def __str__(self):
        return f"Коробка '{self.name}' ({len(self.children)} items)"


# Абстрактный класс посетителя
class Visitor(ABC):
    @abstractmethod
    def visit_product(self, product: Product):
        pass

    @abstractmethod
    def visit_box(self, box: Box):
        pass


# Конкретные посетители
class DeliveryCostCalculator(Visitor):
    def __init__(self, base_rate: float = 100, weight_rate: float = 50, fragile_surcharge: float = 200):
        self.base_rate = base_rate
        self.weight_rate = weight_rate
        self.fragile_surcharge = fragile_surcharge

    def visit_product(self, product: Product):
        # Расчет стоимости доставки для товара
        delivery_cost = self.base_rate + (product.weight * self.weight_rate)

        # Дополнительная плата за хрупкие товары
        if product.category == "fragile":
            delivery_cost += self.fragile_surcharge

        print(f"Доставка '{product.name}': {delivery_cost} руб.")
        return delivery_cost

    def visit_box(self, box: Box):
        # Расчет стоимости доставки для коробки (сумма доставки содержимого + упаковка)
        total_delivery_cost = box.packaging_cost

        for child in box.children:
            total_delivery_cost += child.accept(self)

        print(
            f"Доставка коробки '{box.name}': {total_delivery_cost} руб. (включая упаковку: {box.packaging_cost} руб.)")
        return total_delivery_cost


class TaxCalculator(Visitor):
    def __init__(self, standard_rate: float = 0.20, reduced_rate: float = 0.10, luxury_rate: float = 0.30):
        self.standard_rate = standard_rate
        self.reduced_rate = reduced_rate
        self.luxury_rate = luxury_rate

    def visit_product(self, product: Product):
        # Расчет налога для товара в зависимости от категории
        if product.category == "food" or product.category == "books":
            tax_rate = self.reduced_rate
        elif product.category == "luxury":
            tax_rate = self.luxury_rate
        else:
            tax_rate = self.standard_rate

        tax_amount = product.price * tax_rate
        print(f"Налог на '{product.name}': {tax_amount} руб. (ставка: {tax_rate * 100}%)")
        return tax_amount

    def visit_box(self, box: Box):
        # Расчет налога для коробки (сумма налогов содержимого)
        total_tax = 0

        for child in box.children:
            total_tax += child.accept(self)

        print(f"Общий налог для коробки '{box.name}': {total_tax} руб.")
        return total_tax


# Новый посетитель для расчета скидок
class DiscountCalculator(Visitor):
    def __init__(self, bulk_discount_threshold: float = 10000, bulk_discount_rate: float = 0.10,
                 seasonal_discount_rate: float = 0.05):
        self.bulk_discount_threshold = bulk_discount_threshold
        self.bulk_discount_rate = bulk_discount_rate
        self.seasonal_discount_rate = seasonal_discount_rate

    def visit_product(self, product: Product):
        # Скидка на отдельный товар (например, сезонная)
        discount = product.price * self.seasonal_discount_rate
        print(f"Скидка на '{product.name}': {discount} руб.")
        return discount

    def visit_box(self, box: Box):
        # Скидка на коробку (может быть оптовой скидкой)
        total_price = box.get_total_price()
        discount = 0

        if total_price > self.bulk_discount_threshold:
            discount = total_price * self.bulk_discount_rate
            print(f"Оптовая скидка на коробку '{box.name}': {discount} руб.")
        else:
            # Или сумма сезонных скидок на товары
            for child in box.children:
                discount += child.accept(self)

        return discount


# Класс для управления расчетами
class OrderCalculator:
    def __init__(self):
        self.visitors = []

    def add_visitor(self, visitor: Visitor):
        self.visitors.append(visitor)

    def calculate_all(self, component: ProductComponent):
        results = {}

        for visitor in self.visitors:
            visitor_name = visitor.__class__.__name__
            print(f"\n--- {visitor_name} ---")
            results[visitor_name] = component.accept(visitor)

        return results


# Демонстрация работы
if __name__ == "__main__":
    print("=== Демонстрация паттерна Visitor для расчетов стоимости ===")

    # Создаем товары
    laptop = Product("Ноутбук", 75000, 2.5, "electronics")
    book = Product("Книга", 500, 0.5, "books")
    vase = Product("Ваза", 3000, 1.0, "fragile")
    chocolate = Product("Шоколад", 200, 0.2, "food")

    # Создаем коробки
    electronics_box = Box("Электроника", packaging_cost=100)
    gifts_box = Box("Подарки", packaging_cost=150)

    # Добавляем товары в коробки
    electronics_box.add(laptop)

    gifts_box.add(book)
    gifts_box.add(vase)
    gifts_box.add(chocolate)

    # Создаем главную коробку
    main_box = Box("Главная коробка", packaging_cost=50)
    main_box.add(electronics_box)
    main_box.add(gifts_box)

    # Создаем калькулятор и добавляем посетителей
    calculator = OrderCalculator()
    calculator.add_visitor(DeliveryCostCalculator())
    calculator.add_visitor(TaxCalculator())
    calculator.add_visitor(DiscountCalculator())

    # Выполняем все расчеты
    print(f"\nРасчеты для заказа:")
    results = calculator.calculate_all(main_box)

    # Итоговые результаты
    print(f"\n=== ИТОГИ ===")
    for visitor_name, result in results.items():
        print(f"{visitor_name}: {result} руб.")

"""
Расширение системы для новых типов расчетов:

1. Добавление нового посетителя:
   - Создаем новый класс, наследуемый от Visitor
   - Реализуем методы visit_product() и visit_box() для нового типа расчета

2. Изменения в коде:
   - НЕ требуется изменять существующие классы Product и Box
   - НЕ требуется изменять существующих посетителей
   - Новый посетитель легко интегрируется через OrderCalculator

3. Пример добавления скидок:
   - Создаем DiscountCalculator с логикой расчета скидок
   - Добавляем его в OrderCalculator через add_visitor()
   - Система автоматически применяет новый расчет ко всей иерархии
"""