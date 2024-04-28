import pygame
import requests


def check_color(col):
    try:
        _ = pygame.Color(f'#{col}')
        return True
    except Exception:
        return False

def check_width(wid):
    try:
        if 10 >= int(wid) >= 0:
            return True
        return False
    except Exception:
        return False

def check_route(rou):
    try:
        if len(routes[rou]['points']) >= 2:
            return True
        return False
    except Exception:
        return False

def check_mark(m):
    try:
        mar, siz, con = marks[m]['style'], marks[m]['size'], marks[m]['content']
        if (mar == 'pm' and ((siz in ['s', 'm'] and con in [*map(str, range(100)), '']) or
                             (siz == 'l' and con in [*map(str, range(101)), '']))) or \
                (mar == 'pm2' and siz in ['m', 'l'] and 99 >= int(con) >= 0) or \
                (mar == 'vk' and siz in ['m']) or \
                (mar in ['flag', 'org', 'comma', 'round', 'home', 'work', 'ya_ru']):
            return True
        return False
    except Exception:
        return False


def display_button(x, y, txt):
    text = font.render(txt, True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 191, 255), (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20))
    screen.blit(text, (x, y))
    # print(x - 10, x + text.get_width() + 10, y - 10, y + text.get_height() + 10)

def display_text_field(x, y, txt, default=''):
    text = font.render(txt if txt else default, True, (0, 191, 255) if txt else (128, 128, 128))
    pygame.draw.rect(screen, (0, 191, 255), (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
    screen.blit(text, (x, y))
    # print(x - 10, x + text.get_width() + 10, y - 10, y + text.get_height() + 10)


longitude, latitude = '0', '0'
map_file = 'map.png'
text = 'search'
route = 0
mark = 0
org_m = ''
texts = {'search': '', 'address': '', 'file': '', 'rc0': '', 'rw0': '', 'rc1': '', 'rw1': '', 'rc2': '', 'rw2': '',
         'rbc0': '', 'rbw0': '', 'rbc1': '', 'rbw1': '', 'rbc2': '', 'rbw2': '',
         'mc0': '', 'mc1': '', 'mc2': '', 'mc3': '', 'mc4': '', 'mc5': '', 'mc6': '', 'mc7': '', 'mc8': '', 'mc9': '',
         'org': ''}
routes = [{'points': [], 'color': 'FF0000FF', 'width': '5', 'b_width': '0', 'b_color': '00000000'},
          {'points': [], 'color': '00FF00FF', 'width': '5', 'b_width': '0', 'b_color': '00000000'},
          {'points': [], 'color': '0000FFFF', 'width': '5', 'b_width': '0', 'b_color': '00000000'}]
mark_col = {'pm': ['wt', 'do', 'db', 'bl', 'gn', 'gr', 'lb', 'nt', 'or', 'pn', 'rd', 'vv', 'yw', 'a', 'b'],
            'pm2': ['wt', 'do', 'db', 'bl', 'gn', 'dg', 'gr', 'lb', 'nt', 'or', 'pn', 'rd', 'vv', 'yw', 'a', 'b', 'org',
                    'dir', 'blyw'],
            'flag': [''], 'vk': ['bk', 'gr'], 'org': [''], 'comma': [''], 'round': [''], 'home': [''], 'work': [''],
            'ya_ru': ['']}
mark_siz = {'pm': ['s', 'm', 'l'], 'pm2': ['m', 'l'], 'flag': [''], 'vk': ['m'], 'org': [''], 'comma': [''],
            'round': [''], 'home': [''], 'work': [''], 'ya_ru': ['']}
marks = [{'ll': '', 'style': 'pm', 'color': 'wt', 'size': 'm', 'content': ''} for _ in range(10)]



map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    'll': f'{longitude},{latitude}',
    'z': '1',
    'pl': '',
    'pt': '',
    'l': 'map'}


geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
    'geocode': texts['search'],
    'format': 'json'}


search_api_server = "https://search-maps.yandex.ru/v1/"
search_params = {
    'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
    'text': '',
    'lang': 'ru_RU',
    'll': map_params['ll'],
    'results': '3',
    'type': 'biz'
}


response = requests.get(map_api_server, params=map_params)
with open(map_file, mode='wb') as f:
    f.write(response.content)


