import logging
import time

import requests
from aiogram import Bot, Dispatcher, executor, types
# from telethon import TelegramClient
# from telethon import functions
import nest_asyncio
# import emoji
import json
import datetime
from pyqiwip2p import QiwiP2P

# data = {}

myp = 'ead5390e4cd10728b73bc60c5c712075'
my = "e71b4a2d045899fac91649d6ca1ebe1e"
qiwi_api = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjU0dWExdS0wMCIsInVzZXJfaWQiOiI3OTE4NDYxMDYyNSIsInNlY3JldCI6ImQ0OGVmOTEwMDRhOTVjYzViOWNmODZhYWJiMjQ1ODk2OTY5NDU0OGNhMmE4NWY1ZGM1YTdkMDlmZmE5YmYwYmMifX0="
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token="5389976468:AAGArO3pjoHVkyHNOwWk1kdCK8B8vJdsStU")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
# api_id = 14834490
# api_hash = "b392250f1c7031238f11620f75f6707b"
p2p = QiwiP2P(
    auth_key=qiwi_api)
result = None
nest_asyncio.apply()
waiting = None
dep1 = None
dep2 = None


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


@dp.message_handler(commands=["start", "menu"], state="*")
async def introduction(message: types.Message):
    unique_code = extract_unique_code(message.text)
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    if unique_code:
        data[str(unique_code)][3] += 1
        await bot.send_message(int(unique_code), "❕После получения уровня реферал не должен от вас отставать❕\n❕Для "
                                                 "подтверждения реферала, ему следует приобрести следующий уровень❕")
    if str(message.chat.id) not in data:
        print(1)
        if unique_code:
            data[str(message.chat.id)] = [0, 0, [], 0, "", str(unique_code)]
        else:
            data[str(message.chat.id)] = [0, 0, [], 0, "", None]
    cur_time = datetime.datetime.today().hour
    if 0 <= cur_time <= 5:
        cur_time = "Доброй ночи, "
    elif 6 <= cur_time <= 12:
        cur_time = "Доброе утро, "
    elif 13 <= cur_time <= 17:
        cur_time = "Добрый день, "
    else:
        cur_time = "Добрый вечер, "
    user = str(message.chat.username)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Прогресс 💥', callback_data='progress')
    inline_btn_2 = InlineKeyboardButton('Профиль 🏢', callback_data='profile')
    inline_kb_full.row(inline_btn_1, inline_btn_2)
    inline_btn_3 = InlineKeyboardButton('Справка ⁉', callback_data='ask')
    inline_btn_4 = InlineKeyboardButton('Поддержка ℹ', url="t.me/R460BL")
    inline_kb_full.row(inline_btn_3, inline_btn_4)
    # inline_btn_5 = InlineKeyboardButton('Наш чат 👫', callback_data='chat')
    # inline_kb_full.row(inline_btn_5)
    inline_btn_6 = InlineKeyboardButton('Пригласить друзей 📮', url="t.me/ref_to_cash_bot?start=" +
                                                                    str(message.chat.id))
    inline_kb_full.row(inline_btn_6)
    print(user)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()
    try:
        await message.answer(cur_time + user + "!\n\nТут ты можешь _легко заработать_ за *приглашённых рефералов*🔥"
                                               "\n\nПовышая уровень, ты сможешь получать еще больше 💸",
                             parse_mode="Markdown", reply_markup=inline_kb_full)
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda c: c.data == 'progress')
async def process_callback_button6(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    new_text = "{Уровень " + str(data[str(callback_query.message.chat.id)][0]) + \
               "}\n\nСейчас доступно:\n+2 р за каждого реферала\n\nПолучи " + \
               str(data[str(callback_query.message.chat.id)][0] + 1) + " уровень," \
                                                                       " чтобы открыть возможность:\n+30 р за " \
                                                                       "каждого реферала\n\nили\n\nПолучи сразу " + \
               str(data[str(callback_query.message.chat.id)][
                       0] + 2) + "уровень, чтобы открыть возможность:\n+50 р за реферала"
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_7 = InlineKeyboardButton('Повысить уровень 🔥', callback_data='upgrade')
    inline_kb_full.row(inline_btn_7)
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_8)
    await callback_query.message.edit_text(new_text, reply_markup=inline_kb_full)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'upgrade')
async def process_callback_button5(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    global dep1, dep2
    if data[str(callback_query.message.chat.id)][0] == 0:
        bill = p2p.bill(amount=99, lifetime=10, comment="Получение 1 уровня")  # Выставление счета
        bill1 = p2p.bill(amount=199, lifetime=10, comment="Получение 2 уровня")  # Выставление счета
        dep1 = bill.bill_id
        dep2 = bill1.bill_id
        new_text = f"Чтобы получить 1 уровень, переведите 99 рублей, нажав на ссылку: {bill.pay_url}\n\n" \
                   f"Чтобы получить сразу 2 уровень, переведите 199 рублей, нажав на ссылку: {bill1.pay_url}"
    else:
        bill = p2p.bill(amount=199, lifetime=10, comment="Получение 2 уровня")  # Выставление счета
        dep2 = bill.bill_id
        new_text = f"Чтобы получить 2 уровень, переведите 199 рублей, нажав на ссылку: {bill.pay_url}\n\n"

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_15 = InlineKeyboardButton('Проверить оплату ☑', callback_data='check_dep')
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_15)
    inline_kb_full.row(inline_btn_8)
    await callback_query.message.edit_text(new_text, reply_markup=inline_kb_full)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'check_dep')
