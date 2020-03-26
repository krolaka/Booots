import telebot
import config

from telebot import types 

bot = telebot.TeleBot(config.TOKEN)

   
@bot.message_handler(commands=['start'])
def welcome(message):

	#Keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Red Star")
	item2 = types.KeyboardButton("White Star")

	markup.add(item1, item2)

	bot.send_message(message.chat.id, "Hello there, {0.first_name}!\nWhere we go today?".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main(message):
	if message.chat.type == 'private':
		if message.text == 'Red Star':

			markup = types.InlineKeyboardMarkup(row_width=5)
			item1 = types.InlineKeyboardButton("1", callback_data='Red Star 1')
			item2 = types.InlineKeyboardButton("2", callback_data='Red Star 2')
			item3 = types.InlineKeyboardButton("3", callback_data='Red Star 3')
			item4 = types.InlineKeyboardButton("4", callback_data='Red Star 4')
			item5 = types.InlineKeyboardButton("5", callback_data='Red Star 5')
			item6 = types.InlineKeyboardButton("6", callback_data='Red Star 6')
			item7 = types.InlineKeyboardButton("7", callback_data='Red Star 7')
			item8 = types.InlineKeyboardButton("8", callback_data='Red Star 8')
			item9 = types.InlineKeyboardButton("9", callback_data='Red Star 9')
			item10 = types.InlineKeyboardButton("10", callback_data='Red Star 10')

			markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)

			bot.send_message(message.chat.id, 'All right! Choose, what red star you go', reply_markup=markup)

		elif message.text == 'White Star':

			markup = types.InlineKeyboardMarkup(row_width=3)
			item1 = types.InlineKeyboardButton("5x5", callback_data='White Star 5x5')
			item2 = types.InlineKeyboardButton("10x10", callback_data='White Star 10x10')
			item3 = types.InlineKeyboardButton("15x15", callback_data='White Star 15x15')

			markup.add(item1, item2, item3)

			bot.send_message(message.chat.id, 'All right, what white star we go?', reply_markup=markup)

		else:
			bot.send_message(message.chat.id, 'Press button')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			way1 = ('Red Star 1', 'Red Star 2', 'Red Star 3', 'Red Star 4', 'Red Star 5',
			 'Red Star 6', 'Red Star 7', 'Red Star 8', 'Red Star 9', 'Red Star 10')
			way2 = ('White Star 5x5', 'White Star 10x10', 'White Star 15x15')
			for cycle1 in way1:
				if call.data == cycle1:

					message1 = 'Good, you choose ' + cycle1 + ' level'

					markup1 = types.InlineKeyboardMarkup(row_width=2)
					track1 = types.InlineKeyboardButton("Im in", callback_data= 'Track1')
					track2 = types.InlineKeyboardButton("Not yet", callback_data= 'Track2')

					markup1.add(track1, track2)
						
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message1, reply_markup=markup1)	

			if call.data == 'Track1':
				bot.send_message(call.message.chat.id, text='Player @{0.username} ready!'.format(call.from_user))
			elif call.data == 'Track2':
				bot.send_message(call.message.chat.id, text='Player @{0.username} not ready!'.format(call.from_user))

			for cycle2 in way2:
				if call.data == cycle2:

					message2 = 'Great, you choose ' + cycle2 + "\n\nPress the button to know, if you ready or not"

					markup2 = types.InlineKeyboardMarkup(row_width=2)
					track3 = types.InlineKeyboardButton("Im in", callback_data= 'Track3')
					track4 = types.InlineKeyboardButton("Not yet", callback_data= 'Track4')
					switch_button = types.InlineKeyboardButton(text='Try', switch_inline_query= "Telegram")

					markup2.add(track3, track4, switch_button)
						
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message2, reply_markup=markup2)	

			if call.data == 'Track3':
				bot.send_message(call.message.chat.id, text='Player {0.username} ready!'.format(call.from_user))
			elif call.data == 'Track4':
				bot.send_message(call.message.chat.id, text='Player {0.username} not ready!'.format(call.from_user))
	except Exception as e:
		print(repr(e))


   # RUN
bot.polling(none_stop=True)
