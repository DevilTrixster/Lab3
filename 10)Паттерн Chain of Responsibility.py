from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def can_handle(self, request):
        pass

    @abstractmethod
    def process_request(self, request):
        pass

    def handle_request(self, request):
        if self.can_handle(request):
            self.process_request(request)
        elif self._next_handler:
            self._next_handler.handle_request(request)
        else:
            # Запрос не обработан ни одним обработчиком
            print(f"Запрос {request} не может быть обработан. Обратитесь в главный офис.")

class ManagerHandler(Handler):
    def can_handle(self, request):
        return request.get("amount", 0) <= 1000

    def process_request(self, request):
        print(f"Менеджер обработал запрос на возврат {request.get('amount')} руб.")

class SupervisorHandler(Handler):
    def can_handle(self, request):
        return request.get("amount", 0) <= 5000

    def process_request(self, request):
        print(f"Руководитель обработал запрос на возврат {request.get('amount')} руб.")

class SupportHandler(Handler):
    def can_handle(self, request):
        return request.get("amount", 0) <= 20000

    def process_request(self, request):
        print(f"Служба поддержки обработала запрос на возврат {request.get('amount')} руб.")

if __name__ == "__main__":
    manager = ManagerHandler()
    supervisor = SupervisorHandler()
    support = SupportHandler()

    manager.set_next(supervisor).set_next(support)

    requests = [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 3000},
        {"id": 3, "amount": 15000},
        {"id": 4, "amount": 25000}  # Этот запрос не будет обработан
    ]

    for req in requests:
        print(f"\nОбработка запроса {req['id']}:")
        manager.handle_request(req)

'''
1. Добавить завершающий обработчик по умолчанию в конец цепочки, который будет обрабатывать все
неподходящие запросы (например, записывать в лог, отправлять уведомление администратору).
2. В базовом классе Handler реализовать fallback-логику при отсутствии следующего обработчика, как сделано в примере выше.
3. Ввести механизм принудительной обработки запроса хотя бы одним обработчиком (например, последний в цепочке всегда принимает запрос, 
но с пометкой "особым случаем").
'''