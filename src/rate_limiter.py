import time
from threading import Lock, Semaphore


class RateLimiter:
    def __init__(self, min_interval, max_calls, period):
        self.min_interval = min_interval
        self.max_calls = max_calls
        self.period = period
        self.semaphore = Semaphore(max_calls)
        self.lock = Lock()
        self.call_times = []
        self.last_call = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.lock:
                current_time = time.time()

                # Удаляем старые записи времени вызовов, чтобы они не влияли на лимит
                self.call_times = [t for t in self.call_times if current_time - t < self.period]

                # Проверяем, нужно ли ждать, чтобы не превышать лимит количества запросов
                if len(self.call_times) >= self.max_calls:
                    time_to_wait = self.period - (current_time - self.call_times[0])
                    print(f"Превышен лимит запросов в минуту, ждем {time_to_wait:.2f} секунд.")
                    time.sleep(time_to_wait)
                    current_time = time.time()  # Обновляем текущее время после ожидания

                # Проверяем интервал между вызовами
                elapsed_time = current_time - self.last_call
                if elapsed_time < self.min_interval:
                    time_to_wait = self.min_interval - elapsed_time
                    print(f"Превышен лимит по времени между запросами, ждем {time_to_wait:.2f} секунд.")
                    time.sleep(time_to_wait)

                # Обновляем время последнего вызова
                self.last_call = time.time()
                self.call_times.append(self.last_call)

                # Делаем запрос с использованием семафора для ограничения параллельных вызовов
                with self.semaphore:
                    return func(*args, **kwargs)

        return wrapper