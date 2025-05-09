from .players import player
from .cards import remove_dup_list
import random
from .functions import player_input, player_output, take_input

class Game:
  @classmethod
  def blind__bet(cls, g):
    for i in range(g.num_players):
      if (g.turn)%(g.num_players)==i & i < (g.num_players-2):
        g.blind_(g.players[i+2], g.players[i+1], g.blind_bet)
        break
      elif (g.turn)%(g.num_players) == (g.num_players-2):
        g.blind_(g.players[0], g.players[-1], g.blind_bet)
        break
      elif (g.turn)%(g.num_players) == (g.num_players-1):
        g.blind_(g.players[1], g.players[0], g.blind_bet)
        break

  @classmethod
  def pre_card_bet(cls, g, s_to_c, c_to_s, socketio):
    players_in_play = g.players.copy()
    d = g.players.index(g.player_in_turn)
    while g._play_ == True:
      for i in players_in_play[d:]+players_in_play[:d]:
        if g.max_folds != len(g.players)-1:
          if i.check == True:
            continue
          else:
            # input()
            player_output(s_to_c, 'AAAA', socketio, i.name, i.cards)
            # s_to_c.put('print_output')
            # s_to_c.put(i.cards)
            # print(i.cards)
            if g.bet-i.current_bet == 0: 
              opt_1 = 'Check'
            else:
              opt_1 = 'Call ' + str(g.bet-i.current_bet)
            if (i == g.big_blind_player) & (g.bet == g.blind_bet):
              # print('1.' ,opt_1)
              # print('2. Raise')
              s = '1.' + opt_1
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
              s = '2. Raise'
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
            else:
              # print('1.', opt_1)
              # print('2. Raise')
              # print('3. Fold')
              s = '1.' + opt_1
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
              s = '2. Raise'
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
              s = '3. Fold'
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
            # a = int(input(f"Enter option {i.name}: "))
            a = int(take_input(c_to_s, socketio))
            if a == 1:
              g.player_in_turn = i
              i.call_()
              if g.check == True:
                # print("Check")
                s = 'Check'
                player_output(s_to_c, 'AAAA', socketio, i.name, s)
              else:
                # print("Called ", player.bet)
                s = "Called " + str(g.bet)
                player_output(s_to_c, 'AAAA', socketio, i.name, s)
            elif a == 2:
              g.player_in_turn = i
              b = int(take_input(c_to_s, socketio))
              i.bet_(b)
              i.raise_()
              for j in players_in_play:
                if j == i:
                  continue
                else:
                  j.uncheck_()
              #  print("Raised to ", (b))
              s = 'Raised to ' + str(b)
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
            elif a == 3:
              c = g.players.index(i)
              if c < len(g.players)-1:
                g.player_in_turn = g.players[c+1]
              else:
                g.player_in_turn = g.players[0]
              if (i == g.big_blind_player) & (g.bet == g.blind_bet):
                continue
              else:
                i.fold_()
                # print("Folded")
                s = 'Folded'
                player_output(s_to_c, 'AAAA', socketio, i.name, s)
            else:
              continue
            # print(i.bank)
            s = str(i.bank)
            player_output(s_to_c, 'AAAA', socketio, i.name, s)
        else:
          for j in players_in_play:
            j.check_check_()
          players_in_play = g.check_player_play(players_in_play)
          g.check_play_(players_in_play)
          break
        for j in players_in_play:
          j.check_check_()
        players_in_play = g.check_player_play(players_in_play)
        g.check_play_(players_in_play)
    for k in g.players:
      k.reset()
    g.reset_cls()
    
  @classmethod
  def post_card_bet(cls, players_in_play, turn, g, s_to_c, c_to_s, socketio):
    if turn == 1:
      l1 = g.table_cards[:3]
    elif turn == 2:
      l1 = g.table_cards[:4]
    else:
      l1 = g.table_cards
    d = g.players.index(g.player_in_turn)
    while g._play_ == True:
      if len(players_in_play) > 1:
        for i in players_in_play[d:]+players_in_play[:d]:
          if g.max_folds != g.num_players-1:
            if i.check == True:
              continue
            else:
              # input()
              # print(l1)
              # print(i.cards)
              player_output(s_to_c, 'AAAA', socketio, i.name, l1)
              player_output(s_to_c, 'AAAA', socketio, i.name, i.cards)
              if g.check == True:
                opt_1 = 'Check'
              else: 
                if g.bet-i.current_bet == 0:
                  opt_1 = 'Check'
                else:
                  opt_1 = 'Call ' + str(g.bet-i.current_bet)
              # print('1. ', opt_1)
              # print("2. Raise")
              s = '1. ' + opt_1
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
              s = '2. Raise'
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
              if g.bet == 0:
                pass
              else:
                # print('3. Fold')
                s = '3. Fold'
                player_output(s_to_c, 'AAAA', socketio, i.name, s)
              # a = int(input(f"Enter option {i.name}: "))
              a = int(take_input(c_to_s, socketio))
              if a == 1:
                g.player_in_turn = i
                i.call_()
                if g.check == True or g.bet == 0:
                  # print("Check") 
                  s = 'Check'
                  player_output(s_to_c, 'AAAA', socketio, i.name, s)
                else:
                  # print("Called ", player.bet)
                  s = 'Called ' + str(g.bet)
                  player_output(s_to_c, 'AAAA', socketio, i.name, s)
              elif a == 2:
                g.player_in_turn = i
                # b = int(input("Enter bet: "))
                b = int(take_input(c_to_s, socketio))
                i.bet_(b)
                i.raise_()
                for j in players_in_play:
                  if j == i:
                    continue
                  else:
                    j.uncheck_()
                # print("Raised to ", (b))
                  s = 'Raised to ' + str(b)
                  player_output(s_to_c, 'AAAA', socketio, i.name, s)
              elif a == 3:
                c = players_in_play.index(i)
                if c < len(players_in_play)-1:
                  g.player_in_turn = players_in_play[c+1]
                else:
                  g.player_in_turn = players_in_play[0]
                if g.check == False:
                  i.fold_()
                  # print("Folded")
                  s = 'Folded'
                  player_output(s_to_c, 'AAAA', socketio, i.name, s)
                else:
                  continue
              else:
                continue
              # print(i.bank)
              s = str(i.bank)
              player_output(s_to_c, 'AAAA', socketio, i.name, s)
          else:
            for j in players_in_play:
              j.check_check_()
            players_in_play = g.check_player_play(players_in_play)
            g.check_play_(players_in_play)
            break
          for j in players_in_play:
            j.check_check_()
          players_in_play = g.check_player_play(players_in_play)
          g.check_play_(players_in_play)
      else:
        break
    for k in g.players:
      k.reset()
    g.reset_cls()

  @classmethod
  def add_score_for_all(cls, players_in_play, g):
    for i in players_in_play:
      i.add_score()
      g.player_scores[i] = i.score

  @classmethod
  def compare_score(cls, player_scores, players_in_play, g, s_to_c, socketio):
    max_score = max(player_scores.values())
    d = remove_dup_list(player_scores.values())[1]
    if d[max(d.keys())] == 1:
      for z in players_in_play:
        if max_score == player_scores[z]:
          # print(f"{z.name} wins")
          s = z.name + ' Wins'
          player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)
          z.win_(players_in_play)
          g.player_scores.pop(z)
    else:
      draw_winnings = g.draw_winnings_(d[max(d.keys())])
      for y in players_in_play:
        if y.score == max(d.keys()):
          y.draw_(draw_winnings)
      # print('Draw')
      s = 'Draw'
      player_output(s_to_c, 'AAAA', socketio, 'SERVER', s)

  def __init__(self):
    self.id = 0
    self.num_players = 0
    self.players = []
    self.deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
        '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
          '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']
    self.pot = 0
    self.turn = 0
    self.bet = 0
    self._play_ = True
    self.check = False
    self.big_blind_player = None
    self.player_in_turn = None
    self.max_folds = 0
    self._bank_ = 0
    self.table_cards = None
    self.blind_bet = 0
    self.an = 0
    self.player_scores = {}
    self.hands = []
    self.broke_players = {}
    self.all_in_players = []
    self.all_in_num = 0

  def reset_cls(self):
    self._play_ = True
    self.bet = 0
    self.deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
        '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
          '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']

  def draw_winnings_(self, num_people):
    self.turn += 1
    return self.pot/num_people

  def set_ante_and_blind_bet(cls):
    c = cls._bank_//50
    _ = cls._bank_//200
    blind_bets = [c*a for a in range(1,6)]
    antes = [_*a for a in range(1,6)]
    if cls.turn <= 5:
      cls.blind_bet = round(blind_bets[0])
      cls.an = round(antes[0])
    elif cls.turn <= 10:
      cls.blind_bet = round(blind_bets[1])
      cls.an = round(antes[1])
    elif cls.turn <= 15:
      cls.blind_bet = round(blind_bets[2])
      cls.an = round(antes[2])
    elif cls.turn <= 20:
      cls.blind_bet = round(blind_bets[3])
      cls.an = round(antes[3])
    else:
      cls.blind_bet = round(blind_bets[4])
      cls.an = round(antes[4])

  def check_player_play(self, players_in_play):
    p = []
    for i in players_in_play:
      if not i.play or i.all_in: 
        p.append(i)
    for j in p:
      players_in_play.remove(j)
    return players_in_play
  
  def check_play_(self, players_in_play):
    c = 0
    for i in players_in_play:
      if i.check == True:
        c+=1
      else:
        pass
    if len(players_in_play) != 1:
      if c == len(players_in_play):
        self._play_ = False
      else:
        self._play_ = True
    else:
      self._play_ = False

  def blind_(self, player1, player2, blind_bet):
    self.bet = blind_bet
    player1.big_blind_(blind_bet)
    player2.small_blind_(blind_bet)

  def reset_all_(self):
    for i in self.players:
      i.reset()

  def reset_play_for_all(self):
    for i in self.players:
      i.play = True

  def draw_cards(self, num):
    a = 0
    dummy_hand = []
    while a < num:
      card_a = random.choice(self.deck)
      removed_card_index = self.deck.index(card_a)
      self.deck.pop(removed_card_index)
      a+=1
      dummy_hand.append(card_a)
    return dummy_hand

  def distribute_cards(self):
    card_num = (self.num_players*2) + 5
    chosen_cards = self.draw_cards(card_num)
    b = 0
    while b < self.num_players:
      self.hands.append(chosen_cards[2*b:2*(b+1)])
      b+=1
    self.table_cards = chosen_cards[2*self.num_players:]

  def add_cards(self):
    i = 0
    for j in self.players:
      j.cards = self.hands[i]
      i+=1

  def remove_cards(self):
    for j in self.players:
      j.cards = None

  def ante(self):
    for k in self.players:
      self.pot+=self.an
      k.bank-=self.an

  def check_broke(self):
    for i in self.players:
      if i.bank <= 0:
        self.broke_players[self.players.index(i)] = i
      else:
        continue
    for j in list(self.broke_players.values()):
      self.players.remove(j)

  def broke_unbroke(self, s_to_c, c_to_s, socketio):
    if len(self.broke_players) != 0:
      p = []
      for i in list(self.broke_players.keys()):
        # print("1. Rebuy")
        # print("2. Spectate")
        # print("3. Leave Table")
        player_output(s_to_c, 'AAAA', socketio, i.name, '1. Rebuy')
        player_output(s_to_c, 'AAAA', socketio, i.name, '2. Spectate')
        player_output(s_to_c, 'AAAA', socketio, i.name, '3. Leave Table')
        b = 0
        while b == 0:
          # a = int(input(f"Enter option {player.broke_players[i].name}: "))
          a = int(take_input(c_to_s, socketio))
          if a == 1:
            # print("Rebought")
            player_output(s_to_c, 'AAAA', socketio, i.name, 'Rebought')
            self.players.insert(i, self.broke_players[i])
            p.append(i)
            self.players[i].bank+=self._bank_
            b = 1
          elif a == 2:
            del self.broke_players[i]
            self.num_players-=1
            # print("Spectating")
            player_output(s_to_c, 'AAAA', socketio, i.name, 'Spectating')
            b = 1
          elif a == 3:
            self.num_players-=1
            b = 1
          else:
            pass
      for k in p:
        del self.broke_players[k]
      p.clear()