async def process_callback_button5(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    global dep1, dep2
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_15 = InlineKeyboardButton('Проверить оплату ☑', callback_data='check_dep')
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_15)
    inline_kb_full.row(inline_btn_8)
    if dep1 is not None:
        if p2p.check(bill_id=str(dep1)).status == "PAID":  # проверяем на оплату
            await bot.send_message(callback_query.message.chat.id, "Оплата прошла! У вас теперь 1 уровень 🎉")
            data[callback_query.message.chat.id][0] = 1
            dep1 = None
            if data[callback_query.message.chat.id][5] is not None:
                ref = data[callback_query.message.chat.id][5]
                data[ref][3] -= 1
                data[ref][2].append(callback_query.message.chat.id)
                if data[ref][0] == 0:
                    data[ref][1] += 2
                elif data[ref][0] == 1:
                    data[ref][1] += 30
                else:
                    data[ref][1] += 50
                await bot.send_message(ref, "Поздравляем, у вас новый реферал,баланс пополнен! 🎉")
        else:
            await bot.send_message(callback_query.message.chat.id, "Оплаты пока не видно ❌")

    elif dep2 is not None:
        if p2p.check(bill_id=str(dep2)).status == "PAID":  # проверяем на оплату
            await bot.send_message(callback_query.message.chat.id, "Оплата прошла! У вас теперь 2 уровень 🎉")
            data[callback_query.message.chat.id][0] = 2
            dep2 = None
        else:
            await bot.send_message(callback_query.message.chat.id, "Оплаты пока не видно ❌")
    else:
        await bot.send_message(callback_query.message.chat.id, "Для оплаты, перейдите по ссылке в разделе Прогресс")
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'profile')
async def process_callback_button4(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    # refref = 0
    # for i in data[callback_query.message.chat.id][2]:
    #     if i in data:
    #         refref += len(data[i][2])
    new_text = str(data[str(callback_query.message.chat.id)][0] + 1) \
               + " УРОВЕНЬ\n\nБаланс: " + str(data[str(callback_query.message.chat.id)][1]) + \
               " руб\n\nРефералы: " + str(len(data[str(callback_query.message.chat.id)][2])) \
               + " человек\nОжидают подтверждения: " + str(data[str(callback_query.message.chat.id)][3]) + \
               " человек\n\nЗарабатывай, просто приглашая друзей!\n\n📣 Ваша реферальная ссылка для приглашения: " \
               "t.me/ref_to_cash_bot?start=" + str(callback_query.message.chat.id) + \
               "\n\n📢 Ссылка для отправки вне телеграма:\nhttps://teleg.run/ref_to_cash_bot?start=" \
               + str(callback_query.message.chat.id)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_9 = InlineKeyboardButton('Вывод средств 💰', callback_data='withdraw')
    inline_kb_full.row(inline_btn_9)
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_8)
    await callback_query.message.edit_text(new_text, reply_markup=inline_kb_full)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'ask')
async def process_callback_button3(callback_query: types.CallbackQuery):
    new_text = "Правила проекта\n\n1. Запрещается любого вида накрутка, буксы, а также использование нескольких" \
               " аккаунтов.\n\n2. Запрещается оскорблять администрацию и участников чата, общаться неуважительно." \
               "\n\n3. В чате запрещен мат, флуд и обмен ссылками.\n\n4. Работаем только со странами: РФ, Украина, " \
               "Беларусь.\n\nАдминистрация оставляет за собой право заморозить баланс при наличии подозрений о " \
               "накрутке и недобросовестности."
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    # inline_btn_10 = InlineKeyboardButton('Чат', url="t.me/R460BL")
    inline_btn_11 = InlineKeyboardButton('Админ ❓', url="t.me/R460BL")
    inline_kb_full.row(inline_btn_11)
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_8)
    await callback_query.message.edit_text(new_text, reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'withdraw')
