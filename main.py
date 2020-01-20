import pygame
import sqlite3


def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return rect, frames

def load_image(name, color_key=None):
    image = pygame.image.load(name)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def all_sprites(*group):
    for i in group:
        i.draw(screen)


def delite(*groups):
    for i in groups:
        for j in i:
            j.kill()


def text_render(variables):
    text = []
    global progress, inventory, level, lives
    if variables[0] == '0':
        if [variables[1], variables[2]] == ['1', '2'] and not progress[0]:
            text = [f'- Ох, {name}, что это?', 'Это мой друг, Наталья Владимировна.. -',
                    '- Боже мой! Беги к Екатерине Александровне!', 'Она у себя на третьем этаже? -',
                    '- Да, конечно! И, держи ключи, от учительской, наверняка пригодится.',
                    'Спасибо, Наталья Владимировна! -']
            inventory += [Subject(load_image('data/предметы/ключи.png'), 0, 0, 'ключи')]
            progress[0] = True
        elif [variables[1], variables[2]] == ['3', '2'] and progress[0] and progress[-1] == 0:
            text = ['Екатерина Александровна, тут такое дело... мой друг.. -',
                    f'- Что с ним? Божечки.. {name}.. Наталья Владимиовна знает?',
                    'Можете чем-нибудь помочь? Она послала к Вам. -', '- Я не знаю... дай-ка взглянуть..',
                    '"Учительница взяла вашу рыбку"', '- Полагаю, нам нужно провести несколько реакций.. ',
                    'Что конкретно нужно? -', '- Мне нужен мой гидрато-кристал... Но малышня его у меня украла, не могу найти.',
                    'Я найду его! -']
            progress[-1] += 1
        elif [variables[1], variables[2]] == ['3', '2'] and progress[0]:
            for i in inventory:
                if i != 0:
                    if i.type == 'кристал' and progress[-1] == 1:
                        text = ['Кристал найден! -', '"Кристал у вас забрали"',
                                '- Кристало-гидрат. Отлично.. Сможешь сбегать к Наталье Владимировне?',
                                'А что нужно? -', '- Ключ от учительской. Точнее, мел, который там находится.',
                                'Скоро буду с мелом! -']
                        del inventory[inventory.index(i)]
                        i.kill()
                        i = 0
                        progress[-1] += 1
                        break
                    elif i.type == 'коробка_мела' and progress[-1] == 2:
                        text = [f'- Вот и ты, {name}!', 'Вот мел. -', '"коробки забрали из ваших рук"', '- Сейчас похимичим..',
                                '"Она достала еще колбу с маленькими кристалами и бутылку с кислотой"',
                                '"Вы испугались за своего друга"', '- С ним все будет хорошо. Он учит мой предмет.',
                                '"Учительница посмеялась, а реакция пошла, вспенивая аквариум"',
                                '"из под пены на вас посмотрели уже разумные глаза, из под чешую начала проступать кожа."',
                                '- Это только начало!', '|ВЫ ПРОШЛИ УРОВЕНЬ 1|']
                        del inventory[inventory.index(i)]
                        progress = [0 for x in progress]
                        level += 1
                        mel.progress = level
                        break
        else:
            text = [f'- {name}, уйди. Я временно занята.']
            lives -= 0.5
    elif variables[0] == '1':
        if [variables[1], variables[2]] == ['3', '2'] and  progress[-1] == 0:
            text = [f'- И так, {name}, у нас впереди еще два этапа.', 'И что для них нужно? -',
                    '- Для начала: электроустановка', 'Мне идти к Галине Яколевне!? -',
                    '- Да. Но попробуй ее задобрить... Предложи чай. Она любит.']
            for i in inventory:
                if i.type == 'чай':
                    text += ['Отлично. Я как раз подхватил его в учительской -']
                    break
            if text[-1][-1] != '-':
                text += ['Где я вам его возьму? -', '- Возьми в учительской.']
            progress[-1] += 1
        elif [variables[1], variables[2]] == ['3', '2'] and progress[-1] == 1:
            for i in inventory:
                if i.type == 'электроустановка':
                    text = ['- Отлично! И можешь забрать мою колбу у Юлии Сергеевны?', 'Она у себя? -',
                            '- Да, на первом, конечно же. Бeги давай, я пока всю подключу']
                    del inventory[inventory.index(i)]
                    progress[-1] += 1
                    break
                else:
                    text = ['Жду твою электроустановку']
        elif [variables[1], variables[2]] == ['3', '2'] and progress[-1] == 2 and progress[1] == 1:
            listik = False
            if 'колба' in [x.type for x in inventory] and 'листик' in [x.type for x in inventory]:
                text = ['- Отлично! О, она как раз передала тебе то, что нужно.',
                        '"Она заталкивает лист в колбу, добавляя несколько химикатов"',
                        '"Пена вновь скрывает вашь обзор"',
                        '"После чего вашему взору ваш друг открывает уже получеловеком, полурыбой."', '|ВЫ ПРОШЛИ УРОВЕНЬ 2|']
                del inventory[[x.type for x in inventory].index('колба')]
                del inventory[[x.type for x in inventory].index('листик')]
                progress = [0 for x in progress]
                level += 1
                mel.progress = level
            else:
                text = ['- Жду колбу.']
        elif [variables[1], variables[2]] == ['1', '4'] and progress[-1] == 2:
            text = [f'- {name}, ты от Катеньки? Я сейчас! Наталья Владимировна мне все рассказала!',
                    'Спасибо, Юлия Сергеевна! -', '"Вскоре учительница отдает вам одну из колб."',
                    '- Вот. И я точно знаю, вам это нужно будет.', '"Она оставляет в ваших руках лист с какого-то растения"']
            progress[1] = 1
            subject = Subject(load_image('data/предметы/листик.png'), 0, 0, 'листик')
            inventory += [Subject(load_image('data/предметы/листик.png'), 0, 0, 'листик'),
                          Subject(load_image('data/предметы/колба.png'), 100, 100, 'колба')]
        elif [variables[1], variables[2]] == ['2', '2'] and progress[-1] == 1:
            if 'чай' in [x.type for x in inventory]:
                text = ['- Привет, дорогой! Это что там у тебя?', 'Чай, Галина Яковлена. -', '- А давайка ты мне его отдашь? А я дам электроустановку.',
                         'Откуда вы знаете? -', '- Наталья Владимировна, дитячко.', 'Хорошо, я согласен. -',
                        '"Вы обменялись предметами"']
                inventory += [Subject(load_image('data/предметы/электроустановка.png'), 0, 0, 'электроустановка')]
                del inventory[[x.type for x in inventory].index('чай')]
            else:
                text = ['Хэй, Галина Яковлевна! Нам очень нужна ваша установка! -', 'Я не отдам, она мне еще нужна!',
                         '"Ваше настроение падает. Но у вас еще есть попытки."']
                lives -= 1
        else:
            text = [f'- {name}, уйди. Я временно занята.']
            lives -= 0.5
    if variables[0] == '2':
        if [variables[1], variables[2]] == ['3', '2']:
            if progress[-1] == 0:
                text = ['- И так.. Осталось немного, но. Нам нужно кое-что, из соседнего кабинета,', '- Чего просто так не достать. Цветок у Елены Александровны',
                        'А что в нем особенного? Мы не можем найти такой же в саду? -',
                        '- Этот экзотический. Он будет ехать по почте недели. Твой друг может не дожить']
                progress[-1] += 1
            if progress[-1] == 1 and 'цветок' in [x.type for x in inventory]:
                if 'ножницы' not in [x.type for x in inventory]:
                    text = ['- Отлично. И сбегайка за ножницами, к Ларисе Юрьевне.']
                else:
                    text = ['- Наконец-то! Выйди. Пахнуть будет неприятно.',
                            '"Вы выходите, даже из коридора чувствуя неприятный запах"',
                            '"Войдя через пять минут вы видите друга и обнимаете его', '|ВЫ ПРОШЛИ ИГРУ|']
                    level = 3
        elif [variables[1], variables[2]] == ['3', '4'] and progress[-1] == 1:
            if progress[-2] == 1:
                text = ['Елена Александровна! Дайте пожалуйтса ваш цветок.. Для друга. -',
                        '- Я конечно сопереживаю твоему другу. ',
                        '- Но ты знаешь, как я не люблю шпоры. Так что ты их не получишь']
                lives = 0
            if progress[-2] == 0:
                text = ['Елена Александровна! Дайте пожалуйтса ваш цветок.. Для друга. -',
                        '- конечно! Ты молодец, не стала давать шпоры той крысе.',
                        '- Забирай цветок']
                inventory += [Subject(load_image('data/предметы/цветок.png'), 0, 0, 'цветок')]
                progress[-3] = 1
        elif [variables[1], variables[2]] == ['2', '4'] and progress[-1] == 1:
            text = ['Лариса Юрьевна, можно ножницы? -','- Да, конечно, забирай!']
            inventory += [Subject(load_image('data/предметы/ножницы.png'), 0, 0, 'ножницы')]
        elif [variables[1], variables[2]] == ['с', 'т']:
            if not student_flag[0]:
                text = ['- Хэй! Помоги пожалуйста!', 'Что надо, пацан? -', '- Помоги. У меня контрольная! Ты старше классом, знаешь ответы']
                student_flag[0] = True
            elif student_flag[1]:
                text = ['"Вы забрали у парня листик и написали на нем ответы"', '- Спасибо!', 'Да не за что, пацан. -']
                progress[-2] = 1
            elif not student_flag[1]:
                text = ['Не, пацан, прости, мне спешить нужно! -']
    for i in range(len(text)):
        if text[i][0] == '-':
            text[i] = pygame.font.Font(None, 25).render(text[i], 1, (255, 255, 255)),\
                      (290, 305 + i * (300 // len(text) + 5))
        elif text[i][-1] == '-':
            text_str = pygame.font.Font(None, 25).render(text[i], 1, (255, 255, 255))
            text[i] = (text_str, (890 - text_str.get_width(),
                                  305 + i * (300 // len(text) + 5)))
        elif text[i][0] == '|':
            text_str = pygame.font.Font(None, 40).render(text[i], 1, (255, 255, 255))
            text[i] = (text_str, (774 - text_str.get_width() // 2, 700))
        else:
            text_str = pygame.font.Font(None, 25).render(text[i], 1, (255, 255, 255))
            text[i] = (text_str, (574 - text_str.get_width() // 2,
                                  305 + i * (300 // len(text) + 5)))
    global count_stud
    if ((student_flag == [True, False] and level == 2 and progress[-3] != 1 and
         count_stud == 0 and 'ст' in variables)):
        count_stud += 1
        text += [(pygame.font.Font(None, 40).render('помогать', 1, (255, 255, 255)), (20, 700)), (pygame.font.Font(None, 40).render('не помогать', 1, (255, 255, 255)),
                                                                                                  (1000, 700))]
    global new_say
    new_say = text
    return text


def say(variables):
    fon = load_image('data/вывод.png')
    fon = fon, (width // 2 - fon.get_width() // 2, height // 2 - fon.get_height() // 2)
    screen.blit(*fon)
    close_btn = Button(load_image('data/выход_кнопка.png'), fon[1][0] + fon[0].get_width() - 60, fon[1][1],
                       'выход_из_говорилки', others, 1)
    teachers.draw(screen)
    mel.cur_frame = level * 7
    mel.update()
    mel.rect.x += 100
    hero.draw(screen)
    if coord_hero == [3, 4]:
        variables = f'{level}ст'
    if new_say is True:
        return text_render(variables)
    else:
        return new_say


def pause(type=''):
    fon = pygame.transform.scale(load_image('data/пауза_фон.png'), (width, height))
    screen.blit(fon, (0, 0))
    if type == 'help':
        texts = helping()
    elif type == 'invenotry':
        texts = []
        fon = load_image('data/инвентарь.png')
        screen.blit(fon, (0, 0))
        for i in range(len(inventory)):
            if inventory[i] != 0 and inventory is not None:
                inventory[i].add(subjects)
                inventory[i].rect.x, inventory[i].rect.y = 75 + (i % 3) * 400, 75 + (i % 2) * 100
        subjects.draw(screen)
    elif type == 'say':
        mel.rect.x, mel.rect.y = 748, 330
        global count
        count = 0
        texts = say(f'{level}{coord_hero[-2]}{coord_hero[-1]}')
    elif type == 'win':
        btn = Button(load_image('data/кнопка_заставка.png'), 20, 700, 'НАЧАТЬ ЗАНОВО', others, 2)
        btn = Button(load_image('data/кнопка_заставка.png'), 800, 700, 'ВЫЙТИ', others, 2)
        texts = [(pygame.font.Font(None, 60).render('ВЫ ВЫИГРАЛИ!!', 1, (255, 255, 255)), (400, 200)),
                 (pygame.font.Font(None, 60).render('НАЧАТЬ ЗАНОВО!', 1, (255, 255, 255)), (80, 700)),
                 (pygame.font.Font(None, 60).render('ВЫЙТИ!', 1, (255, 255, 255)), (860, 700))]
    elif type == 'lose':
        btn = Button(load_image('data/кнопка_заставка.png'), 20, 700, 'НАЧАТЬ ЗАНОВО', others, 1)
        btn = Button(load_image('data/кнопка_заставка.png'), 800, 700, 'ЗАГРУЗИТЬ', others, 1)
        texts = [(pygame.font.Font(None, 60).render('ВЫ ПРОИГРАЛИ!!', 1, (255, 255, 255)), (400, 200)),
                 (pygame.font.Font(None, 60).render('НАЧАТЬ ЗАНОВО!', 1, (255, 255, 255)), (80, 700)),
                 (pygame.font.Font(None, 60).render('ВЫЙТИ!', 1, (255, 255, 255)), (860, 700))]
    else:
        texts = ['ПОМОЩЬ', 'СОХРАНИТЬСЯ', 'ВЫЙТИ']
        for i in range(3):
            btn = Button(load_image('data/кнопка_заставка.png'), 350, 300 + 5 * i + 103 * i, texts[i], others, 2)
            texts[i] = pygame.font.Font(None, 60).render(texts[i], 1, (255, 255, 255))
            texts[i] = tuple([texts[i]] + [(btn.rect.x + (btn.rect.w - texts[i].get_width()) // 2, btn.rect.y + (btn.rect.h - texts[i].get_height()) // 2)])
        texts += [(pygame.font.Font(None, 60).render(f'{name}: {level + 1} уровень. HP: {lives}', 1, (255, 255, 255)), (10, 10))]
    others.draw(screen)
    func = [screen.blit(*text) for text in texts]


def helping():
    fon = load_image('data/вывод.png')
    fon = fon, (width // 2 - fon.get_width() // 2, height // 2 - fon.get_height() // 2)
    screen.blit(*fon)
    close_btn = Button(load_image('data/выход_кнопка.png'), fon[1][0] + fon[0].get_width() - 60, fon[1][1], 'выход_из_помощи', others, 1)
    text = ['Brother For Brother: Брат за Брата',
            'Ваш лучший друг по совершеной случайности оказывается в беде,',
            'И вы можете найти того, кто поможет ему спастись.',
            'Найдите этого человека и помогите ему спасти вашего друга,',
            'Попутно не разозлив остальных!',
            '- Что бы двигаться, жмите на стрелки на клавиатуре.',
            '- Что бы открыть инвентарь, жмите Е.',
            '- Что бы переходить на локацию, жмите направленную на нее стрелку.',
            '- Что бы заговорить с персонажами, жмите знак, появляющийся над ними.',
            '- Что бы взять предмет, нажмите на него.',
            'При выходе из игры все достижения автоматически сохраняются.', 'Обратная связь: Наира Акобян: https://vk.com/yfbhf']
    for i in range(len(text)):
        text[i] = pygame.font.Font(None, 23).render(text[i], 1, (255, 255, 255)), (fon[1][0] + 20, fon[1][1] + 20 + i * 30)
    return text


def fon_create():
    subject = ''
    global coord_hero
    delite(arrows)
    if coord_hero[0] in list(range(1, 6)):
        fon = pygame.transform.scale(load_image(f'data/стена_этаж{coord_hero[0]}.png'), (width, height))
        if mel.rect.x < 100 and coord_hero[1] != 1:
            arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), -90), 50, 300, 'влево')
        elif mel.rect.x > 900 and coord_hero[1] != 5:
            arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), 90), 1050, 300, 'вправо')
        else:
            if mel.rect.x < 300 and coord_hero[1] == 1:
                if coord_hero[0] == 2:
                    arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), -180), 430, 150,
                                   'лестница_вверх')
                    arrow = Arrows(load_image('data/Стрела.png'), 430, 500, 'лестница_вниз')
                elif coord_hero[0] == 1:
                    arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), -180), 150, 500,
                                   'лестница_вверх')
                else:
                    arrow = Arrows(load_image('data/Стрела.png'), 230, 150, 'лестница_вниз')
            elif mel.rect.x > 600 and coord_hero[1] == 5:
                if coord_hero[0] == 2:
                    arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), -180), 710, 150,
                                   'лестница_вверх')
                    arrow = Arrows(load_image('data/Стрела.png'), 710, 500, 'лестница_вниз')
                elif coord_hero[0] == 1:
                    arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), -180), 950, 500,
                                   'лестница_вверх')
                else:
                    arrow = Arrows(load_image('data/Стрела.png'), 860, 500, 'лестница_вниз')
            else:
                for j in doors:
                    if pygame.sprite.spritecollideany(j, hero):
                        arrow2 = Arrows(load_image('data/Стрела.png'), j.rect.x + (j.rect.w // 2), j.rect.y - 150,
                                        j.type)
                        break
        delite(doors, tables, boards, teacher_desk, others, stairs, desks, teachers, subjects, say_btns)
        if coord_hero[1] == 1:
            if coord_hero[0] == 1:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 0, 0)
            if coord_hero[0] == 2:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 0, 13)
            if coord_hero[0] == 3:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 0, 120)
            door = Door(load_image('data/дверь_туалет.png'), 540, 128, 'туалет')
        elif coord_hero[1] == 5:
            if coord_hero[0] == 1:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 1050, 0)
            if coord_hero[0] == 2:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 800, 13)
            if coord_hero[0] == 3:
                stair = Stairs(load_image(f'data/лестница_этаж{coord_hero[0]}.png'), 970, 120)
            door = Door(load_image('data/дверь_туалет.png'), 340, 128, 'туалет')
        elif coord_hero[1] == 3:
            if coord_hero[0] == 1:
                door = Door(load_image('data/парадная_дверь.png'), 340, 210, 'столовая')
            elif coord_hero[0] == 2:
                door = Door(load_image('data/парадная_дверь.png'), 340, 210, 'спортзал')
            elif coord_hero[0] == 3:
                door = Door(load_image('data/парадная_дверь.png'), 340, 210, 'учительская')
            table = Table(load_image('data/таблички.png'), 810, 240, coord_hero[1] - 2, coord_hero[0] - 1)
        else:
            if coord_hero == [3, 4] and level == 2 and progress[-3] != 1:
                student = Teacher(100, 330, 10, 'ученик')
                if pygame.sprite.collide_rect(mel, student):
                    saying_btn = Eyes(load_image('data/разговаривать.png'), student.rect.x + student.rect.w / 2,
                                      student.rect.y - 250,
                                      (int(coord_hero[-1]), int(coord_hero[-2])), say_btns)
            door = Door(load_image('data/дверь_в_кабинет.png'), 340, 210, 'класс')
            table = Table(load_image('data/таблички.png'), 710, 240, coord_hero[1] - 2, coord_hero[0] - 1)
    else:
        delite(doors, tables, boards, teacher_desk, others, stairs, desks, teachers, say_btns, subjects)
        if coord_hero[-1] not in ['1', '2', '3', '4', '5'] and coord_hero[:-2] not in ['стол учителя', 'парта',
                                                                                       'доска']:
            if coord_hero == 'ключи':
                coord_hero = 'учительская'
            fon = pygame.transform.scale(load_image(f'data/{coord_hero}.png'), (width, height))
            if coord_hero == 'столовая':
                if len(inventory) == 0 or 'кристал' not in [x.type for x in inventory]:
                    subject = Subject(load_image('data/предметы/кристал.png'), 116, 733, 'кристал')
            if coord_hero == 'учительская':
                if (len(inventory) == 0 or 'коробка_мела' not in [x.type for x in inventory]) and level == 0:
                        subject = Subject(load_image('data/предметы/коробка_мела.png'), 420, 560, 'коробка_мела')
                if (len(inventory) == 0 or 'чай' not in [x.type for x in inventory]) and level in [1, 0]:
                    subject = Subject(load_image('data/предметы/чай.png'), 580, 610, 'чай')
        elif coord_hero[:-2] in ['стол учителя', 'парта', 'доска']:
            fon = pygame.transform.scale(load_image(f'data/фон {coord_hero[:-2]}.png'), (width, height))
            arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), 90), 1050, 300, 'вправо')
        else:
            fon = pygame.transform.scale(load_image(f'data/{coord_hero[:-2]}.png'), (width, height))
            if coord_hero[:-2] == 'класс':
                element = Elements(load_image('data/стол учителя.png'), 0, 560, teacher_desk, 'стол учителя')
                element3 = Elements(load_image('data/тумба.png'), 0, 0, boards, 'доска')
                element1 = Teacher(100, 330, (int(coord_hero[-1]), int(coord_hero[-2])), load_image('data/учителя.png'))
                if pygame.sprite.collide_rect(mel, element):
                    saying_btn = Eyes(load_image('data/разговаривать.png'), element.rect.x + element.rect.w / 2, element.rect.y - 250,
                                    (int(coord_hero[-1]), int(coord_hero[-2])), say_btns)
                    if left:
                        global count
                        count = 0
        if mel is not None and mel.rect.x > 900 and coord_hero[1] != 5:
            arrow = Arrows(pygame.transform.rotate(load_image('data/Стрела.png'), 90), 1050, 300, 'вправо')
    return fon


