from .cards import add_score, add_high_card_score
import random

class player():
  def __init__(self, name,  bank, game):
    self.g = game
    self.g._bank_ = bank
    self.name = name
    self.bank = bank
    self.prev_bank = bank
    self.play = True
    self.cards = None
    self.g.players.append(self)
    self.g.num_players+=1
    self.all_in = False
    self.check = False
    self.score = 0
    self.reset()
    print(self.name, self.bank)

  def reset(self):
    self.bet = 0
    self.current_bet = 0
    self.check = False

  def check_(self):
    self.check = True
  
  def allin(self):
    self.all_in = True
    self.__class__.all_in_num+=1
    self.g.all_in_players.append(self)

  def un_all_in(self):
    self.all_in = False
    self.g.all_in_num-=1

  def uncheck_(self):
    if self.all_in:
      pass
    else:
      self.check = False

  def check_check_(self):
    if self.check == False:
      self.g.check = False
    else:
      pass

  def bet_(self, bet):
    self.g.check = False
    if bet >= self.bank:
      bet = self.bank
    else:
      pass
    if bet>=self.g.bet:
      self.bet = bet
      self.g.bet = bet
    else:
      self.bet = self.g.bet

  def call_(self):
    self.bet = self.g.bet
    if self.bet >= self.bank:
      self.g.pot+=self.bank
      self.bank = 0
      self.allin()
    else:
      self.bank-=(self.bet-self.current_bet)
      self.g.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_()

  def fold_(self):
    if not self.all_in:
      if self.g.max_folds != len(self.g.players):
        self.play = False
        self.g.max_folds+=1

  def raise_(self):
    if self.bet >= self.bank:
      self.allin()
      self.g.pot += self.bank
      self.bank = 0
    else:
      self.bank-=(self.bet-self.current_bet)
      self.g.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_() 

  def big_blind_(self, blind_bet):
    if self.bank <= blind_bet:
      self.g.pot += self.bank
      self.bank = 0
      self.allin()
    else:
      self.bank-=blind_bet
      self.g.pot+=blind_bet
    self.current_bet=blind_bet
    self.g.big_blind_player = self
  
  def small_blind_(self, blind_bet):
    if self.bank <= blind_bet//2:
      self.g.pot += self.bank
      self.bank = 0
      self.allin()
    else:
      self.bank-=blind_bet//2
      self.g.pot+=blind_bet//2
    self.current_bet=blind_bet//2
  
  def win_(self, players_in_play):
    self.bank+=self.g.pot
    self.g.pot = 0
    self.g.max_folds = 0
    self.g.turn += 1
    self.prev_bank = self.bank
    players_in_play.remove(self)
    for i in self.g.all_in_players:
      i.un_all_in()
    self.g.all_in_players.clear()
    self.g.reset_play_for_all()
    return players_in_play
  
  def draw_(self, draw_winnings):
    self.bank += draw_winnings
    self.g.pot -= draw_winnings
    self.prev_bank = self.bank
    self.g.reset_play_for_all()
    for i in self.g.all_in_players:
      i.un_all_in()
    self.g.all_in_players.clear()
    self.g.max_folds = 0

  def add_score(self):
    cards = self.cards + self.g.table_cards
    l1 = add_score(cards, 0)
    self.score += add_high_card_score(cards, l1[0], l1[1])

