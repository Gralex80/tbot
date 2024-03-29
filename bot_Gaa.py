import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('MYTOKEN')

# keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# #keyboard1.row('')
# keyboard1.row('Привет', 'Пока')

#kb = types.KeyboardButton('Отправить адрес' ,request_location = True))

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

def get_user_step(uid):
    if uid in userStep:
        print(str(userStep[uid]))
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# def process_step01(message):
#         print(str(message.chat.id))
#     #try:
#         #chat_id = message.chat.id
#         #name = message.text
#         #user = User(name)
#         #user_dict[chat_id] = user
#         bot.send_message(message.chat.id,'Начали!')
#         #msg = bot.reply_to(message, 'How old are you?')
#         #bot.register_next_step_handler(msg, process_age_step)
#     #except Exception as e:
#         #bot.reply_to(message, 'oooops')
#      #   None


# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())




        #bot.send_photo(cid, open('d:/PROG/PyTbot/examples/detailed_example/rooster.jpg', 'rb'),
         #              reply_markup=hideBoard)  # send file and hide keyboard, after image is sent


#@bot.message_handler(content_types=['photo'],func=lambda message: get_user_step(message.chat.id) == 3)
@bot.message_handler(content_types=['photo'],func=lambda message: get_user_step(message.chat.id) == 4)
def handle_file(message):
    #try:
    chat_id = message.chat.id
    file_info = bot.get_file(message.photo[-1].file_id)
    print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'D:/'+file_info.file_path;
    print(src)

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Отличное фото!")
    bot.send_message(message.chat.id, f"{str(message.chat.first_name)}, У Вас все готово! Хорошего дня!",reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    userStep[message.chat.id] = -1
    #bot.send_message(message.chat.id, 'Все готово!')
    #except Exception as e:
       
        #bot.reply_to(message+"!!!", e)


# @bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
# def msg_image_select(message):
#     cid = message.chat.id
#     text = message.text

#     # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
#     #bot.send_chat_action(cid, 'typing')

#     #if text == 'Фото витрины':  # send the appropriate image based on the reply to the "/getImage" command
#         #
#         # bot.send_message(message.chat.id, 'Конец', reply_markup=telebot.types.ReplyKeyboardRemove())
#     userStep[message.chat.id] = 5

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def msg_image_select(message):
    cid = message.chat.id
    text = message.text

    # if text == 'Включить кофемашину':  
    #     keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    #     button_on = telebot.types.KeyboardButton(text="Фото витрины")        
    #     keyboard.add(button_on)
    #     bot.send_message(message.chat.id, 'Супер! Осталось отправить фото витрины', reply_markup=keyboard)
    #     userStep[message.chat.id] = 4


## step 02
@bot.message_handler(content_types=["location"],func=lambda message: get_user_step(message.chat.id) == 2)
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        
        # keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        # button_on = telebot.types.KeyboardButton(text="Включить кофемашину")
        # keyboard.add(button_on)
        # bot.send_message(message.chat.id, 'Замечательно!. Теперь, подготовь кофемашину и включи ее', reply_markup=keyboard)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
        InlineKeyboardButton("Нет", callback_data="cb_no"))    
        userStep[message.chat.id] = 3
        bot.send_message(message.chat.id, "Включить кофемашину?", reply_markup=markup)
  

#@bot.message_handler(commands=["geo"],func=lambda message: get_user_step(message.chat.id) == 2)
def geo(call):
    try:
        if get_user_step(call.message.chat.id) == 2:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)
            bot.send_message(call.message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
    except:
        None

## step 01 and 03
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "cb_yes" and userStep[call.message.chat.id]>0:
            if userStep[call.message.chat.id] == 1:
                userStep[call.message.chat.id] = 2
                geo(call)
            if userStep[call.message.chat.id] == 3:
                userStep[call.message.chat.id] = 4
                bot.send_message(call.message.chat.id, "Осталось отправить Фото. Пришли мне фото витрины", reply_markup=telebot.types.ReplyKeyboardRemove())

            bot.answer_callback_query(call.id, "Отлично! Идем дальше!")    
        if call.data == "cb_no" and userStep[call.message.chat.id]>0:
            userStep[call.message.chat.id] = -1
            bot.answer_callback_query(call.id, "Хорошего дня!")

    except:
        None

@bot.message_handler(commands=['start'])
def start_message(message):
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
    InlineKeyboardButton("Нет", callback_data="cb_no"))    
    bot.send_message(message.chat.id, f"Привет {str(message.chat.first_name)}!\nНачнем работу?", reply_markup=markup)
    userStep[message.chat.id] = 1    
    

    #bot.send_message(message.chat.id, 'chat_id:'+str(message.chat.id)+'User:'+str(message.chat.first_name), reply_markup=keyboard1)

#def inline(callback):
#    bot.delete_message(callback.message.chat.id, callback.message.message_id)    
    #bot.send_message(message.chat.id, 'chat_id:'+str(message.chat.id)+'User:'+str(message.chat.first_name)+'message_id:'+str(message.message_id))
    #m=message.message_id
    #bot.delete_message(message.chat.id, message.message_id)
    #print(message.text)
    
    # while m!=0:
    #     try:
    #         bot.delete_message(message.chat.id, m)
    #     except:
    #         None
    #     m=m-1

      
    #bot.send_message(message.chat.id, 'end')

# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, 'Привет, мой создатель')
#     elif message.text.lower() == 'пока':
#         bot.send_message(message.chat.id, 'Прощай, создатель')
#     elif message.text.lower() == 'я тебя люблю':
#         bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

# @bot.message_handler(lambda message: message.text.lower() == "Без пюрешки")
# async def without_puree(message):
#     await message.reply("Так невкусно!")



# @bot.message_handler(content_types=['sticker'])
# def sticker_id(message):
#     print(message)




bot.polling(none_stop=False, interval=1, timeout=10, long_polling_timeout=360)
