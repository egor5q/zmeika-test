import random
import traceback
from telebot import types, TeleBot
import time
import threading
import telebot
import os

bot = TeleBot(os.environ['zmeika'])

games = {}

    
def createplayer(user, em):
    return {user.id:{
        'id':user.id,
        'name':user.first_name,
        'emoji':em,
        'coords':{},
        'look':'right',
        'len':5,
        'main':[1, 1],
        'alive':True
    }
           }



@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Приветствие')

    
@bot.message_handler(commands=['del'])
def deleeet(m):
    try:
        game = games[m.chat.id]
    except:
        return
    if game['creator'] == m.from_user.id:
        del games[game['id']]
        bot.send_message(m.chat.id, 'Игра удалена.')
    
@bot.message_handler(commands=['prepare'])
def startgame(m):

    if m.chat.id not in games:
        game = creategame(m)
        x = m.text.split(' ')

        games.update(game)
        game = games[m.chat.id]
        bot.send_message(m.chat.id, 'Подготовка к игре запущена. Код игры: '+game['code']+'. '+
                         'Для присоединения к игре напишите `/join '+game['code']+'`', parse_mode = 'markdown')
    else:
        bot.send_message(m.chat.id, 'В этом чате уже есть игра!')
        return
    
    
@bot.message_handler(commands=['join'])
def joinn(m):
    try:
        x = m.text.split(' ')[1]
    except:
        bot.send_message(m.chat.id, 'Неверный формат!')
        return
    game = None
    for ids in games:
        if games[ids]['code'] == x:
            game = games[ids]
    if game == None:
        bot.send_message(m.chat.id, 'Игры не существует!')
        return
    if len(game['players']) >= game['maxp']:
        bot.send_message(m.chat.id, 'В игре уже присутствует максимальное число игроков ('+str(game['maxp'])+')!')
        return
    if game['started'] == True:
        bot.send_message(m.chat.id, 'Игра уже идёт!')
        return
    ems = ['👁', '🐼', '🐷', '🌝', '🌚', '💣']
    
    allem = []
    em = random.choice(ems)
    for ids in game['players']:
        allem.append(game['players'][ids]['emoji'])
    while em in allem:
        em = random.choice(ems)
    
    game['players'].update(createplayer(m.from_user, em))
    player = game['players'][m.from_user.id]
    if len(game['players']) == 1:
        player['coords'].update({'1-1':{'pos':[1, 1],
                                       'lifetime':5,
                                       'type':'zmei',
                                       'id':player['id'],
                                       'created':'now'}})
        player['main'] = [1, 1]
        game['ground']['1-1']['item'] = player['coords']['1-1']                      
        player['look'] = 'bot'
        
    elif len(game['players']) == 2:
        player['coords'].update({'1-16':{'pos':[1, 16],
                                       'lifetime':5,
                                       'type':'zmei',
                                       'id':player['id'],
                                       'created':'now'}})
        player['main'] = [1, 16]
        game['ground']['1-16']['item'] = player['coords']['1-16']
        player['look'] = 'right'
        
    elif len(game['players']) == 3:
        player['coords'].update({'16-16':{'pos':[16, 16],
                                       'lifetime':5,
                                       'type':'zmei',
                                       'id':player['id'],
                                       'created':'now'}})
        player['main'] = [16, 16]
        game['ground']['16-16']['item'] = player['coords']['16-16']
        player['look'] = 'top'
        
    elif len(game['players']) == 4:
        player['coords'].update({'16-1':{'pos':[16, 1],
                                       'lifetime':5,
                                       'type':'zmei',
                                       'id':player['id'],
                                       'created':'now'}})
        player['main'] = [16, 1]
        game['ground']['16-1']['item'] = player['coords']['16-1']
        player['look'] = 'left'
    bot.send_message(m.chat.id, 'Вы успешно присоединились к игре! Эмодзи вашей змейки - '+em+'!')
    bot.send_message(game['id'], m.from_user.first_name+' присоединился!')
    
    
