import cards

class player():
  pot = 0
  turn = 0
  bet = 0
  _play_ = True
  check = True
  big_blind_player = None
  num_players = 3
  max_folds = 0
  _bank_ = 0
  players = []
  table_cards = None
  blind_bet = 50
  player_scores = {}

  @classmethod
  def draw_winnings_(cls, num_people):
    player.turn += 1
    return cls.pot/num_people

  @classmethod
  def set_blind_bet(cls):
    blind_bets = []
    c = cls.bank/100
    for i in range(1,6):
      blind_bets.append(c*i)
    if cls.turn <= 5:
      cls.blind_bet = blind_bets[0]
    elif cls.turn <= 10:
      cls.blind_bet = blind_bets[1]
    elif cls.turn <= 15:
      cls.blind_bet = blind_bets[2]
    elif cls.turn <= 20:
      cls.blind_bet = blind_bets[3]
    else:
      cls.blind_bet = blind_bets[4]

  @classmethod
  def blind_(cls, player1, player2, blind_bet):
    cls.bet = blind_bet
    player1.big_blind_(blind_bet)
    player2.small_blind_(blind_bet)

  @classmethod
  def check_player_play(cls, players_in_play):
    for i in players_in_play:
      if i.play != True:
        players_in_play.remove(i)
    return players_in_play
  
  @classmethod
  def check_play_(cls, players_in_play):
    c = 0
    for i in players_in_play:
      if i.check == True:
        c+=1
      else:
        pass
    if len(players_in_play) != 1:
      if c == len(players_in_play):
        player._play_ = False
      else:
        player._play_ = True
    else:
      player._play_ = False

  @classmethod
  def reset_all_(cls):
    for i in cls.players:
      i.reset()

  @classmethod
  def reset_cls(cls):
    cls._play_ = True
    cls.bet = 0

  def __init__(self, name,  bank):
    self.cards = None
    self.score = 0
    self.__class__._bank_ = bank
    self.name = name
    self.bank = bank
    self.prev_bank = bank
    self.play = True
    self.__class__.players.append(self)
    # self.__class__.num_players+=1
    self.reset()
    print(self.name, self.bank)

  def reset(self):
    self.bet = 0
    self.all_in = False
    self.check = False
    self.current_bet = 0

  def check_(self):
    self.check = True
  
  def allin(self):
    self.all_in = True

  def uncheck_(self):
    if self.all_in:
      pass
    else:
      self.check = False

  def check_check_(self):
    if self.check == False:
      player.check = False
    else:
      pass

  def bet_(self, bet):
    player.check = False
    if bet>=self.__class__.bet:
      self.bet = bet
      self.__class__.bet = bet
    else:
      self.bet = self.__class__.bet

  def call_(self):
    # last mei uske do baar katt gaye for somme reason
    self.bet = player.bet
    self.bank-=(self.bet-self.current_bet)
    player.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_()

  def fold_(self):
    if player.max_folds != len(player.players):
      self.play = False
      player.max_folds+=1
      a = player.players.index(self)
      key = 'player'+str(a+1)+'_score'
      player.player_scores.pop(key)

  def raise_(self):
    self.bank-=(self.bet-self.current_bet)
    player.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_() 

  def big_blind_(self, blind_bet):
    self.bank-=blind_bet
    self.current_bet=blind_bet
    player.big_blind_player = self
    player.pot+=blind_bet
  
  def small_blind_(self, blind_bet):
    self.bank-=blind_bet//2
    self.current_bet=blind_bet//2
    player.pot+=blind_bet//2
  
  def win_(self, players_in_play):
    self.bank+=player.pot
    player.pot = 0
    player.turn += 1
    self.prev_bank = self.bank
    players_in_play.remove(self)
    return players_in_play
    
  
  def draw_(self, draw_winnings):
    self.bank += draw_winnings
    player.pot -= draw_winnings
    self.prev_bank = self.bank

p1_name = input("Enter first player: ")
p2_name = input("Enter second player: ")
p3_name = input("Enter third player: ")
bank = int(input("Enter bank: "))
p1 = player(p1_name, bank) 
p2 =  player(p2_name, bank)
p3 = player(p3_name, bank)


# players_in_play = player.check_player_play(players_in_play)
def ante(ante):
  for k in player.players:
    player.pot+=ante
    k.bank-=ante