pygame.init()
font = pygame.font.Font(None, 20)
screen = pygame.display.set_mode((1000, 1000))
screen.fill((255, 255, 255))
screen.blit(pygame.image.load(map_file), (20, 70))
display_button(30, 30, 'Открыть')
display_button(120, 30, 'Сохранить')
display_text_field(223, 30, '', 'Имя файла')
display_text_field(30, 550, '', 'Поиск места')
display_button(566, 550, 'Искать')
display_text_field(30, 603, 'Адрес: ')
display_button(650, 30, 'Прицел на карте')
display_button(797, 30, 'Обводка линии')
display_button(650, 80, 'Переключить линию: 1')
display_button(840, 80, 'Сохранить настройки')
display_text_field(650, 134, '', 'Цвет линии HEX')
display_text_field(798, 134, '', 'Толщина линии')
display_text_field(650, 187, '', 'Цвет обводки HEX')
display_text_field(814, 187, '', 'Толщина обводки')
display_button(650, 241, 'Добавить точку')
display_button(794, 241, 'Удалить точку')
display_button(650, 295, 'Стиль метки: pm')
display_button(797, 295, 'Цвет метки: wt')
display_button(650, 348, 'Размер метки: s')
display_text_field(793, 348, '', 'Контент метки')
display_button(650, 401, 'Добавить метку')
display_button(794, 401, 'Удалить метку')
display_text_field(30, 657, '', 'Поиск по организациям')
display_button(566, 657, 'Искать')
pygame.display.flip()
route_color = pygame.Color(0, 0, 0)
move = False
shift = False
typing = False
pos = False
aim = False
dot = False
mk = False
org_search = False
change = False
running = True
while running:
    for event in pygame.event.get():
        # Выход
        if event.type == pygame.QUIT:
            running = False
        # Колесо мыши - изменение масштаба
        elif event.type == pygame.MOUSEWHEEL:
            map_params['z'] = str(int(map_params.get('z')) + event.y)
            change = True
        # Левая кнопка мыши
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Перемещение
            if 20 <= event.pos[0] <= 620 and 70 <= event.pos[1] <= 520:
                move = True
            # Кнопки - Файл
            elif 20 <= event.pos[0] <= 95 and 20 <= event.pos[1] <= 50: # Открыть
                typing = False
            elif 120 <= event.pos[0] <= 200 and 20 <= event.pos[1] <= 50: # Сохранить
                typing = False
                with open(f'{texts["file"]}.txt', mode='wt', encoding='utf-8') as f:
                    f.write('-map-\n')
                    f.write(f'{map_params["ll"]};{map_params["z"]};{map_params["l"]}')
                    f.write('-routes-\n')
                    for el in routes:
                        f.write(f'{el["color"]};{el["width"]};{el["b_width"]};{el["b_color"]};{el["points"]}\n')
                    f.write('-marks-\n')
                    for el in marks:
                        f.write(f'{el["ll"]};{el["style"]};{el["color"]};{el["size"]};{el["content"]}\n')
                    f.write('-end-\n')
            elif 213 <= event.pos[0] <= 305 and 20 <= event.pos[1] <= 50: # Файл
                text = 'file'
                typing = True
            # Кнопки - Поиск
            elif 20 <= event.pos[0] <= 215 and 540 <= event.pos[1] <= 573: # Поиск
                text = 'search'
                typing = True
            elif 556 <= event.pos[0] <= 620 and 540 <= event.pos[1] <= 573: # Искать
                pos = True
                typing = False
                change = True
            # Кнопки - Маршруты
            elif 640 <= event.pos[0] <= 767 and 20 <= event.pos[1] <= 54: # Прицел
                aim = not aim
                typing = False
                change = True
            elif 787 <= event.pos[0] <= 909 and 20 <= event.pos[1] <= 54: # Обводка
                typing = False
                dot = True
            elif 640 <= event.pos[0] <= 810 and 70 <= event.pos[1] <= 104: # Линия
                typing = False
                dot = True
                route = (route + 1) % 3
                change = True
            elif 830 <= event.pos[0] <= 989 and 70 <= event.pos[1] <= 104: # Применить
                c, w = texts[f'rc{route}'], texts[f'rw{route}']
                routes[route]['color'] = c if check_color(c) else routes[route]['color']
                routes[route]['width'] = w if check_width(w) else routes[route]['width']
                bc, bw = texts[f'rbc{route}'], texts[f'rbw{route}']
                routes[route]['b_color'] = bc if check_color(bc) else routes[route]['b_color']
                routes[route]['b_width'] = bw if check_width(bw) else routes[route]['b_width']
                dot = True
                change = True
            elif 640 <= event.pos[0] <= 768 and 124 <= event.pos[1] <= 157: # Цвет
                text = f'rc{route}'
                typing = True
            elif 788 <= event.pos[0] <= 912 and 124 <= event.pos[1] <= 157: # Толщина
                text = f'rw{route}'
                typing = True
            elif 640 <= event.pos[0] <= 785 and 177 <= event.pos[1] <= 210: # Цвет обводки
                text = f'rbc{route}'
                typing = True
            elif 804 <= event.pos[0] <= 945 and 177 <= event.pos[1] <= 210: # Толщина обводки
                text = f'rbw{route}'
                typing = True
            elif 640 <= event.pos[0] <= 764 and 231 <= event.pos[1] <= 265: # Добавить точку
                typing = False
                routes[route]['points'].append(f'{map_params["ll"]}')
            elif 784 <= event.pos[0] <= 899 and 231 <= event.pos[1] <= 265: # Удалить точку
                typing = False
                routes[route]['points'] = routes[route]['points'][:-1]
            # Кнопки - метки
            elif 640 <= event.pos[0] <= 767 and 285 <= event.pos[1] <= 319: # Стиль метки
                marks[mark]['style'] = list(mark_col.keys())[(list(mark_col.keys()).index(marks[mark]['style']) + 1) % 10]
                marks[mark]['color'] = mark_col[marks[mark]['style']][0]
                marks[mark]['size'] = mark_siz[marks[mark]['style']][0]
                change = True
            elif 787 <= event.pos[0] <= 902 and 285 <= event.pos[1] <= 318: # Цвет метки
                marks[mark]['color'] = mark_col[marks[mark]['style']]\
                    [(mark_col[marks[mark]['style']].index(marks[mark]['color']) + 1) % len(mark_col[marks[mark]['style']])]
                change = True
            elif 640 <= event.pos[0] <= 763 and 338 <= event.pos[1] <= 372: # Размер метки
                marks[mark]['size'] = mark_siz[marks[mark]['style']] \
                    [(mark_siz[marks[mark]['style']].index(marks[mark]['size']) + 1) % len(mark_siz[marks[mark]['style']])]
                change = True
            elif 783 <= event.pos[0] <= 896 and 338 <= event.pos[1] <= 371: # Контент метки
                text = f'mc{mark}'
                typing = True
            elif 640 <= event.pos[0] <= 764 and 391 <= event.pos[1] <= 425: # Добавить метку
                marks[mark]['ll'] = map_params['ll']
                marks[mark]['content'] = texts[f'mc{mark}']
                if not check_mark(mark):
                    marks[mark]['content'] = ''
                mark = (mark + 1) % 10
                mk = True
                change = True
            elif 784 <= event.pos[0] <= 908 and 391 <= event.pos[1] <= 425: # Удалить метку
                mark -= 1
                marks[mark]['ll'] = ''
                marks[mark]['style'], marks[mark]['color'], marks[mark]['size'] = 'pm', 'wt', 's'
                marks[mark]['content'], texts[f'mc{mark}'] = '', ''
                mk = True
                change = True
            elif 20 <= event.pos[0] <= 196 and 647 <= event.pos[1] <= 681: # Поиск организаций
                text = 'org'
                typing = True
            elif 556 <= event.pos[0] <= 620 and 647 <= event.pos[1] <= 680: # Искать
                org_search = True
                typing = False
                change = True
            else:
                typing = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            move = False
        elif event.type == pygame.MOUSEMOTION and move:
            rx, ry = event.rel[0], event.rel[1]
            lon, lat = map_params['ll'].split(',')
            lon = str(float(lon) - round(rx / int(map_params['z']) ** (3 if shift else 2)))
            lat = str(float(lat) + round(ry / int(map_params['z']) ** (3 if shift else 2)))
            map_params['ll'] = f'{lon},{lat}'
            change = True
        # Shift - уточнение перемещения
        elif event.type == pygame.KEYDOWN and event.key == pygame.KMOD_SHIFT and not typing:
            shift = True
        elif event.type == pygame.KEYUP and event.key == pygame.KMOD_SHIFT and not typing:
            shift = False
        elif event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_BACKSPACE:
                texts[text] = texts[text][:-1]
            elif event.key == pygame.K_RETURN:
                typing = False
            else:
                texts[text] += event.unicode
            change = True
    if org_search:
        try:
            search_params['text'] = texts['org']
            search_params['ll'] = map_params['ll']
            json_response = requests.get(search_api_server, params=search_params).json()
            organizations = json_response["features"]
            for i in range(len(organizations)):
                org_m += '~' if i != 0 else ''
                point = organizations[i]["geometry"]["coordinates"]
                org_m += f'{point[0]},{point[1]},pm2lbl{i + 1}'
            map_params['pt'] = org_m + map_params['pt']
        except Exception as exc:
            print(exc)
        org_search = False
    if pos:
        try:
            geocoder_params['geocode'] = texts['search']
            json_response = requests.get(geocoder_api_server, params=geocoder_params).json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            address = toponym['metaDataProperty']['GeocoderMetaData']['text']
            toponym_longitude, toponym_latitude = toponym['Point']['pos'].split(" ")
            map_params['ll'] = f'{toponym_longitude},{toponym_latitude}'
            texts['address'] = address
            change = True
            pos = False
        except Exception as exc:
            print(exc)
    if change:
        try:
            if dot:
                map_params['pl'] = ''
                for r in range(3):
                    if check_route(r):
                        map_params['pl'] += '~' if r != 0 else ''
                        map_params['pl'] += f'c:{routes[r]["color"]},w:{routes[r]["width"]},'
                        map_params['pl'] += f'bc:{routes[r]["b_color"]},bw:{routes[r]["b_width"]},'
                        map_params['pl'] += f'{",".join(routes[r]["points"])}'
                dot = False
            if mk:
                map_params['pt'] = f'{org_m}~' if org_m else ''
                for p in range(10):
                    if marks[p]['ll']:
                        map_params['pt'] += '~' if p != 0 else ''
                        map_params['pt'] += f'{marks[p]["ll"]},{marks[p]["style"]}{marks[p]["color"]}'
                        map_params['pt'] += f'{marks[p]["size"]}{marks[p]["content"]}'
                mk = False
            response = requests.get(map_api_server, params=map_params)
            with open(map_file, mode='wb') as f:
                f.write(response.content)
            screen.fill(pygame.Color(255, 255, 255))
            screen.blit(pygame.image.load(map_file), (20, 70))
            if aim:
                pygame.draw.rect(screen, pygame.Color(255, 0, 0), (315, 290, 10, 10), 1)
            display_button(30, 30, 'Открыть')
            display_button(120, 30, 'Сохранить')
            display_text_field(223, 30, texts['file'], 'Имя файла')
            display_text_field(30, 550, texts['search'], 'Поиск места')
            display_button(566, 550, 'Искать')
            display_text_field(30, 603, f'Адрес: {texts["address"]}')
            display_button(650, 30, 'Прицел на карте')
            display_button(797, 30, 'Обводка линии')
            display_button(650, 80, f'Переключить линию: {route + 1}')
            display_button(840, 80, 'Сохранить настройки')
            display_text_field(650, 134, texts[f'rc{route}'], 'Цвет линии HEX')
            display_text_field(798, 134, texts[f'rw{route}'], 'Толщина линии')
            display_text_field(650, 187, texts[f'rbc{route}'], 'Цвет обводки HEX')
            display_text_field(814, 187, texts[f'rbw{route}'], 'Толщина обводки')
            display_button(650, 241, 'Добавить точку')
            display_button(794, 241, 'Удалить точку')
            display_button(650, 295, f'Стиль метки: {marks[mark]["style"]}')
            display_button(797, 295, f'Цвет метки: {marks[mark]["color"]}')
            display_button(650, 348, f'Размер метки: {marks[mark]["size"]}')
            display_text_field(793, 348, f'{texts[f"mc{mark}"]}', 'Контент метки')
            display_button(650, 401, 'Добавить метку')
            display_button(794, 401, 'Удалить метку')
            display_text_field(30, 657, f'{texts["org"]}', 'Поиск по организациям')
            display_button(566, 657, 'Искать')
            change = False
            pygame.display.flip()
        except Exception as exc:
            print(map_params)
            print(exc)
pygame.quit()