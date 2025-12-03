from abc import ABC, abstractmethod
from typing import List, Optional


# Класс товара
class Product:
    def __init__(self, name: str, category: str, price: float, popularity: int):
        self.name = name
        self.category = category
        self.price = price
        self.popularity = popularity

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price} руб., популярность: {self.popularity}"


# Интерфейс итератора
class CatalogIterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Optional[Product]:
        pass

    @abstractmethod
    def next_count(self, count: int) -> List[Product]:
        pass

    @abstractmethod
    def reset(self):
        pass


# Конкретные итераторы
class CategoryIterator(CatalogIterator):
    def __init__(self, products: List[Product]):
        self._products = sorted(products, key=lambda x: (x.category, x.name))
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> Optional[Product]:
        if self.has_next():
            product = self._products[self._index]
            self._index += 1
            return product
        return None

    def next_count(self, count: int) -> List[Product]:
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
        if self.has_next():
            product = self._products[self._index]
            self._index += 1
            return product
        return None

    def next_count(self, count: int) -> List[Product]:
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
        if self.has_next():
            product = self._products[self._index]
            self._index += 1
            return product
        return None

    def next_count(self, count: int) -> List[Product]:
        result = []
        for _ in range(count):
            if self.has_next():
                result.append(self.next())
            else:
                break
        return result

    def reset(self):
        self._index = 0


# Класс каталога
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
            raise ValueError(f"Unknown iterator type: {iterator_type}")

    def has_next(self) -> bool:
        if self._current_iterator:
            return self._current_iterator.has_next()
        return False

    def next(self) -> Optional[Product]:
        if self._current_iterator:
            return self._current_iterator.next()
        return None

    def next_count(self, count: int) -> List[Product]:
        if self._current_iterator:
            return self._current_iterator.next_count(count)
        return []

    def reset(self):
        if self._current_iterator:
            self._current_iterator.reset()

    def get_products_count(self) -> int:
        return len(self._products)


# Демонстрация работы
if __name__ == "__main__":
    # Создаем каталог
    catalog = Catalog()

    # Добавляем товары
    catalog.add_product(Product("Ноутбук", "Электроника", 75000, 85))
    catalog.add_product(Product("Смартфон", "Электроника", 45000, 95))
    catalog.add_product(Product("Книга", "Книги", 500, 70))
    catalog.add_product(Product("Кофе", "Продукты", 300, 60))
    catalog.add_product(Product("Футболка", "Одежда", 1500, 75))

    print("=== Обход по категориям ===")
    catalog.set_iterator("category")
    while catalog.has_next():
        print(catalog.next())

    print("\n=== Обход по цене (от дешевых к дорогим) ===")
    catalog.set_iterator("price")
    while catalog.has_next():
        print(catalog.next())

    print("\n=== Обход по популярности (от самых популярных) ===")
    catalog.set_iterator("popularity")
    products = catalog.next_count(3)
    for product in products:
        print(product)

"""
Ситуация, когда в каталоге нет товаров, соответствующих критерию, может возникнуть в нескольких случаях:

1. Пустой каталог - нет товаров вообще
2. Критерий слишком строгий - нет товаров, удовлетворяющих условиям

Обработка таких ситуаций:

1. Для пустого каталога:
   - Итераторы будут корректно работать, возвращая has_next() = False
   - Метод next() будет возвращать None

2. Для критериев, которые могут не находить товары:
   - Можно добавить валидацию при создании итератора
   - Предоставить информацию о количестве найденных товаров

3. Изменения в системе для улучшения обработки:
   - Добавить метод в Catalog для проверки наличия товаров перед созданием итератора
   - Реализовать исключения для случаев, когда итератор не может быть создан
   - Добавить логирование для отладки проблем с критериями

"""
