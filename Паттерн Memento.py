import copy
from typing import List, Dict, Any


# Класс товара
class Product:
    def __init__(self, id: str, name: str, price: float, quantity: int = 1):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - {self.price} руб. (x{self.quantity})"

    def __eq__(self, other):
        return self.id == other.id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['id'], data['name'], data['price'], data['quantity'])


# Класс Memento для хранения состояния корзины
class ShoppingCartMemento:
    def __init__(self, state: List[Dict[str, Any]]):
        self._state = copy.deepcopy(state)
        self._timestamp = None

    def get_state(self) -> List[Dict[str, Any]]:
        return copy.deepcopy(self._state)


# Класс корзины покупок
class ShoppingCart:
    def __init__(self):
        self._items: List[Product] = []

    def add_product(self, product: Product):
        """Добавляет товар в корзину"""
        # Проверяем, есть ли товар уже в корзине
        for item in self._items:
            if item.id == product.id:
                item.quantity += product.quantity
                return

        self._items.append(copy.copy(product))

    def remove_product(self, product_id: str, quantity: int = 1):
        """Удаляет товар из корзины"""
        for item in self._items:
            if item.id == product_id:
                if item.quantity <= quantity:
                    self._items.remove(item)
                else:
                    item.quantity -= quantity
                return

    def clear_cart(self):
        """Очищает корзину"""
        self._items.clear()

    def get_items(self) -> List[Product]:
        """Возвращает копию списка товаров"""
        return copy.deepcopy(self._items)

    def get_total_price(self) -> float:
        """Возвращает общую стоимость корзины"""
        return sum(item.price * item.quantity for item in self._items)

    def create_memento(self) -> ShoppingCartMemento:
        """Создает Memento с текущим состоянием корзины"""
        state = [item.to_dict() for item in self._items]
        return ShoppingCartMemento(state)

    def restore_from_memento(self, memento: ShoppingCartMemento):
        """Восстанавливает состояние корзины из Memento"""
        self._items.clear()
        state_data = memento.get_state()
        for item_data in state_data:
            self._items.append(Product.from_dict(item_data))

    def __str__(self):
        if not self._items:
            return "Корзина пуста"

        items_str = "\n".join(f"  {i + 1}. {item}" for i, item in enumerate(self._items))
        return f"Корзина покупок:\n{items_str}\nИтого: {self.get_total_price()} руб."


# Класс Caretaker для управления моментами сохранения
class CartCaretaker:
    def __init__(self, max_history_size: int = 10):
        self._mementos: List[ShoppingCartMemento] = []
        self._max_history_size = max_history_size
        self._current_index = -1

    def save_state(self, cart: ShoppingCart):
        """Сохраняет текущее состояние корзины"""
        memento = cart.create_memento()

        # Удаляем все состояния после текущего (если были отмены и новые действия)
        if self._current_index < len(self._mementos) - 1:
            self._mementos = self._mementos[:self._current_index + 1]

        self._mementos.append(memento)
        self._current_index = len(self._mementos) - 1

        # Ограничиваем размер истории
        if len(self._mementos) > self._max_history_size:
            self._mementos.pop(0)
            self._current_index -= 1

    def undo(self, cart: ShoppingCart) -> bool:
        """Отменяет последнее изменение"""
        if self._current_index <= 0:
            return False  # Нет предыдущих состояний

        self._current_index -= 1
        cart.restore_from_memento(self._mementos[self._current_index])
        return True

    def redo(self, cart: ShoppingCart) -> bool:
        """Возвращает отмененное изменение"""
        if self._current_index >= len(self._mementos) - 1:
            return False  # Нет последующих состояний

        self._current_index += 1
        cart.restore_from_memento(self._mementos[self._current_index])
        return True

    def can_undo(self) -> bool:
        """Проверяет, возможна ли отмена"""
        return self._current_index > 0

    def can_redo(self) -> bool:
        """Проверяет, возможен ли возврат"""
        return self._current_index < len(self._mementos) - 1

    def get_history_size(self) -> int:
        """Возвращает количество сохраненных состояний"""
        return len(self._mementos)

    def clear_history(self):
        """Очищает историю"""
        self._mementos.clear()
        self._current_index = -1


# Демонстрация работы
if __name__ == "__main__":
    # Создаем корзину и caretaker
    cart = ShoppingCart()
    caretaker = CartCaretaker(max_history_size=5)

    print("=== Демонстрация паттерна Memento для корзины покупок ===\n")

    # Сохраняем начальное состояние (пустая корзина)
    caretaker.save_state(cart)

    # Добавляем товары
    print("1. Добавляем товары в корзину:")
    cart.add_product(Product("1", "Ноутбук", 75000))
    caretaker.save_state(cart)
    print(cart)

    print("\n2. Добавляем еще товары:")
    cart.add_product(Product("2", "Мышь", 1500))
    cart.add_product(Product("3", "Клавиатура", 3000))
    caretaker.save_state(cart)
    print(cart)

    print("\n3. Изменяем количество товара:")
    cart.add_product(Product("1", "Ноутбук", 75000))  # Увеличиваем количество ноутбуков
    caretaker.save_state(cart)
    print(cart)

    print(f"\n4. История сохранена: {caretaker.get_history_size()} состояний")

    # Отменяем изменения
    print("\n5. Отменяем последнее изменение (возвращаем 1 ноутбук):")
    if caretaker.undo(cart):
        print(cart)

    print("\n6. Еще одна отмена (убираем мышь и клавиатуру):")
    if caretaker.undo(cart):
        print(cart)

    # Возвращаем изменения
    print("\n7. Возвращаем отмененное (добавляем мышь и клавиатуру):")
    if caretaker.redo(cart):
        print(cart)

    # Пытаемся отменить несколько раз
    print("\n8. Пытаемся отменить несколько раз:")
    for i in range(5):
        if caretaker.undo(cart):
            print(f"Отмена #{i + 1}: {cart.get_total_price()} руб.")
        else:
            print(f"Дальнейшая отмена невозможна")
            break

"""
Вопрос: Как вы будете хранить несколько точек сохранения (например, для отмены нескольких действий)? 
Какие ограничения могут возникнуть при использовании этого паттерна?

Ответ:

Хранение нескольких точек сохранения:

1. Используем список (стек) для хранения объектов Memento
2. Реализуем механизм навигации по истории с помощью текущего индекса
3. Ограничиваем максимальный размер истории для управления памятью
4. При превышении лимита удаляем самые старые сохранения

Ограничения паттерна Memento:

1. Потребление памяти: каждое сохранение состояния занимает память
2. Производительность: глубокое копирование больших объектов может быть медленным
3. Сложность управления: при большом количестве состояний сложно управлять историей
4. Ограниченная глубина отмены: приходится ограничивать количество хранимых состояний
5. Сериализация состояний: сложные объекты могут быть трудно сериализуемы
6. Временные затраты: создание и восстановление состояний требует времени

Дополнительные улучшения:

1. Сжатие данных: можно сжимать состояния перед сохранением
2. Инкрементальное сохранение: сохранять только изменения, а не полное состояние
3. Оптимизация памяти: использовать слабые ссылки или внешнее хранилище
4. Селективное сохранение: сохранять только важные изменения, а не каждое действие
5. Группировка операций: объединять несколько действий в одну точку сохранения

Пример оптимизации - инкрементальное сохранение:

class IncrementalCartMemento:
    def __init__(self, previous_state, changes):
        self._changes = changes  # Только изменения
        self._previous_state_ref = weakref.ref(previous_state) if previous_state else None
"""