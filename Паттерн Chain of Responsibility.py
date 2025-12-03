from abc import ABC, abstractmethod
from typing import Optional


# Класс запроса на возврат
class RefundRequest:
    def __init__(self, request_id: str, order_id: str, customer_id: str,
                 amount: float, reason: str, priority: int = 1):
        self.request_id = request_id
        self.order_id = order_id
        self.customer_id = customer_id
        self.amount = amount
        self.reason = reason
        self.priority = priority  # 1-низкий, 2-средний, 3-высокий
        self.status = "pending"
        self.handled_by = None
        self.comments = []

    def add_comment(self, handler: str, comment: str):
        self.comments.append(f"{handler}: {comment}")

    def __str__(self):
        return f"Запрос на возврат {self.request_id} (Заказ: {self.order_id}, Сумма: {self.amount} руб.)"


# Абстрактный класс обработчика
class Handler(ABC):
    def __init__(self):
        self._next_handler: Optional['Handler'] = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def _can_handle(self, request: RefundRequest) -> bool:
        pass

    @abstractmethod
    def _process_request(self, request: RefundRequest) -> bool:
        pass

    def handle_request(self, request: RefundRequest) -> bool:
        print(f"{self.__class__.__name__}: Получен запрос {request.request_id}")

        if self._can_handle(request):
            print(f"{self.__class__.__name__}: Обрабатываю запрос")
            if self._process_request(request):
                request.handled_by = self.__class__.__name__
                return True

        if self._next_handler:
            print(f"{self.__class__.__name__}: Передаю запрос следующему обработчику")
            return self._next_handler.handle_request(request)

        print(f"{self.__class__.__name__}: Не могу обработать запрос и нет следующего обработчика")
        return False


# Конкретные обработчики
class ManagerHandler(Handler):
    def _can_handle(self, request: RefundRequest) -> bool:
        # Менеджер может обрабатывать запросы до 5000 руб и низкого/среднего приоритета
        return request.amount <= 5000 and request.priority <= 2

    def _process_request(self, request: RefundRequest) -> bool:
        request.status = "approved_by_manager"
        request.add_comment("Менеджер", f"Одобрен возврат {request.amount} руб. Причина: {request.reason}")
        print(f"Менеджер: Одобрил возврат {request.amount} руб. для заказа {request.order_id}")
        return True


class SupervisorHandler(Handler):
    def _can_handle(self, request: RefundRequest) -> bool:
        # Руководитель может обрабатывать запросы до 20000 руб и любого приоритета
        return request.amount <= 20000

    def _process_request(self, request: RefundRequest) -> bool:
        if request.priority == 3:  # Высокий приоритет
            request.status = "expedited_approval"
            request.add_comment("Руководитель", f"Срочно одобрен возврат {request.amount} руб.")
            print(f"Руководитель: Срочно одобрил возврат {request.amount} руб.")
        else:
            request.status = "approved_by_supervisor"
            request.add_comment("Руководитель", f"Одобрен возврат {request.amount} руб.")
            print(f"Руководитель: Одобрил возврат {request.amount} руб.")
        return True


class SupportHandler(Handler):
    def __init__(self, technical_issues_only: bool = False):
        super().__init__()
        self.technical_issues_only = technical_issues_only

    def _can_handle(self, request: RefundRequest) -> bool:
        # Служба поддержки обрабатывает технические вопросы или любые запросы, если не technical_issues_only
        if self.technical_issues_only:
            return "технический" in request.reason.lower() or "брак" in request.reason.lower()
        return True

    def _process_request(self, request: RefundRequest) -> bool:
        if "технический" in request.reason.lower() or "брак" in request.reason.lower():
            request.status = "technical_refund"
            request.add_comment("Поддержка", f"Возврат по технической причине: {request.reason}")
            print(f"Поддержка: Обработал технический возврат")
            return True
        else:
            request.status = "referred_to_support"
            request.add_comment("Поддержка", f"Запрос направлен на дополнительную проверку")
            print(f"Поддержка: Направил запрос на дополнительную проверку")
            return True


