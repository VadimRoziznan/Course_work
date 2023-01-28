import requests


class VkUser:

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {'access_token': token, 'v': version}

    def get_user_id(self, user_name=None, birth_day=None, birth_month=None,
                    birth_year=None, city=None):
        user_id = self.url + 'users.search'
        user_id_params = {'q': user_name, 'sort': 0, 'birth_day': birth_day,
                          'birth_month': birth_month, 'birth_year': birth_year,
                          'hometown': city}
        response = requests.get(user_id, params={**self.params,
                                                 **user_id_params}).json()
        if len(response.get('response').get('items')) < 1:
            print(f'Пользователь {user_name} не найден, данные '
                  f'введены не верно или не все поля заполнены. ')
            return 0
        else:
            return response['response']['items'][0]['id']


        # if str(response.get('response').get('items').get('id')).isdigit() is False:
        #     print(f'Пользователь {user_name} не найден, данные '
        #           f'введены не верно или не все поля заполнены. ')
        #     return 0
        # else:
        #     return response['response']['items'][0]['id']



    def get_photo(self, user_id):
        photos_url = self.url + 'photos.get'
        photos_params = {'owner_id': user_id, 'album_id': 'profile',
                         'extended': 1, 'photo_sizes': 1}
        response = requests.get(photos_url, params={**self.params,
                                                    **photos_params}).json()
        if response.get('error'):
            print(f'Пользователь не найден, данные '
                  f'введены не верно или не все поля заполнены.')
            return 0
        else:
            return response['response']
