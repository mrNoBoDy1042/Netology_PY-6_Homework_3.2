########################################################################################################################
# Task 3.2 - Использовать API Yandex translate для перевода файлов
# Exitcodes:
# 0 - нормальный выход
# 1 - Файл для перевода не найден
# 2 - Файл или папка с результатом перевода уже существует
########################################################################################################################
import requests
import os

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
API_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(resource_path, from_lang, to_lang='ru', result_path=''):
    """
    Перевод файла при помощи API Yandex Translate
    :param result_path:
    :param resource_path:
    :param from_lang:
    :param to_lang:
    :return:
    """
    text = ''

    # Находим файл и читаем его
    try:
        with open(resource_path) as f:
            text = f.read()

    # Если файл не найден, то кидаем ошибку и exitcode 1
    except FileNotFoundError:
        print('404 Файл не найден')
        exit(1)

    # Словарь заголовков для обращения к Yandex translate API
    options = {
        'key': API_KEY,
        'text': text,
        'lang': '{0}-{1}'.format(from_lang.lower(), to_lang),
    }

    # Обращаемся к API и сохраняем ответ в response
    response = requests.get(API_URL, params=options)

    # Если в качестве пути для сохранения результата ничего не передано, то возвращаем переведенный текст
    if result_path == '':
        return ''.join(response.json()['text'])

    # Иначе создаем файл с переводом
    else:
        # Создаем файл и сохраняем в него текст перевода
        try:
            # Создаем имя нового файла: имя исходного файла + _translated_to_ + язык на который был переведен + .txt
            with open('{0}_translated_to_{1}.txt'.format(
                    os.path.join(result_path, os.path.split(resource_path)[1][:-4:]), to_lang), 'w') as f:
                # Записываем в файл полученный текст
                f.write(''.join(response.json()['text']))
            # Возвращаем статус перевода
            return 'Перевод выполнен успешно'

        # Если файл с переводом уже есть, то выходим с exitcode 2
        except FileExistsError:
            print('406 Файл перевода уже существует')
            exit(2)


def get_txt_files(path_to_dir):
    """
    Получаем список txt файлов для перевода
    :param path_to_dir:
    :return:
    """
    txt_files = list(filter(lambda x: x.endswith('.txt'), os.listdir(path_to_dir)))
    return txt_files


def prepare_to_translate(path_to_source, path_to_result=''):
    """
    Процедура для обработки ввода. Если не передавать путь для сохранения файлов перевода, то превод выведется на экран
    :param path_to_result:
    :param path_to_source:
    :return:
    """

    # Если исходные данные -  папка, то получаем список txt файлов в ней
    if os.path.isdir(path_to_source):
        txt_files = get_txt_files(path_to_source)

        # Если путь для сохранения файлов не пуст, то создаем папку для сохранения файлов перевода по этому пути
        if path_to_result != '':
            try:
                # Создаем путь до папки: путь для сохранения результатов + название папки, отправленной на перевод +
                # + _translated
                path_to_result = os.path.join(path_to_result,
                                              ''.join(path_to_source.split(os.path.sep)[-2:]) + '_translated')
                # Создаем папку с результатами перевода
                os.mkdir(path_to_result)

            # Если папка уже есть, то ывыходим с exitcode 2
            except OSError:
                print('406 Переданная папка уже переведена')
                exit(2)

        # Переводим каждый файл
        for file in txt_files:
            print(file)
            print(translate_it(file, file[:-4:], result_path=path_to_result))
            print('------------------------------------------------------------')

    # Если исхадные данные - путь к файлу, то переводим только его
    else:
        # Получаем название файла, он же язык
        language_of_file = os.path.split(path_to_source)[1][:-4:]
        # Отправляем путь к файлу, язык файла и путь
        print(translate_it(path_to_source, language_of_file, result_path=path_to_result))


# Проверка работоспособности абсолютного пути. Файлы перевода создаются в указанном пути, если оставить его пустым,
# то перевод выведется на экран
# prepare_to_translate('P:\\Netology python homeworks\\Homework 3.2\\', 'p:\\')

# Работа с относительными путями. Файлы перевода сохранятся в той же папке, что и файл .py
launch_path = os.path.dirname(__file__)
prepare_to_translate(launch_path, launch_path)