# Обработчик по умолчанию для необработанных запросов
class DefaultHandler(Handler):
    def _can_handle(self, request: RefundRequest) -> bool:
        # Этот обработчик всегда может обработать запрос (последний в цепочке)
        return True

    def _process_request(self, request: RefundRequest) -> bool:
        request.status = "escalated"
        request.add_comment("Система", "Запрос эскалирован для ручной обработки")
        print(f"Обработчик по умолчанию: Запрос эскалирован для ручной обработки")
        # Здесь может быть логика уведомления администратора
        return True


# Класс для построения цепочки ответственности
class RefundProcessor:
    def __init__(self):
        self._chain = self._build_chain()

    def _build_chain(self) -> Handler:
        # Строим цепочку: Менеджер -> Руководитель -> Поддержка -> Обработчик по умолчанию
        manager = ManagerHandler()
        supervisor = SupervisorHandler()
        support = SupportHandler()
        default = DefaultHandler()

        manager.set_next(supervisor).set_next(support).set_next(default)
        return manager

    def process_refund(self, request: RefundRequest) -> bool:
        print(f"\n=== Обработка запроса на возврат ===")
        print(f"Запрос: {request}")
        print(f"Причина: {request.reason}")
        print(f"Приоритет: {request.priority}")

        result = self._chain.handle_request(request)

        print(f"Результат: {request.status}")
        print(f"Обработан: {request.handled_by}")
        if request.comments:
            print("Комментарии:")
            for comment in request.comments:
                print(f"  - {comment}")

        return result


# Система уведомлений для необработанных запросов
class NotificationSystem:
    @staticmethod
    def notify_unhandled_request(request: RefundRequest):
        print(f"!!! ВНИМАНИЕ: Запрос {request.request_id} не был обработан системой !!!")
        print(f"Требуется ручное вмешательство администратора")

    @staticmethod
    def log_request(request: RefundRequest, success: bool):
        status = "УСПЕХ" if success else "НЕУДАЧА"
        print(f"[ЛОГ] Запрос {request.request_id}: {status}, Статус: {request.status}")


# Демонстрация работы
if __name__ == "__main__":
    print("=== Демонстрация паттерна Chain of Responsibility для обработки возвратов ===\n")

    processor = RefundProcessor()

    # Тестовые запросы
    requests = [
        RefundRequest("REF001", "ORD1001", "CUST123", 3000, "Не подошел размер", 1),
        RefundRequest("REF002", "ORD1002", "CUST124", 15000, "Технический брак", 3),
        RefundRequest("REF003", "ORD1003", "CUST125", 50000, "Не понравился товар", 2),
        RefundRequest("REF004", "ORD1004", "CUST126", 8000, "Ошибка в заказе", 2),
        RefundRequest("REF005", "ORD1005", "CUST127", 1000, "Длительная доставка", 1)
    ]

    for request in requests:
        success = processor.process_refund(request)
        NotificationSystem.log_request(request, success)

        if not success or request.status == "escalated":
            NotificationSystem.notify_unhandled_request(request)

        print("-" * 50)

"""
Вопрос: Как вы будете обрабатывать ситуацию, когда запрос не обрабатывается ни одним из обработчиков? 
Какие изменения внесете в систему?

Ответ:

Обработка необработанных запросов:

1. Добавление обработчика по умолчанию (DefaultHandler):
   - Всегда может обработать запрос
   - Эскалирует запрос для ручной обработки
   - Логирует инцидент

2. Система уведомлений:
   - Уведомляет администраторов о необработанных запросах
   - Ведет детальное логирование всех запросов

3. Мониторинг и аналитика:
   - Отслеживание статистики необработанных запросов
   - Анализ причин, почему запросы не обрабатываются

Изменения в системе для улучшения обработки:

1. Расширение критериев обработки:
   - Более гибкие условия в методах _can_handle()
   - Возможность настройки пороговых значений

2. Резервные механизмы:
   - Несколько цепочек для разных типов запросов
   - Фолбэк обработчики для специфических случаев

3. Улучшенное логирование:
   - Трассировка прохождения запроса по цепочке
   - Детальная информация о причинах отказа на каждом этапе

4. Динамическая настройка цепочки:
   - Возможность изменять порядок обработчиков в runtime
   - Добавление/удаление обработчиков без остановки системы

5. Обратная связь:
   - Уведомление клиентов о статусе их запроса
   - Прогресс обработки в реальном времени
"""