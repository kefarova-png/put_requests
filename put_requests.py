import requests


class GoogleMapTest:
    def __init__(self):  # Создаем атрибуты экземпляра класса
        # Параметры тестируемого сайта:
        self.BASE_URL = "https://rahulshettyacademy.com"
        self.KEY_PARAM = {"key": "qaclick123"}  # для всех запросов
        self.POST_RESOUSE = "/maps/api/place/add/json"
        self.post_body = {
            "location": {"lat": -38.383494, "lng": 33.427362},
            "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": ["shoe park", "shop"],
            "website": "http://google.com",
            "language": "French-IN",
        }
        self.GET_RESOUSE = "/maps/api/place/get/json"
        # Переменная для имени файла, в который будем писать:
        self.FILE_NAME = "place_ids.txt"

        self.PUT_RESOUSE = "/maps/api/place/update/json"

        # Шаблон Body для метода PUT (из документации):
        self.put_body = {
            "place_id": "c104d917f4b60e2c9a5feda6c9cbf279",
            "address": "100 Lenina street, RU",
            "key": "qaclick123"
        }

        self.post_url = f"{self.BASE_URL}{self.POST_RESOUSE}"  # путь для POST-запроса
        self.get_url = f"{self.BASE_URL}{self.GET_RESOUSE}"  # путь для GET-запроса
        self.put_url = f"{self.BASE_URL}{self.PUT_RESOUSE}"  # путь для PUT-запроса

    def put_positive_testing(self):
        print("\nПОЗИТИВНЫЙ СЦЕНАРИЙ ТЕСТИРОВАНИЯ PUT-ЗАПРОСА")
        # Создаем новый place_id для тестирования
        response = requests.post(self.post_url, params=self.KEY_PARAM, json=self.post_body)
        assert response.status_code == 200, (
            f"Провал! Сервер НЕ подтверждает создание place_id для тестирования. "
            f"Статус код ответа = {response.status_code}"
        )

        post_data = response.json()  # преобразуем ответ в JSON-словарь
        dynamic_pid = post_data.get("place_id")  # берем значение созданного place_id
        print(f"Локация с place_id = '{dynamic_pid}' успешно \n"
              f"создана сервером и будет использована при тестировании")

        real_put_body = self.put_body.copy()  # Сделаем копию, чтобы не перезаписать исходный
        real_put_body["place_id"] = dynamic_pid  # заменяем в шаблоне тела PUT-запроса place_id на созданный

        print("Пытаемся обновить параметр adress")
        put_response = requests.put(self.put_url, params=self.KEY_PARAM, json=real_put_body)  # PUT-запрос

        # Проверяем, что place_id обновлен по мнению сервера (код ответа 200)
        assert put_response.status_code == 200, (
            f"Провал! Обновление не произведено! Статус код ответа: {put_response.status_code}"
        )
        print("Успех! Сервер подтверждает обновление")

        # Проверяем GET-запросом, что обновляемый place_id имеет обновленный адрес:
        # 1) Сделаем копию словаря query_params, чтобы не перезаписать исходный KEY_PARAM
        query_params = self.KEY_PARAM.copy()
        # 2) Формируем query_params для GET-запроса:
        query_params["place_id"] = dynamic_pid
        # 3) шлём GET-запрос для проверки обновленного адреса у обновляемого place_id
        get_response = requests.get(self.get_url, params=query_params)
        # 4) Проверим статус ответа на GET-запрос:
        assert get_response.status_code == 200, (
            f"Провал! Сервер НЕ подтверждает существование тестируемой локации"
            f"Статус код ответа = {get_response.status_code}"
        )
        # 5) СРАВНИМ ПОЛУЧЕННЫЙ РЕЗУЛЬТАТ С ОЖИДАЕМЫМ
        # Берем обновленный адрес из тела PUT-запроса:
        put_address = self.put_body["address"]
        # Проверяем, что address из ответа на GET-запрос
        # равен put_address из ранее отправленного PUT-запроса:
        get_data = get_response.json()  # превращаем ответ от сервера в словарь
        # Читаем значение для address, которое сравниваем с ожидаемым put_address:
        assert get_data.get(
            "address"
        ) == put_address, f"Провал! Параметр address не соответствует обновлению"
        print("Успех! Параметр address соответствует произведенному обновлению")

    def put_negative_testing(self):
        print("\nНЕГАТИВНЫЙ СЦЕНАРИЙ ТЕСТИРОВАНИЯ PUT-ЗАПРОСА")
        # Попытаемся обновить НЕсуществующий place_id:
        unreal_place_id = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        # 1) Сделаем копию словаря query_params, чтобы не перезаписать исходный KEY_PARAM
        query_params = self.KEY_PARAM.copy()
        # 2) Формируем query_params для GET-запроса:
        query_params["place_id"] = unreal_place_id
        print(f'Попытаемся обновить НЕсуществующую локацию, \n'
              f'используя "НЕсуществующий" place_id = "{unreal_place_id}"')
        # 3) Отправляем PUT-запрос:
        put_response = requests.put(self.put_url, params=self.KEY_PARAM, json=self.put_body)
        # 4) СРАВНИМ ПОЛУЧЕННЫЙ РЕЗУЛЬТАТ С ОЖИДАЕМЫМ
        # Проверяем, что place_id НЕ найден по мнению сервера (код ответа 404)
        assert put_response.status_code == 404, (
            f'Провал! Cервер не ответил 404-й ошибкой на попытку обновления \n'
            f'НЕсуществующей локации с "НЕсуществующим" place_id = {unreal_place_id}! \m'
            f'Статус код ответа: {put_response.status_code}'
        )
        print(f"Успех! Сервер НЕ подтверждает обновление НЕсуществующей локации \n"
              f"(Статус код ответа: {put_response.status_code})")
        # 5) Проверим GET-запросом, что локация не создалась:
        # Сделаем копию словаря query_params, чтобы не перезаписать исходный KEY_PARAM
        query_params = self.KEY_PARAM.copy()
        # Формируем query_params для GET-запроса:
        query_params["place_id"] = unreal_place_id
        # Шлём GET-запрос для проверки существования такого place_id
        get_response = requests.get(self.get_url, params=query_params)
        # 4) Проверим статус ответа на GET-запрос:
        assert get_response.status_code != 200, (
            f"Провал! Сервер подтверждает обновление НЕсуществовавшей локации \n"
            f"с place_id = '{unreal_place_id}'. Статус код ответа = {get_response.status_code}"
        )
        print(f"Успех! Локация с place_id = '{unreal_place_id}' \n"
              f"проверочным GET-запроса не обнаружена. \n"
              f"(Статус код ответа = {get_response.status_code})")


test = GoogleMapTest()
test.put_positive_testing()
test.put_negative_testing()