def blind_bet():
  for i in range(player.num_players):
    print(i)
    print(player.players)
    if (player.turn)%(player.num_players)==i & i < (player.num_players-2):
      player.blind_(player.players[i+1], player.players[i+2], player.blind_bet)
      break
    elif (player.turn)%(player.num_players) == (player.num_players-2):
      player.blind_(player.players[-1], player.players[0], player.blind_bet)
      break
    elif (player.turn)%(player.num_players) == (player.num_players-1):
      player.blind_(player.players[0], player.players[1], 50)
      break

def add_cards():
  players_in_play = player.check_player_play(player.players.copy())
  hands = cards.distribute_cards(3)
  player.table_cards = hands['table_cards']
  k=1
  for i in players_in_play:
    i.cards = hands['hand%s' %k]
    scores = cards.compare_hands(hands, 3).copy()
    i.score = scores['player%s_score' %k]
    k+=1
  k=1
  player.player_scores = cards.compare_hands(hands, 3).copy()
  return players_in_play

def pre_card_bet():
  players_in_play = player.players.copy()
  while player._play_ == True:
    for i in players_in_play:
      print(i.cards)
      if i.check == True:
        continue
      else:
        a = int(input(f"Enter option {i.name}: "))
        if a == 1:
          i.call_()
          if player.check == True:
            print("Check")
          else:
            print("Called ", player.bet)
        elif a == 2:
          b = int(input("Enter bet: "))
          i.bet_(b)
          i.raise_()
          for j in players_in_play:
            if j == i:
              continue
            else:
              j.uncheck_()
          print("Raised to ", (b))
        elif a == 3:
          if (i == player.big_blind_player) & (player.big_blind_player.current_bet == 50):
            continue
          else:
            i.fold_()
            print("Folded")
        else:
          continue
        i.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
        print(i.bank)
  for k in player.players:
    k.reset()
  player.reset_cls()
  
def post_card_bet():
  players_in_play = player.check_player_play(player.players.copy())
  while player._play_ == True:
    for i in players_in_play:
      if i.check == True:
        continue
      else:
        a = int(input(f"Enter option {i.name}: "))
        if a == 1:
          i.call_()
          if player.check == True or player.bet == 0:
            print("Check") 
          else:
            print("Called ", player.bet)
        elif a == 2:
          b = int(input("Enter bet: "))
          i.bet_(b)
          i.raise_()
          for j in players_in_play:
            if j == i:
              continue
            else:
              j.uncheck_()
          print("Raised to ", (b))
        elif a == 3:
          if player.check == False:
            i.fold_()
            print("Folded")
          else:
            continue
        else:
          continue
        i.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
        print(i.bank)
  for k in player.players:
    k.reset()
  player.reset_cls()

def compare_score(player_scores, num_players, players_in_play):
  max_score = max(player_scores.values())
  unique_scores = cards.remove_dup_list(player_scores.values())[0]
  d = cards.remove_dup_list(player_scores.values())[1]
  if d[max(d.keys())] == 1:
    for z in range(0,num_players):
      if max_score == player_scores["player%s_score" %(z+1)]:
        print(f"{add_cards()[z].name} wins")
        add_cards()[z].win_(players_in_play)
        key = 'player' + str(z+1) + '_score'
        player.player_scores.pop(key)
  else:
    draw_winnings = player.draw_winnings_(d[max(d.keys())])
    for y in add_cards():
      if y.score == max(d.keys()):
        y.draw_(draw_winnings)
    print('Draw')

while True:
  add_cards()
  ante(5)
  blind_bet()
  pre_card_bet()
  players_in_play = player.check_player_play(player.players.copy())
  while len(players_in_play) != 1:
    print("end of pre flop bet")
    print(player.table_cards[0:3])
    post_card_bet()
    players_in_play = player.check_player_play(player.players.copy())
    print(player.table_cards[0:4])
    post_card_bet()
    players_in_play = player.check_player_play(player.players.copy())
    print(player.table_cards)
    post_card_bet()
    players_in_play = player.check_player_play(player.players.copy())
    break
  if len(players_in_play) == 1:
    print(players_in_play[0].name, " wins")
    players_in_play[0].win_(players_in_play)
  else:
    while player.pot != 0:
      compare_score(player.player_scores, len(players_in_play), players_in_play)
      players_in_play = player.check_player_play(player.players.copy())
  print(p1.bank)
  print(p2.bank)
  print(p3.bank)
  print(player.pot)
