from random import Random
from typing import List
from game.game_state import GameState
import game.character_class
from game.item import Item
import util.utility as util
from game.position import Position
from strategy.strategy import Strategy
from game.player_state import PlayerState
import math
 
center = [Position(4,4), Position(4,5), Position(5,4), Position(5,5)]
 
def manhattan_distance(p1: Position, p2: Position) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
 
def chebyshev_distance(p1: Position, p2: Position) -> int:
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y))
 
def find_closet_center(position: Position) -> Position:
    closet_dist = None
    target_index = None
    for i in range(len(center)):
        if closet_dist is None:
            closet_dist = manhattan_distance(position,center[i])
            target_index = i
        elif(manhattan_distance(position,center[i]) < closet_dist):
            closet_dist = manhattan_distance(position,center[i])
            target_index = i
    return center[target_index]
 
def is_center(my_position: Position):
    x = my_position.x
    y = my_position.y
    for p in center:
        if(x == p.x and y == p.y):
            return True
    return False
 
def get_tiles_in_attack_range(my_position: Position, my_range: int) -> List[tuple]:
    reachable_list = []
    for x in range(-my_range, my_range+1):
        for y in range(-my_range, my_range+1):
            if (chebyshev_distance(my_position, Position(x,y)) <= my_range  and (x != 0 and y != 0) and util.in_bounds(Position(x,y))):
                reachable_list.append((my_position.x + x, my_position.y + y))
               
    return reachable_list
 
def get_reachable_tiles(my_position: Position, my_speed: int) -> List[tuple]:
    reachable_list = []
    for x in range(-my_speed, my_speed+1):
        for y in range(-my_speed, my_speed+1):
            if (manhattan_distance(my_position, Position(x,y)) and util.in_bounds(Position(x,y))):
                reachable_list.append((my_position.x + x, my_position.y + y))
               
    return reachable_list

#def check_possible_attack_next_turn(game_state: GameState):
    
class Wiz_Strategy(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.WIZARD
 
    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        sp_arr = [Position(0,0),Position(9,0),Position(9,9),Position(0,9)]
        player_list = game_state.player_state_list
        my_position = player_list[my_player_index].position
        my_coin = player_list[my_player_index].gold
        my_health = player_list[my_player_index].health
        my_range = player_list[my_player_index].stat_set.range
        my_speed = player_list[my_player_index].stat_set.speed
        my_item = player_list[my_player_index].item
        
        if(((my_coin >= 5 and my_health <= 3) or my_coin >= 8) and my_item == Item.NONE):
            return sp_arr[my_player_index]
       
        opponents = []
        
        for player_index in range(len(player_list)):
            if(player_index != my_player_index):
                opponents.append(player_list[player_index])
        
       
        if(is_center(my_position)):
            if(my_position.x == 4 and my_position.y == 4):
                return Position(5,5)    
            elif(my_position.x == 4 and my_position.y == 5):
                return Position(5,4) 
            elif(my_position.x == 5 and my_position.y == 4):
                return Position(4,5) 
            elif(my_position.x == 5 and my_position.y == 5):
                return Position(4,4)         
            else:
                 my_position                 
        else:
            attacked_tiles = []
            reachable_tiles = get_reachable_tiles(my_position, my_speed)
            #for (x,y) in reachable_tiles:
                #for o in opponents:
                    #if(chebyshev_distance((Position(x,y),):
                    
                    
            return find_closet_center(my_position)
       
    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        opponents = []
        player_list = game_state.player_state_list
        my_position = player_list[my_player_index].position
        my_attack_range = player_list[my_player_index].stat_set.range
        my_health = player_list[my_player_index].health
        my_damage = player_list[my_player_index].stat_set.damage
        for player_index in range(len(player_list)):
            if(player_index != my_player_index):
                opponents.append(player_list[player_index])
 
        chosen_opponent = None
        for o in opponents:
            if(chebyshev_distance(my_position, o.position) <= my_attack_range):
                if(o.stat_set.damage >= my_health and my_damage >= o.health):
                    chosen_opponent = o
                    return player_list.index(chosen_opponent)
                    break
                elif(my_damage >= o.health):
                    chosen_opponent = o
                    return player_list.index(chosen_opponent)
                    break
                else:
                    chosen_opponent = o
        if (chosen_opponent is None):
            return my_player_index
        else:
            return player_list.index(chosen_opponent)
            
    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        player_list = game_state.player_state_list
        my_coin = player_list[my_player_index].gold
        if(my_coin >= 8):
            return Item.PROCRUSTEAN_IRON
        else:
            return Item.NONE
 
    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return True