@bot.message_handler(commands=['go'])
def go(m):
  try:
    if m.chat.id not in games:
        bot.send_message(m.chat.id, 'Игра ещё не была создана!')
        return
    game = games[m.chat.id]
    if m.from_user.id != game['creator']:
        bot.send_message(m.chat.id, 'Не вы создатель игры!')
        return
    if game['started'] == False:
        game['started'] = True

        bot.send_message(game['id'], 'Игра начинается! Переключайтесь в личку бота, чтобы управлять своей змейкой.')
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = '^', callback_data = 'up '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none')
                                                                )
        kb.add(types.InlineKeyboardButton(text = '<', callback_data = 'left '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = '>', callback_data = 'right '+str(game['id']))
                                                                )
    
        kb.add(types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = 'v', callback_data = 'down '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none')
        )
        
        lst = []
        for ids in game['ground']:
            if game['ground'][ids]['item'] == None:
                lst.append(game['ground'][ids])
        foods = ['🌭', '🍏', '🍄', '🍩']        
        while len(game['food']) < game['foodamount']:
            place = random.choice(lst)
            game['ground'][str(place['code'][0])+'-'+str(place['code'][0])]['item'] = {
                'pos':[place['code'][0], place['code'][1]],
                'type':'food',
                'emoji':random.choice(foods)
            }
                
                
                
        
        for ids in game['players']:
            try:
                msg = bot.send_message(game['players'][ids]['id'], ground(game, id=game['players'][ids]['id'], kb=True, send=True), reply_markup = kb)
                game['msgs'].append(msg)
            except:
                bot.send_message(441399484, traceback.format_exc())
                

        threading.Timer(6, next_turn, args=[game]).start()
  except:
    bot.send_message(441399484, traceback.format_exc())
        
@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    try:
        game = games[int(call.data.split(' ')[1])]
    except:
        return
    try:
        player = game['players'][call.from_user.id]
    except:
        return
    if call.data.split(' ')[0] == 'up':
        player['look'] = 'top'
    elif call.data.split(' ')[0] == 'down':
        player['look'] = 'bot'
    elif call.data.split(' ')[0] == 'left':
        player['look'] = 'left'
    elif call.data.split(' ')[0] == 'right':
        player['look'] = 'right'
    bot.answer_callback_query(call.id, 'ᅠ')
        
        
     
