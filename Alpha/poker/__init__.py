from threading import Thread 
from queue import Queue 
from .game import Game
from .players import player
from .functions import player_output

def take_input(s_to_c, c_to_s):
  while True:
    h = s_to_c.get()
    if h == 'take_input':
      i = input('Enter option(correct): ')
      c_to_s.put(i)
    elif h == 'print_output':
      print(s_to_c.get())
    else:
      c_to_s.put('test')

def play(num, bank, names, s_to_c, c_to_s, socketio):
  g = Game()
  for a in range(num):
    player(names[a], bank, g)
  while True:
    g.hands = []
    g.big_blind_player = None
    g.set_ante_and_blind_bet()
    g.ante()
    Game.blind__bet(g)
    k = g.players.index(g.big_blind_player) + 1
    if k < g.num_players:
      pass
    else:
      k = 0
    g.player_in_turn = g.players[k]
    g.distribute_cards()
    g.add_cards()
    Game.pre_card_bet(g, s_to_c, c_to_s, socketio)
    s = "End of Pre-Flop Bet"
    player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
    # print("End of Pre-Flop Bet")
    players_in_play = g.check_player_play(g.players.copy())
    Game.post_card_bet(players_in_play, 1, g, s_to_c, c_to_s, socketio)
    # print('Turn 1 done')
    s = "Turn 1 done"
    player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
    players_in_play = g.check_player_play(players_in_play)
    Game.post_card_bet(players_in_play, 2, g, s_to_c, c_to_s, socketio)
    # print('Turn 2 done')
    s = "Turn 2 done"
    player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
    players_in_play = g.check_player_play(players_in_play)
    Game.post_card_bet(players_in_play, 3, g, s_to_c, c_to_s, socketio)
    # print('Turn 3 done')
    s = "Turn 3 done"
    player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
    players_in_play = g.check_player_play(players_in_play)
    players_in_play = list(set(players_in_play + g.all_in_players))
    if len(players_in_play) == 1:
        # print(players_in_play[0].name, " wins")
        s = players_in_play[0].name + ' wins'
        player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
        players_in_play[0].win_(players_in_play)
    else:
      Game.add_score_for_all(players_in_play, g)
      while g.pot != 0:
        Game.compare_score(g.player_scores, players_in_play, g, s_to_c, socketio)
        players_in_play = g.check_player_play(players_in_play)
    g.remove_cards()
    g.check_broke()
    g.broke_unbroke(s_to_c, c_to_s, socketio)
    if len(g.players) < 2:
      break
    else:
      pass

s_to_c = Queue()
c_to_s = Queue()
t1 = Thread(target=play, args=(3, 1000, ['n','p','t'], s_to_c, c_to_s))
t2 = Thread(target=take_input, args=(s_to_c, c_to_s))
# t1.start()
# t2.start()