def input_(texts):
    fon = load_image('data/ввод.png')
    screen.blit(fon, (200, 300))
    for i in range(len(texts)):
        text = pygame.font.Font(None, 30).render(texts[i][0], 1, (255, 255, 255))
        if text.get_width() > 500:
            text = pygame.font.Font(None, 25).render(texts[i][0], 1, (255, 255, 255))
        screen.blit(text, (texts[i][1]))
    pygame.display.flip()


def zastavka():
    fon = pygame.transform.scale(load_image('data/заставка.png'), (width, height))
    screen.blit(fon, (0, 0))
    texts = ['НАЧАТЬ ИГРУ', 'ПОМОЩЬ', 'ВЫХОД']
    for i in range(3):
        x = Button(load_image('data/кнопка_заставка.png'), 0, 520 + i * 130, texts[i], btn, 2)
    running = True
    helping_flag = False
    while running:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in btn:
                    if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                            range(i.rect.y, i.rect.y + 1 + i.rect.h)):
                        if i.text == 'НАЧАТЬ ИГРУ':
                            return 'continue'
                        elif i.text == 'ПОМОЩЬ':
                            helping_flag = True
                        elif i.text == 'ВЫХОД':
                            return False
                        click = True
                        break
                if not click:
                    for i in others:
                        if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                                range(i.rect.y, i.rect.y + 1 + i.rect.h)):
                            if i.text == 'выход_из_помощи':
                                helping_flag = False
                        break
            if event.type == pygame.MOUSEMOTION:
                for i in btn:
                    i.unclicked()
                for i in btn:
                    if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                            range(i.rect.y, i.rect.y + 1 + i.rect.h)):
                        i.clicked()
        screen.blit(fon, (0, 0))
        btn.draw(screen)
        for i in btn:
            text = pygame.font.Font(None, 60).render(i.text, 1, (255, 255, 255))
            screen.blit(text,
                        (i.rect.x + (i.rect.w - text.get_width()) // 2, i.rect.y +(i.rect.h - text.get_height()) // 2))
        if helping_flag:
            pause('help')
        pygame.display.flip()


def update_players_list(btn, players, choice, delit, cur):
    names, progress, passwords = (cur.execute("SELECT name FROM players_progress").fetchall(),
                                  cur.execute("SELECT level FROM players_progress").fetchall(),
                                  cur.execute("SELECT password FROM players").fetchall())
    x = Button(load_image('data/добавить_игрока.png'), 912, 443, '', btn, 2)
    for i in range(len(names)):
        if progress[i][0] == 3:
            x = Button(load_image('data/игрок в списке.png'), 32, 524 + i * 71, f'{names[i][0]}\tПобедитель',
                       players, 1)
            x = Button(load_image('data/удалить_игрока.png'), 871, 524 + i * 71, names[i][0], delit, 2)
        else:
            x = Button(load_image('data/игрок в списке.png'), 32, 524 + i * 71, f'{names[i][0]}\t{progress[i][0] + 1}', players, 1)
            x = Button(load_image('data/выбрать_игрока.png'), 758, 524 + i * 71, names[i][0], choice, 2)
            x = Button(load_image('data/удалить_игрока.png'), 871, 524 + i * 71, names[i][0], delit, 2)
    func = [x.add(btn) for x in players]
    func = [x.add(btn) for x in choice]
    func = [x.add(btn) for x in delit]
    return btn, players, choice, delit, names, progress, passwords


def delete(name):
    fail = sqlite3.connect('players_progress/players.db')
    cur = fail.cursor()
    cur.execute(f"DELETE FROM players_progress WHERE name='{name}'")
    cur.execute(f"DELETE FROM players WHERE name='{name}'")
    cur.execute(f"DELETE FROM players_inventory WHERE players='{name}'")
    fail.commit()
    fail.close()


def choice_player():
    fail = sqlite3.connect('players_progress/players.db')
    cur = fail.cursor()
    fon = pygame.transform.scale(load_image('data/заставка.png'), (width, height))
    screen.blit(fon, (0, 0))
    spisok = load_image('data/список игроков.png')
    screen.blit(spisok, (23, 510))
    players, delit, choice, btn = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    btn, players, choice, delit, names, progress, passwords = update_players_list(btn, players, choice, delit, cur)
    fail.commit()
    running = True,
    player_input = False, False
    redaction, delit_flag = False, False
    player_name, player_password = '', ''
    input_close_btn = None
    while running[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and (player_input[0] or player_input[1] or redaction or delit_flag):
                if event.key == 13:
                    if (len(player_name) > 6 and player_input[0]) or player_input[1]:
                        if len(player_password) > 6 and player_input[1]:
                            cur.execute("INSERT INTO players_progress(name, coord_hero, math, biology, physik, IT, russian, student, chemestry, lives, level)" +
                                        f" VALUES('{player_name}', '1, 3', 0, 0, 0, 0, 0, 0, 0, 3, 0)")
                            cur.execute(f"INSERT INTO players(name, password) VALUES('{player_name}', '{player_password}')")
                            cur.execute(f"INSERT INTO players_inventory(players) VALUES('{player_name}')")
                            fail.commit()
                            return 'game', [1, 3], Hero(load_image('data/Mel_Sprite.png', -1), 7, 3,
                                                        500, 500, 0), [], [False]*6 + [0], player_name, 3
                        else:
                            player_input = False, True
                    elif len(player_name) > 6:
                        if player_password == check_pass:
                            if redaction:
                                progress_hero = cur.execute(f"SELECT * FROM players_progress WHERE name='{player_name}'").fetchall()[-1]
                                inventory = cur.execute(f"SELECT * FROM players_inventory WHERE players='{player_name}'").fetchall()[-1][1:]
                                if str(progress_hero[1][0]).isalpha():
                                    coord_hero = progress_hero[1]
                                else:
                                    coord_hero = [int(x) for x in progress_hero[1].split(', ')]
                                inventory = [Subject(load_image(f'data/предметы/{x}.png'), 0, 0, x) for x in inventory if x != 0 and x is not None]
                                return 'game', coord_hero, \
                                          Hero(load_image('data/Mel_Sprite.png', -1), 7, 3, 500, 500, progress_hero[-1]), inventory, progress_hero[
                                                                                                              2:-2], progress_hero[0], progress_hero[-2]
                            if delit_flag:
                                cur.execute(f"DELETE FROM players_progress WHERE name='{i.text}'")
                                cur.execute(f"DELETE FROM players WHERE name='{i.text}'")
                                cur.execute(f"DELETE FROM players_inventory WHERE players='{i.text}'")
                                delit_flag, player_name, player_password = False, '', ''
                                fail.commit()
                        else:
                            checked = True
                elif event.key == pygame.K_BACKSPACE:
                    if player_input[0]:
                        player_name = player_name[:-1]
                    elif (player_input[1] or redaction or delit_flag):
                        player_password = player_password[:-1]
                else:
                    if len(player_name) <= 12 and player_input[0]:
                        player_name += str(event.unicode)
                    elif len(player_password) <= 12 and (player_input[1] or redaction or delit_flag):
                        player_password += str(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not player_input[0] and not player_input[1] and not delit_flag and not redaction:
                    if event.pos[0] in list(range(width - 59, width)) and event.pos[1] in list(range(0, 47)):
                        return False, 'заставка'
                    else:
                        for i in btn:
                            if event.pos[0] in list(range(i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                                    range(i.rect.y + 1 + i.rect.h)):
                                if i in choice:
                                    player_name = i.text
                                    checked = False
                                    check_pass = cur.execute(
                                        f"SELECT password FROM players WHERE name='{player_name}'").fetchone()[0]
                                    redaction= True
                                elif i in delit:
                                    player_name = i.text
                                    delit_flag = True
                                    checked = False
                                    check_pass = cur.execute(
                                        f"SELECT password FROM players WHERE name='{player_name}'").fetchone()[0]
                                elif i not in players:
                                    if len(names) < 5:
                                        player_input = True, False
                                break
                elif input_close_btn is not None:
                    if ((event.pos[0] in list(range(input_close_btn.rect.x, input_close_btn.rect.x + 1 + input_close_btn.rect.w)) and
                         event.pos[1] in list(range(input_close_btn.rect.y, input_close_btn.rect.y + 1 + input_close_btn.rect.h)))):
                        player_input = False, False
                        new, redaction, delit_flag = False, False, False
                        player_name, player_password = '', ''
                        input_close_btn = None
        delite(choice, delit, players, btn)
        btn, players, choice, delit, names, progress, passwords = update_players_list(btn, players, choice, delit, cur)
        fail.commit()
        if player_input[0] or player_input[1] or delit_flag or redaction:
            if input_close_btn is None:
                input_close_btn = Button(load_image('data/выход_кнопка.png'), 781, 307, '', btn, 1)
            delite(btn)
            input_close_btn.add(btn)
            texts = [['', (260, 270)], ['', (280, 380)], ['', (297, 475)],
                     ['Нажмите ENTER для продолжения', (290, 575)]]
            if player_input[0]:
                texts[1], texts[2] = ['Введите имя игроку, содержащее более 6 символов:', (280, 380)], [player_name, (297, 475)]
            if player_input[1] or delit_flag or redaction:
                texts[1][0], texts[2][0] = f'Введите пароль {player_name}, содержащий более 6 символов:', player_password
                if not player_input[1] and checked:
                     texts[0][0] = 'Пароль неверный'
            input_(texts)
            btn.draw(screen)
        else:
            screen.blit(fon, (0, 0))
            screen.blit(spisok, (23, 510))
            for i in players:
                screen.blit(pygame.font.Font(None, 30).render(i.text.split()[0], 1, (255, 255, 255)), (i.rect.x + 5, i.rect.y + 5))
                screen.blit(pygame.font.Font(None, 30).render(i.text.split()[1] + ' уровень', 1, (255, 255, 255)),
                            (i.rect.x + 325, i.rect.y + 5))
            btn.draw(screen)
        screen.blit(load_image('data/выход_кнопка.png'), (width - 59, 0))
        pygame.display.flip()


def save(inventory):
    inventory = list(inventory)
    for i in range(len(inventory)):
        if inventory[i] is None:
            inventory[i] = 0
    fail = sqlite3.connect('players_progress/players.db')
    cur = fail.cursor()
    progressers = ['math', 'biology', 'physik', 'IT', 'russian', 'student', 'chemestry']
    for i in range(len(inventory)):
        if inventory[i] != 0 and inventory[i] is not None:
            cur.execute(f'UPDATE players_inventory SET slot_{i + 1}="{inventory[i].type}" WHERE players="{name}"')
        else:
            cur.execute(f'UPDATE players_inventory SET slot_{i + 1}="{0}" WHERE players="{name}"')
    if str(coord_hero[0]).isalpha():
        cur.execute(
            f'UPDATE players_progress SET coord_hero="{coord_hero}" WHERE name="{name}"')
    else:
        cur.execute(
            f'UPDATE players_progress SET coord_hero="{coord_hero[0]}, {coord_hero[1]}" WHERE name="{name}"')
    cur.execute(f'UPDATE players_progress SET lives={lives}')
    for i in range(len(progressers)):
        if progressers[i] == 'chemestry':
            cur.execute(f'UPDATE players_progress SET {progressers[i]} = {progress[i]} WHERE name="{name}"')
        else:
            if progress[i]:
                cur.execute(f'UPDATE players_progress SET {progressers[i]}=1 WHERE name="{name}"')
            else:
                cur.execute(f'UPDATE players_progress SET {progressers[i]}=0 WHERE name="{name}"')
    cur.execute(f'UPDATE players_progress SET lives={lives} WHERE name="{name}"')
    cur.execute(f'UPDATE players_progress SET level={level} WHERE name="{name}"')
    fail.commit()
    fail.close()


def numbers_for_teach(numbx, numby):
    if numbx == 2:
        numbx = 0
    else:
        numbx = 1
    numby -= 1
    return numbx * 3, numby * 6


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, progress):
        super().__init__(hero)
        self.rect, self.frames = cut_sheet(sheet, columns, rows)
        self.cur_frame = progress * 7
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.napr = True
        self.say = False
        self.progress = progress

    def update(self):
        self.cur_frame %= 7
        if numb % 3 == 0 and iteration and not self.say:
            if self.cur_frame == 1:
                self.cur_frame = 3
            else:
                self.cur_frame = 1
        if not iteration and self.image != self.frames[0] and not self.say:
            self.cur_frame = 0
            self.cur_frame_past = 1
        if self.say and numb % 3 == 0:
            if self.cur_frame != 0:
                while self.cur_frame != 0:
                    if self.cur_frame == 2:
                        self.cur_frame = 4
                    if self.cur_frame == 1:
                        self.cur_frame = 3
                    else:
                        self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    clock.tick(5)
            else:
                if self.cur_frame == 5:
                    self.cur_frame = 6
                else:
                    self.cur_frame = 5
            self.cur_frame_past = 1
        self.cur_frame += self.progress * 7
        self.image = self.frames[self.cur_frame]

    def drive(self, left, right, count):
        if left != right:
            if right:
                if self.rect.x + 1 + self.rect.w < width:
                    self.rect.x += count
                    if not self.napr:
                        self.frames = [pygame.transform.flip(x, True, False) for x in self.frames]
                        self.image = self.frames[self.cur_frame]
                        self.napr = True
            if left:
                if self.rect.x - 1 > 0:
                    self.rect.x -= count
                    if self.napr:
                        self.frames = [pygame.transform.flip(x, True, False) for x in self.frames]
                        self.image = self.frames[self.cur_frame]
                        self.napr = False


def click_did(coord_hero, mel, event):
    global inventory
    not_arrow, not_subjects = True, True
    for i in arrows:
        if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                range(i.rect.y, i.rect.y + 1 + i.rect.h)):
            if str(type(coord_hero)) == "<class 'list'>":
                if i.type == 'влево':
                    coord_hero[1] -= 1
                elif i.type == 'вправо':
                    coord_hero[1] += 1
                elif i.type == 'туалет':
                    coord_hero = f'туалет{coord_hero[0]}{coord_hero[1]}'
                elif i.type == 'класс':
                    coord_hero = f'класс{coord_hero[0]}{coord_hero[1]}'
                elif i.type == 'лестница_вверх':
                    coord_hero[0] += 1
                elif i.type == 'лестница_вниз':
                    coord_hero[0] -= 1
                else:
                    if i.type != 'учительская':
                        coord_hero = i.type
                    else:
                        for i in inventory:
                            if i.type == 'ключи':
                                coord_hero = i.type
                if i.type == 'влево':
                    mel.rect.x = 900
                elif i.type == 'вправо':
                    mel.rect.x = 50
                elif 'лестница' not in i.type:
                    mel.rect.x = 900
                    mel.drive(True, False, 0)
            else:
                if coord_hero[:-2] in ['туалет', 'класс']:
                    coord_hero = [int(coord_hero[-2]), int(coord_hero[-1])]
                if coord_hero == 'столовая':
                    coord_hero = [1, 3]
                if coord_hero == 'спортзал':
                    coord_hero = [2, 3]
                if coord_hero == 'учительская':
                    coord_hero = [3, 3]
                if coord_hero[:-2] in ['стол учителя', 'парта', 'доска']:
                    mel = Hero(load_image('data/Mel_Sprite.png', -1), 7, 3, 500, 500, level)
                    coord_hero = f'класс{coord_hero[-2:]}'

                mel.rect.x = 500
            not_arrow = False
            break
    if not_arrow:
        if not inventory_open:
            for i in subjects:
                if event.pos[0] in list(range(i.rect.x,
                                              i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(range(i.rect.x,
                                                                                                   i.rect.y + 1 + i.rect.h)):
                    inventory += [i]
                    i.kill()
                    not_subjects = False
                    break
            if not_subjects:
                for i in say_btns:
                    if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(
                            range(i.rect.y, i.rect.y + 1 + i.rect.h)):
                        global pause_flag, saying
                        pause_flag = True
                        saying = True
                        break
    return mel, coord_hero


class Arrows(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__(arrows)
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Subject(pygame.sprite.Sprite):
    def __init__(self, image, x, y, teacher):
        super().__init__(subjects)
        self.image = image
        self.type = teacher
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Door(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        super().__init__(doors)
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Stairs(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(stairs)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Table(pygame.sprite.Sprite):
    def __init__(self, image, x, y, numbx, numby):
        super().__init__(tables)
        self.rect = pygame.Rect(0, 0, image.get_width() // 3,image.get_height() // 3)
        frame_location = (self.rect.w * numbx, self.rect.h * numby)
        self.image = image.subsurface(pygame.Rect(frame_location, self.rect.size))
        self.rect = self.rect.move(x, y)
        self.napr = True


class Elements(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group, name):
        super().__init__(group)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y, text, group, count):
        super().__init__(group)
        self.text = text
        self.rect, self.frames = cut_sheet(image, count, 1)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def clicked(self):
        self.image = self.frames[-1]

    def unclicked(self):
        self.image = self.frames[0]


class Eyes(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type, group):
        super().__init__(group)
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Teacher(pygame.sprite.Sprite):
    def __init__(self, x, y, type, image):
        super().__init__(teachers)
        if image == 'ученик':
            self.image = load_image('data/ученик.png')
            self.rect = self.image.get_rect()
        else:
            self.type = sum(numbers_for_teach(type[0], type[1]))
            self.rect, self.frames = cut_sheet(image, 6, 3)
            self.numb = self.type
            self.image = self.frames[self.type]
        self.rect = self.rect.move(x, y)


pygame.init()
size = width, height = 1200, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Brother-For-Brother')
hero = pygame.sprite.Group()
others = pygame.sprite.Group()
btn = pygame.sprite.Group()
subjects = pygame.sprite.Group()
running = False, 'заставка'
while running is not False:
    if running == (False, 'заставка'):
        pygame.display.flip()
        running = zastavka()
    elif running == 'continue':
        pygame.display.flip()
        running = choice_player()
    elif running is not False:
        running, coord_hero, mel, inventory, progress, name, lives = True, running[1], running[2], list(running[3]),\
                                                              list(running[4]), running[5], running[6]
        level = mel.progress
        teachers = pygame.sprite.Group()
        arrows = pygame.sprite.Group()
        doors = pygame.sprite.Group()
        stairs = pygame.sprite.Group()
        tables = pygame.sprite.Group()
        teacher_desk = pygame.sprite.Group()
        desks = pygame.sprite.Group()
        boards = pygame.sprite.Group()
        clock = pygame.time.Clock()
        say_btns = pygame.sprite.Group()
        student_flag = [False, False]
        count_stud = 0
        win_flag, lose_flag = False, False
        first_iter = True
        iteration, right, left, pause_flag, numb, helping_flag, saying, inventory_open, new_say = False, \
                                                                                                  False, False, False, 0, \
                                                                                                  False, False, False, True
        while running is True:
            if level == 3 and not win_flag:
                win_flag, pause_flag = True, True
            elif lives == 0 and not lose_flag:
                lose_flag, pause_flag = True, True
            pause_btn = Button(load_image('data/пауза_кнопка.png'), width - 80, 0, '', others, 1)
            if (not win_flag and not lose_flag) or first_iter or saying:
                first_iter = False
                fon = fon_create()
                pause_btn = Button(load_image('data/пауза_кнопка.png'), width - 80, 0, '', others, 1)
                screen.blit(fon, (0, 0))
                all_sprites(doors, tables, boards, teachers, teacher_desk, others, stairs, hero, arrows, say_btns, desks, subjects)
                if pause_flag:
                    delite(arrows)
                    all_sprites(doors, tables, boards, teachers, teacher_desk, others, stairs, hero, arrows, desks)
                    if helping_flag:
                        pause('help')
                    elif inventory_open:
                        pause('invenotry')
                    elif saying:
                        pause('say')
                    elif win_flag:
                        pause('win')
                    elif lose_flag:
                        pause('lose')
                    else:
                        pause()
                count = 30
            else:
                delite(arrows)
                all_sprites(doors, tables, boards, teachers, teacher_desk, others, stairs, hero, arrows, desks)
                if win_flag:
                    pause('win')
                elif lose_flag:
                    pause('lose')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(inventory)
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        right, iteration = True, True
                    if event.key == pygame.K_LEFT:
                        left, iteration = True, True
                    if event.key == 101:
                        if pause_flag:
                            pause_flag = False
                            inventory_open = False
                        else:
                            pause_flag = True
                            inventory_open = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        right = False
                        iteration = False
                    if event.key == pygame.K_LEFT:
                        left = False
                        iteration = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in list(range(pause_btn.rect.x, pause_btn.rect.x + 1 + pause_btn.rect.w)) and event.pos[1] in list(range(pause_btn.rect.y, pause_btn.rect.y + 1 + pause_btn.rect.h)):
                        if pause_flag and not helping_flag and not saying and not inventory_open:
                            pause_flag = False
                        elif not pause_flag:
                            pause_flag = True
                    elif saying and coord_hero == [3, 4] and count_stud == 1:
                        if event.pos[0] in list(range(20, 250)) and event.pos[1] in list(range(700, 800)):
                            student_flag = [True, True]
                            new_say = True
                        elif event.pos[0] in list(range(1000, 1200)) and event.pos[1] in list(range(700, 800)):
                            student_flag = [True, False]
                            new_say = True
                        else:
                            for i in others:
                                if i.text == 'выход_из_говорилки':
                                    mel.rect.y = 500
                                    saying = False
                                    pause_flag = False
                                    new_say = True
                                    break
                    elif pause_flag:
                        for i in others:
                            if event.pos[0] in list(range(i.rect.x, i.rect.x + 1 + i.rect.w)) and event.pos[1] in list(range(i.rect.y, i.rect.y + 1 + i.rect.h)):
                                if i.text == 'СОХРАНИТЬСЯ':
                                    save(inventory)
                                if i.text == 'ВЫЙТИ':
                                    print('k')
                                    if not lose_flag:
                                        save(inventory)
                                    running = False
                                if i.text == 'ПОМОЩЬ':
                                    helping_flag = True
                                if i.text == 'выход_из_помощи':
                                    helping_flag = False
                                if i.text == 'выход_из_говорилки':
                                    mel.rect.y = 500
                                    saying = False
                                    pause_flag = False
                                    new_say = True
                                if i.text == 'НАЧАТЬ ЗАНОВО' and (win_flag or lose_flag):
                                    if win_flag:
                                        save(inventory)
                                    if lose_flag:
                                        delete(name)
                                    print('l')
                                    running = (False, 'заставка')
                                    break
                                if i.text == 'ЗАГРУЗИТЬ':
                                    running = 'continue'
                                    break
                    else:
                        mel, coord_hero = click_did(coord_hero, mel, event)
            if mel is not None and not pause_flag:
                if iteration:
                    numb += 1
                    mel.drive(left, right, count)
                mel.update()
            pygame.display.flip()
            clock.tick(10)
