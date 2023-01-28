import requests


class Yandex:

    host = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def folder(self, folder='Photo_from_vk'):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        params = {'path': f'{folder}', 'permanently': 'true'}
        requests.put(url, headers=self.get_headers(), params=params)
        return folder

    def upload_from_internet(self, file_url, file_name, folder):
        uri = "v1/disk/resources/upload/"
        url = self.host + uri
        params = {'path': f'/{folder}/{file_name}', 'url': file_url}
        response = requests.post(url, headers=self.get_headers(), params=params)
        if response.status_code == 202:
            return print(f'Загрузка файла {file_name} прошла успешно.')
        else:
            return print(f'Произошла ошибка.')
