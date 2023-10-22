# じゃんけん強化学習
# player game 
# gameから相手が出した手と勝率が返される
# 100回ごとにplayerの確率リストが更新される
# result　1:player1勝利 2:player2勝利
import numpy as np
class Player:
    def __init__(self, cp, rock_p, scissors_p, paper_p):
            self.element_list = ['rock','scissors','paper']
            self.prob_list = [rock_p, scissors_p, paper_p]
            self.win_rate_list = [0,0,0]
            self.decision_list = []
            self.result_list = []
            self.cp = cp
            self.stop_learning = 0
    def decision(self):
        decision = np.random.choice(self.element_list, 1, p=self.prob_list)
        self.decision_list.append(decision[0])
        return decision
    def check_result(self, result):
        self.result_list.append(result)
    def add_prob_list(self, add_prob):
        self.prob_list = [self.prob_list[0] + add_prob[0], self.prob_list[1] + add_prob[1], self.prob_list[2] + add_prob[2]]
    def learning_add(self, win_rate):
        add_prob = [0,0,0]
        max_index = win_rate.index(max(win_rate))
        min_index = win_rate.index(min(win_rate))
        mid_index = win_rate.index(sorted(win_rate)[1])
        if(self.prob_list[mid_index] < 0.01 or self.prob_list[mid_index] > 0.99):
            self.stop_learning = 1
            print('stop learning')
        else:
            if( 0.99 > self.prob_list[max_index]) : 
                add_prob[max_index] += 0.01
            elif(self.prob_list[mid_index] > 0.01):
                # maxの要素を抜いてmaxのものをいじる
                add_prob[mid_index] += 0.01
            if(self.prob_list[min_index] > 0.01) : 
                add_prob[min_index] -= 0.01
            elif(self.prob_list[mid_index] > 0.01):
                # minの要素を抜いてminのものをいじる
                add_prob[mid_index] -= 0.01
        for i in range(0, len(self.prob_list)):
            if(self.prob_list[i] > 1):
                self.prob_list[i] = 1
            elif(self.prob_list[i] < 0):
                self.prob_list[i] = 0
        return add_prob
    def learning(self):
        if(self.cp == 0):
            r_count = 0
            s_count = 0
            p_count = 0
            r_score = 0
            s_score = 0
            p_score = 0
            r_score_rate = 0
            s_score_rate = 0
            p_score_rate = 0
            for i in range(0, len(self.result_list)):
                if(self.decision_list[i] == 'rock'):
                    r_count += 1
                    if(self.result_list[i] == 1):
                        r_score += 1
                    elif(self.result_list[i] == 2):
                        r_score -= 1
                elif(self.decision_list[i] == 'scissors'):
                    s_count += 1
                    if(self.result_list[i] == 1):
                        s_score += 1
                    elif(self.result_list[i] == 2):
                        s_score -= 1
                elif(self.decision_list[i] == 'paper'):
                    p_count += 1
                    if(self.result_list[i] == 1):
                        p_score += 1
                    elif(self.result_list[i] == 2):
                        p_score -= 1
            r_score_rate = r_score / r_count if r_count != 0 else 0
            s_score_rate = s_score / s_count if s_count != 0 else 0
            p_score_rate = p_score / p_count if p_count != 0 else 0
            winrate = [r_score_rate , s_score_rate, p_score_rate]
            print(winrate)
            add_prob = self.learning_add(winrate)
            self.add_prob_list(add_prob)
    def get_score(self):
        win_count = self.result_list.count(1)
        win_rate = win_count / len(self.result_list)
        return {'win_count': win_count, 'win_rate': win_rate}
    def get_result_list(self):
        return self.result_list
    def get_decision_list(self):
        return self.decision_list
    def get_prob_list(self):
        return self.prob_list
class Game:
    def __init__(self,player_a,player_b):
        self.player_1 = player_a
        self.player_2 = player_b
        self.result = [0,0]
    def play_game(self):
        player_1 = self.player_1.decision()
        player_2 = self.player_2.decision()
        self.judge(player_1,player_2)
    def judge(self,player_1,player_2):
        if(player_1 == 'rock'):
            if(player_2 == 'scissors'):
                self.result = [1,2]
            elif(player_2 == 'paper'):
                self.result = [2,1]
        elif(player_1 == 'scissors'):
            if(player_2 == 'rock'):
                self.result = [2,1]
            elif(player_2 == 'paper'):
               self.result = [1,2]
        elif(player_1 == 'paper'):
            if(player_2 == 'rock'):
                self.result = [1,2]
            elif(player_2 == 'scissors'):
                self.result = [2,1]
        print(player_1,player_2,self.result)
        self.player_1.check_result(self.result[0])
        self.player_2.check_result(self.result[1])
# field
player1 = Player(0,0.4,0.3,0.3)
player2 = Player(1,0.3,0.4,0.3)

learning_count = 0
END_COUNT = 10
LEARNING_END_COUNT = 100
while learning_count < LEARNING_END_COUNT:
    game_count = 0
    while game_count < END_COUNT:
        game = Game(player1,player2)
        game.play_game()
        game_count += 1
    player1.learning()
    player2.learning()
    learning_count += 1

# print(player1.get_score())
# print(player2.get_score())
print(player1.get_prob_list())
print(player2.get_prob_list())
