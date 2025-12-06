from abc import ABC, abstractmethod
from typing import List, Optional


class Product:
    def __init__(self, name: str, category: str, price: float, popularity: int):
        self.name = name
        self.category = category
        self.price = price
        self.popularity = popularity

    def __repr__(self):
        return f"{self.name} ({self.category}) - {self.price} руб, популярность: {self.popularity}"


class CatalogIterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Optional[Product]:
        pass

    @abstractmethod
    def next_n(self, count: int) -> List[Product]:
        pass

    @abstractmethod
    def reset(self):
        pass


class CategoryIterator(CatalogIterator):
    def __init__(self, products: List[Product]):
        self._products = sorted(products, key=lambda x: x.category)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> Optional[Product]:
        if not self.has_next():
            return None
        product = self._products[self._index]
        self._index += 1
        return product

    def next_n(self, count: int) -> List[Product]:
        result = []
        for _ in range(count):
            if self.has_next():
                result.append(self.next())
            else:
                break
        return result

    def reset(self):
        self._index = 0


class PriceIterator(CatalogIterator):
    def __init__(self, products: List[Product]):
        self._products = sorted(products, key=lambda x: x.price)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> Optional[Product]:
        if not self.has_next():
            return None
        product = self._products[self._index]
        self._index += 1
        return product

    def next_n(self, count: int) -> List[Product]:
        result = []
        for _ in range(count):
            if self.has_next():
                result.append(self.next())
            else:
                break
        return result

    def reset(self):
        self._index = 0


class PopularityIterator(CatalogIterator):
    def __init__(self, products: List[Product]):
        self._products = sorted(products, key=lambda x: x.popularity, reverse=True)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> Optional[Product]:
        if not self.has_next():
            return None
        product = self._products[self._index]
        self._index += 1
        return product

    def next_n(self, count: int) -> List[Product]:
        result = []
        for _ in range(count):
            if self.has_next():
                result.append(self.next())
            else:
                break
        return result

    def reset(self):
        self._index = 0


class Catalog:
    def __init__(self):
        self._products: List[Product] = []
        self._current_iterator: Optional[CatalogIterator] = None

    def add_product(self, product: Product):
        self._products.append(product)

    def set_iterator(self, iterator_type: str):
        if iterator_type == "category":
            self._current_iterator = CategoryIterator(self._products)
        elif iterator_type == "price":
            self._current_iterator = PriceIterator(self._products)
        elif iterator_type == "popularity":
            self._current_iterator = PopularityIterator(self._products)
        else:
            raise ValueError(f"Неизвестный тип итератора: {iterator_type}")

    def has_next(self) -> bool:
        if self._current_iterator is None:
            return False
        return self._current_iterator.has_next()

    def next(self) -> Optional[Product]:
        if self._current_iterator is None:
            return None
        return self._current_iterator.next()

    def next_n(self, count: int) -> List[Product]:
        if self._current_iterator is None:
            return []
        return self._current_iterator.next_n(count)

    def reset(self):
        if self._current_iterator:
            self._current_iterator.reset()

if __name__ == "__main__":
    catalog = Catalog()

    catalog.add_product(Product("Ноутбук", "Электроника", 25999, 8))
    catalog.add_product(Product("Смартфон", "Электроника", 21000, 9))
    catalog.add_product(Product("Книга", "Книги", 500, 7))
    catalog.add_product(Product("Футболка", "Одежда", 3255, 6))
    catalog.add_product(Product("Кофе", "Продукты", 150, 5))

    print("Обход по категориям:")
    catalog.set_iterator("category")
    while catalog.has_next():
        print(catalog.next())

    print("\nОбход по цене (возрастание):")
    catalog.set_iterator("price")
    while catalog.has_next():
        print(catalog.next())

    print("\nОбход по популярности (убывание):")
    catalog.set_iterator("popularity")
    products = catalog.next_n(3)
    for product in products:
        print(product)

    catalog.reset()
    print("\nСброшенный итератор популярности:")
    while catalog.has_next():
        print(catalog.next())

'''
При обработке ситуации, когда в каталоге нет товаров, соответствующих критерию:
   - Все итераторы корректно работают с пустыми списками товаров - методы has_next() сразу возвращают False.
   - При создании итератора с пустым списком продуктов:
   - Конструкторы итераторов принимают пустой список
   - Методы next() возвращают None
   - Методы next_n() возвращают пустой список
Для критериев, требующих фильтрации (например, товары конкретной категории), следует:
    a) Реализовать параметризованные конструкторы итераторов
    b) Добавить в Catalog метод set_iterator_with_filter(), принимающий критерии фильтрации
    c) Фильтровать товары перед передачей в итератор
Изменения в системе:
    1.Добавить поддержку фильтров в итераторы
    2.В Catalog добавить методы для фильтрации по критериям
    3.Возвращать специальный "пустой итератор" при отсутствии товаров
    4.Добавить логирование или уведомление о пустом результате
    5.При пустом результате: методы next() возвращают None, has_next() = False, что позволяет клиентскому коду безопасно обрабатывать отсутствие данных.'''