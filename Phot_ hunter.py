import configparser
import PySimpleGUI as Sg
import pandas
import sys
import os

sys.path.append(os.path.join('..'))
from Library.yandex import Yandex
from Library.vk import VkUser
from Library.WorkingOnFiles import WorkingWithFiles

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token_vk = config["settings"]["token_vk"]
    token_yandex = config["settings"]["token_yandex"]
    data = ['id', 'username']
    count_photo_loading = 1
    progressbar = [
        [Sg.ProgressBar(0, orientation='h', size=(51, 10), key='progressbar')]
    ]
    outputwin = [[Sg.Output(size=(78, 20))]]
    section1 = [
        [Sg.Text('День рождения:  '), Sg.Input(key='birth_day')],
        [Sg.Text('Месяц рождения:'), Sg.Input(key='birth_month')],
        [Sg.Text('Год рождения:    '), Sg.Input(key='birth_year')],
        [Sg.Text('Родной город:     '), Sg.Input(key='city')]
    ]
    layout = [
        [Sg.Frame('Progress', layout=progressbar)],
        [Sg.Text('Выберете по какому параметру будет осуществляться поиск '
                 'пользователя VK:')],
        [Sg.Combo(values=data, default_value=['id'], size=(20, 1),
                  key='user_data', enable_events=True)],
        [Sg.Text('Введите данные пользователя VK:')],
        [Sg.InputText(key='data_vk')],
        [Sg.pin(Sg.Column(section1, key='Sec_1', visible=False))],
        [Sg.Text('Введите количество фотографий для скачивания:')],
        [Sg.Input(5, key='count_photo')],
        [Sg.Frame('Output', layout=outputwin)],
        [Sg.Submit('Start'), Sg.Cancel()]
    ]
    window = Sg.Window('Photo hunter', layout)
    progress_bar = window['progressbar']

    while True:
        event, values = window.read(timeout=10)
        if values['user_data'] == 'id':
            window['Sec_1'].update(visible=False)
            data_vk = values['data_vk']
        if values['user_data'] == 'username':
            window['Sec_1'].update(visible=True)
        if event == 'Cancel' or event is None:
            break
        if event == 'Start':
            if values['count_photo'].isdigit() is False:
                print('Неправильно указано количество фотографий.')
                continue
            if values['user_data'] == 'username':
                data_vk = VkUser(token_vk, '5.131').get_user_id(
                    values['data_vk'], values['birth_day'],
                    values['birth_month'], values['birth_year'], values['city'])
                if data_vk == 0:
                    continue
            name_folder = Yandex(token_yandex).folder()
            list_response = VkUser(token_vk, '5.131').get_photo(data_vk)
            if list_response == 0:
                continue
            report_file = []
            for i, el in enumerate(list_response['items']):
                if int(el['likes']['count']) not in [value['file_name']
                                                     for value in report_file]:
                    Yandex(token_yandex).upload_from_internet(
                        el['sizes'][-1]['url'], el['likes']['count'],
                        name_folder)
                    report_file.append({
                        "file_name": el['likes']['count'],
                        "size": el['sizes'][-1]['type']})
                else:
                    result_s = str(pandas.to_datetime(el['date'], unit='s')
                                   ).replace(':', '-')
                    Yandex(token_yandex).upload_from_internet(
                        el['sizes'][-1]['url'],
                        str(el['likes']['count']) + ' ' +
                        result_s, name_folder)
                    report_file.append({
                        "file_name": [str(el['likes']['count']) +
                                      ' ' + result_s],
                        "size": el['sizes'][-1]['type']})
                current_count = int(list_response['count']) \
                    if int(list_response['count']) < int(values['count_photo']) \
                    else int(values['count_photo'])
                progress_bar.Update(current_count=current_count,
                                    max=current_count)
                progress_bar.UpdateBar(i + 1)
                count_photo_loading += 1
                if count_photo_loading > int(values['count_photo']):
                    break
            WorkingWithFiles().file_write(report_file)
            print('Все файлы загружены успешно.')
            count_photo_loading = 1
    window.close()
