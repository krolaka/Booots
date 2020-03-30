import telebot
import config
import pickledb

from telebot import types 

bot = telebot.TeleBot(config.TOKEN)
db = pickledb.load('session.json', False)

@bot.message_handler(commands=['start'])
def welcome(message):
  message_text = "Hello there, {0.first_name}!\nWhere we go today?".format(message.from_user)
  bot.send_message(message.chat.id, message_text, parse_mode='html', reply_markup=start_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    markup, message = switcher(call)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message, reply_markup=markup)
  except Exception as e:
    print(repr(e))

def start_markup():
  markup = types.InlineKeyboardMarkup(row_width=2)
  rs = types.InlineKeyboardButton("Red Star", callback_data='rs')
  ws = types.InlineKeyboardButton("White Star", callback_data='ws')
  markup.add(rs, ws)

  return markup 

def rs():
  markup = types.InlineKeyboardMarkup(row_width=5)
  item1 = types.InlineKeyboardButton("1", callback_data='rs_1')
  item2 = types.InlineKeyboardButton("2", callback_data='rs_2')
  item3 = types.InlineKeyboardButton("3", callback_data='rs_3')
  item4 = types.InlineKeyboardButton("4", callback_data='rs_4')
  item5 = types.InlineKeyboardButton("5", callback_data='rs_5')
  item6 = types.InlineKeyboardButton("6", callback_data='rs_6')
  item7 = types.InlineKeyboardButton("7", callback_data='rs_7')
  item8 = types.InlineKeyboardButton("8", callback_data='rs_8')
  item9 = types.InlineKeyboardButton("9", callback_data='rs_9')
  item10 = types.InlineKeyboardButton("10", callback_data='rs_10')
  markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
  message = 'All right! Choose, what red star you go?'

  return markup, message

def ws():
  markup = types.InlineKeyboardMarkup(row_width=3)
  item1 = types.InlineKeyboardButton("5x5", callback_data='ws_5')
  item2 = types.InlineKeyboardButton("10x10", callback_data='ws_10')
  item3 = types.InlineKeyboardButton("15x15", callback_data='ws_15')
  markup.add(item1, item2, item3)
  message = 'All right, what white star we go?' 

  return markup, message

def confirm(call):
  markup = types.InlineKeyboardMarkup(row_width=2)
  track1 = types.InlineKeyboardButton("Im in", callback_data='y')
  track2 = types.InlineKeyboardButton("Not yet", callback_data='n')
  markup.add(track1, track2)
  message = parse_data(call)

  return markup, message

def parse_data(call):
  message_id = str(call.message.message_id)
  username = call.from_user.username
  ready_users = ''
  data = call.data
  star = get_star_text(message_id)
  
  if data == 'y':
    add_user(message_id, username)
    ready_users = new_confirm_message(message_id)
  elif data == 'n':
    rm_user(message_id, username)
    ready_users = new_confirm_message(message_id)
  else:
    type_star, level = data.split('_')
    if type_star == 'ws':
      star = 'White Star ' + level + 'x' + level
    else:
      star = 'Red Star ' + level
    db.set(message_id, {'star': star, 'usernames': []})

  return ping_users() + " you choose " + star + "\nPress the button to know, if you ready or not. \n\n" + ready_users

def new_confirm_message(message_id):
  ready_users = ''
  record = db.get(message_id)
  for username in record['usernames']:
    ready_users += '@' + username + " ready!"
  return ready_users

def ping_users():
  ping_users = ''
  record = db.get('usernames')
  if record:
    for username in record:
      ping_users += ' @' + username + ','
  return ping_users

def get_star_text(message_id):
  record = db.get(message_id)
  if record:
    star = record['star']
  else:
    star = ''
  return star
  
def add_user(message_id, username):
  users = list()
  record = db.get(message_id)
  usernames = record['usernames']
  if not usernames:
    usernames = list()
  users.extend(usernames)
  users.append(username)
  uniq_users = list(set(users))
  record['usernames'] = uniq_users
  add_users(uniq_users)  

def add_users(uniq_users):
  all_users = db.get('usernames')
  if not all_users:
    all_users = list()
  all_users.extend(uniq_users)
  db.set('usernames', list(set(all_users)))
  db.dump()

def rm_user(message_id, username):
  users = list()
  record = db.get(message_id)
  usernames = record['usernames']
  if not usernames:
    usernames = list()
  users.extend(usernames)
  if username in users:
    users.remove(username)
  record['usernames'] = users

def switcher(call):
  list_of_data = ['ws_5', 'ws_10', 'ws_15', 'rs_1', 'rs_2', 'rs_3', 'rs_4', 'rs_5', 'rs_6', 'rs_7', 'rs_8', 'rs_9', 'rs_10', 'y', 'n']
  data = call.data
  if data == 'rs':
    return rs()
  elif data == 'ws':
    return ws()
  elif data in list_of_data:
    return confirm(call)

bot.polling(none_stop=True)