def next_turn(game):
  try:
    fragmentdie = []
    playerdie = []
    for ids in game['players']:
        player = game['players'][ids]
        for idss in game['players'][ids]['coords']:
            crd = game['players'][ids]['coords'][idss]
            crd['created'] = 'notnow'
    for ids in game['players']:
        player = game['players'][ids]
        for idss in game['players'][ids]['coords']:
            crd = game['players'][ids]['coords'][idss]
            crd['lifetime'] -= 1
            if crd['lifetime'] <= 0:
                fragmentdie.append({'player':player, 'fragment':crd})
        if player['alive']:
            if player['look'] == 'top':
                player['main'][1] -= 1
            elif player['look'] == 'left':
                player['main'][0] -= 1
            elif player['look'] == 'bot':
                player['main'][1] += 1
            elif player['look'] == 'right':
                player['main'][0] += 1
            if player['main'][0] > 16 or player['main'][1] > 16:
                playerdie.append(player)
    for ids in game['players']:
        for idss in game['players']:
            p1 = game['players'][ids]
            p2 = game['players'][idss]
            if str(p1['main'][0])+'-'+str(p1['main'][1]) in p2['coords']:
                print('in')
                if p2 == p1 and p1['coords'][str(p1['main'][0])+'-'+str(p1['main'][1])]['created'] == 'now':
                    print('it is main block')
                    print(p1['coords'][str(p1['main'][0])+'-'+str(p1['main'][1])])
                elif p2 != p1 and p2['coords'][str(p1['main'][0])+'-'+str(p1['main'][1])]['lifetime'] == 0:
                    pass
                else:
                    print('sneak die!')
                    playerdie.append(p1)
    
    fdremove = []
    for ids in game['players']:
        player = game['players'][ids]
        item = game['ground'][str(player['main'][0])+'-'+str(player['main'][1])]['item']
        if item != None:
            if item['type'] == 'food':
                for ids in player['coords']:
                    fragment = player['coords'][ids]
                    fragment['lifetime'] += 1
                    for ids in fragmentdie:
                        if ids['player']['id'] == player['id']:
                            fdremove.append(ids)
    for ids in fdremove:
        fragmentdie.remove(ids)
                    
    for ids in game['players']:
        player = game['players'][ids]
        player['coords'].update({str(player['main'][0])+'-'+str(player['main'][1]):{
                    'pos':[player['main'][0], player['main'][1]],
                    'lifetime':player['len'],
                    'type':'zmei',
                    'id':player['id'],
                    'created':'now'}})
            
    for ids in fragmentdie:
        del game['players'][ids['player']['id']]['coords'][str(ids['fragment']['pos'][0])+'-'+str(ids['fragment']['pos'][1])]
        try:
            game['ground'][str(ids['fragment']['pos'][0])+'-'+str(ids['fragment']['pos'][1])]['item'] = None
        except:
            pass
        
    for ids in game['players']:
        for idss in game['players'][ids]['coords']:
            try:
                coord = game['players'][ids]['coords'][idss]
                game['ground'][idss]['item'] = coord
            except:
                playerdie.append(game['players'][ids])
                
    for ids in playerdie:
        game['players'][ids['id']]['alive'] = False
            
    for ids in game['msgs']:
        msg = ids
        ground(game, id=msg.chat.id, kb=True, send=False, msgid = msg.message_id)
    allow = False
    for ids in game['players']:
        if game['players'][ids]['alive'] == True:
            allow = True
    if allow:
        threading.Timer(1.5, next_turn, args = [game]).start()
    else:
        for ids in game['msgs']:
            msg = ids
            bot.send_message(msg.chat.id, 'Все змейки мертвы, игра завершена!')
      
  except:
    bot.send_message(441399484, traceback.format_exc())

            
            
    
    
    
def ground(game, id, kb=False, send=True, msgid = None):
    text = ''
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = '^', callback_data = 'up '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none')
                                                                )
    kb.add(types.InlineKeyboardButton(text = '<', callback_data = 'left '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = '>', callback_data = 'right '+str(game['id']))
                                                                )
    
    kb.add(types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none'),
           types.InlineKeyboardButton(text = 'v', callback_data = 'down '+str(game['id'])),
           types.InlineKeyboardButton(text = 'ᅠ', callback_data = 'none')
                                                                )
    
    for ids in game['ground']:
        obj = game['ground'][ids]
        if obj['item'] == None:
            text += '⬜'
        elif obj['item']['type'] == 'zmei':
            player = game['players'][obj['item']['id']]
            text += player['emoji']
        elif obj['item']['type'] == 'food':
            text += obj['emoji']
    if send == True:
        return text
    else:
        try:
            medit(text, id, msgid, reply_markup = kb)
        except:
            pass
          
        
        
     
def creategame(m, machine = 'phone', maxp = 4):
    g = {}
    x = 1
    y = 1
    while y <= 16:
        x = 1
        while x <= 16:
            g.update({str(x)+'-'+str(y):{'code':[x, y],
                                        'item':None}})
            x+=1
        y+=1
    
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    lst = []
    for ids in games:
        lst.append(games[ids]['code'])
    
    code = ''
    while len(code) < 5:
        code += random.choice(nums)

    while code in lst:
        code = ''
        while len(code) < 5:
            code += random.choice(nums)
    
    return {m.chat.id:{
        'id':m.chat.id,
        'players':{},
        'started':False,
        'creator':m.from_user.id,
        'msgs':[],
        'turn':1,
        'text':'',
        'ground':g,
        'machine':machine,
        'code':code,
        'maxp':maxp,
        'food':{},
        'foodamount':5
        
    }
           }
    
    
    
def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                    reply_markup=reply_markup,
                                    parse_mode=parse_mode)

print('7777')
bot.polling(none_stop=True)