async def process_callback_button2(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    global waiting
    if data[str(callback_query.message.chat.id)][4] == "":
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
        inline_kb_full.row(inline_btn_8)
        waiting = callback_query
        await callback_query.message.edit_text("Введите ваш счёт Qiwi: ", reply_markup=inline_kb_full)
    else:
        new_text = "Ваш адрес для вывода QIWI: " + str(data[str(callback_query.message.chat.id)][4]) + \
                   "\nСредства будут перечислены на указанный Вами адрес в ближайшее время (обычно в течение часа)."
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_12 = InlineKeyboardButton('Изменить номер 🏷', callback_data='change')
        inline_btn_13 = InlineKeyboardButton('Вывести 📩', callback_data='go')
        inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
        inline_kb_full.row(inline_btn_12)
        inline_kb_full.row(inline_btn_13)
        inline_kb_full.row(inline_btn_8)
        await callback_query.message.edit_text(new_text, reply_markup=inline_kb_full)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.message_handler()
async def changing(message: types.Message):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    global waiting
    if waiting:
        if len(message.text) < 3:
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
            inline_kb_full.row(inline_btn_8)
            await waiting.message.edit_text("Номер должен быть больше 3-х символов.\nПовторите ввод! 🔁",
                                            reply_markup=inline_kb_full)
        else:
            data[str(message.chat.id)][4] = message.text
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_btn_12 = InlineKeyboardButton('Изменить номер 🏷', callback_data='change')
            inline_btn_13 = InlineKeyboardButton('Вывести 📩', callback_data='go')
            inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
            inline_kb_full.row(inline_btn_12)
            inline_kb_full.row(inline_btn_13)
            inline_kb_full.row(inline_btn_8)
            new_text = "Ваш адрес для вывода QIWI: " + str(data[str(waiting.message.chat.id)][4]) + \
                       "\nСредства будут перечислены на указанный Вами адрес в ближайшее время (обычно в течение часа) 💯"
            await waiting.message.edit_text(new_text, reply_markup=inline_kb_full)
            waiting = None
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'change')
async def process_callback_button2(callback_query: types.CallbackQuery):
    global waiting
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
    inline_kb_full.row(inline_btn_8)
    waiting = callback_query
    await callback_query.message.edit_text("Введите ваш счёт Qiwi: ", reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'go')
async def process_callback_button2(callback_query: types.CallbackQuery):
    with open("data.json", "r") as f:
        data = json.load(f)
    f.close()
    global qiwi_api, my
    if data[str(callback_query.message.chat.id)][1] < 10:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
        inline_kb_full.row(inline_btn_8)
        await callback_query.message.edit_text("У вас недостаточно денег на счету! 🛑", reply_markup=inline_kb_full)
    else:
        n = str(data[str(callback_query.message.chat.id)][4])
        s = requests.Session()
        s.headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + my, 'Accept': 'application/json'}
        postjson = {"sum": {"amount": int(data[str(callback_query.message.chat.id)][1]), "currency": "643"},
                    "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "",
                    "fields": {"account": n}, 'id': str(int(time.time() * 1000))}
        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
        print(res)
        if str(res.status_code) != "200":
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
            inline_kb_full.row(inline_btn_8)
            await callback_query.message.edit_text("Произошла ошибка, попробуйте снова", reply_markup=inline_kb_full)
        else:
            data[str(callback_query.message.chat.id)][1] = 0
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            inline_btn_8 = InlineKeyboardButton('Назад 🔙', callback_data='menu')
            inline_kb_full.row(inline_btn_8)
            await callback_query.message.edit_text("Перевод отправлен, ждите) 🔜", reply_markup=inline_kb_full)
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler(lambda c: c.data == 'menu')
async def process_callback_button7(callback_query: types.CallbackQuery):
    cur_time = datetime.datetime.today().hour
    if 0 <= cur_time <= 5:
        cur_time = "Доброй ночи, "
    elif 6 <= cur_time <= 12:
        cur_time = "Доброе утро, "
    elif 13 <= cur_time <= 17:
        cur_time = "Добрый день, "
    else:
        cur_time = "Добрый вечер, "
    user = str(callback_query.message.chat.username)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Прогресс 💥', callback_data='progress')
    inline_btn_2 = InlineKeyboardButton('Профиль 🏢', callback_data='profile')
    inline_kb_full.row(inline_btn_1, inline_btn_2)
    inline_btn_3 = InlineKeyboardButton('Справка ⁉', callback_data='ask')
    inline_btn_4 = InlineKeyboardButton('Поддержка ℹ', url="t.me/R460BL")
    inline_kb_full.row(inline_btn_3, inline_btn_4)
    # inline_btn_5 = InlineKeyboardButton('Наш чат 👫', callback_data='chat')
    # inline_kb_full.row(inline_btn_5)
    inline_btn_6 = InlineKeyboardButton('Пригласить друзей 📮', url="t.me/ref_to_cash_bot?start=" +
                                                                    str(callback_query.message.chat.id))
    inline_kb_full.row(inline_btn_6)
    print(user)
    try:
        await callback_query.message.edit_text(
            cur_time + user + "!\n\nТут ты можешь _легко заработать_ за *приглашённых рефералов*🔥"
                              "\n\nПовышая уровень, ты сможешь получать еще больше 💸",
            parse_mode="Markdown", reply_markup=inline_kb_full)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
