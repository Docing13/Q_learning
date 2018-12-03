from tkinter import Canvas,Label,Tk
import threading
import random
import time

class map_generator():
    '''This class provides level creation.
    '''
    def __init__(self):
        '''Info about level`s obstacles and their coords
        '''
        self.map_size = 16
        self.map0 = [[1,4],[1,9],
             [2,1],[2,2],[2,4],[2,5],[2,6],[2,9],[2,12],[2,13],[2,14],
             [3,9],[3,12],
             [4,4],[4,5],[4,12],
             [5,2],[5,4],[5,7],[5,8],[5,9],
             [6,1],[6,2],[6,7],[6,12],[6,13],[6,14],
             [7,5],[7,6],[7,7],[7,8],[7,9],[7,10],[7,13],
             [8,7],
             [9,7],[9,11],
             [10,4],[10,7],[10,9],[10,10],[10,11],[10,12],[10,13],[10,14],
             [11,1],[11,2],[11,3],[11,4],[11,9],[11,13],
             [13,2],[13,3],[13,4],[13,5],[13,6],[13,7],[13,9],[13,11],[13,12],[13,13],
             [14,6],[14,9],[14,13]
             ]
    
    def make_canvas(self):
        '''creating level`s canvas
        '''
        can = []
        for y in range(self.map_size):
            for x in range(self.map_size):
                mc = move_cell()
                mc.position_y = y
                mc.position_x = x
                can.append(mc)
        return can
    
    def make_border(self):   
        '''returns arr of perimeter with obstacles
        '''     
        mb = []
        for _ in range(self.map_size):
            w = wall()
            w.position_x = 0
            w.position_y = _
            mb.append(w)
        for _ in range(self.map_size + 1):
            w = wall()
            w.position_x = self.map_size
            w.position_y = _
            mb.append(w)
        for _ in range(self.map_size):
            w = wall()
            w.position_x = _
            w.position_y = 0
            mb.append(w)
        for _ in range(self.map_size):
            w = wall()
            w.position_x = _
            w.position_y = self.map_size
            mb.append(w)
        for _ in range(self.map_size):
            w = wall()
            w.position_x = 0
            w.position_y = _
            mb.append(w)
        return mb
    
    def make_inside(self, inside_poligon):
        '''returns arr with inside parts of level
        inside_poligon - arr with obstacles coords
        '''
        arr = []
        for _ in inside_poligon:
            w = wall()
            w.position_y = _[0]
            w.position_x = _[1]
            arr.append(w)
        return arr
        
    def make_decorations(self):
        '''returns arr with special elements of level
        like target
        '''
        t = target()
        arr = []
        arr.append(t)
        return arr
        
    def generate_map1(self):
        '''returns summary map arr for map1:
        map1 - map with obstacles inside level
        '''
        full_map = self.make_canvas() + self.make_border() + self.make_inside(self.map0) + self.make_decorations()
        return full_map
    
    def generate_map0(self):
        '''returns summary map arr for map0:
        map0 - map with obstacles only on the level` perimeter
        '''
        full_map = self.make_canvas() + self.make_border() + self.make_decorations()
        return full_map
          
class move_cell():
    '''class for moving cell creation
    '''
    def __init__(self, target_position_y = 0, target_position_x = 0, marker = 0):
        '''position of cell in coords x and y
        marker is using for noneGUI or debugging
        '''
        self.position_x = target_position_x
        self.position_y = target_position_y
        self.marker = marker 
               
class target():
    '''class for target creation
    '''
    def __init__(self, target_position_y = 1, target_position_x = 14, marker = 3):
        '''position of target point in coords x and y
        marker is using for noneGUI or debugging
        '''
        self.position_x = target_position_x
        self.position_y = target_position_y
        self.marker = marker

class wall():
    '''class for wall(obstacle) creation
    '''
    def __init__(self, marker = 5, wall_position_x = 0, wall_position_y = 0):   
        '''position of wall point in coords x and y
        marker is using for noneGUI or debugging
        '''     
        self.marker = marker
        self.position_x = wall_position_x
        self.position_y = wall_position_y
        
class Q_agent():
    '''class for Q agent creation
    '''
    def __init__(self, marker = 1, agent_position_y = 14, agent_position_x = 1, trip_marker = 8):
        '''position of wall point in coords x and y
        marker is using for noneGUI or debugging
        trip_marker is using for tracering the way
        that agent went
        '''
        #reward dict provides get reward for every state
        self.reward0 = {
            (11, 16): -1, (16, 6): -1, (16, 16): -1, (1, 16): -1,
            (16, 9): -1, (0, 14): -1, (4, 16): -1, (8, 0): -1,
            (16, 2): -1, (0, 7): -1, (0, 16): -1, (7, 16): -1,
            (0, 10): -1, (12, 16): -1, (16, 14): -1, (0, 3): -1,
            (16, 7): -1, (4, 0): -1, (9, 0): -1, (16, 10): -1,
            (0, 15): -1, (0, 6): -1, (16, 3): -1, (15, 0): -1,
            (14, 1): 100, (13, 16): -1, (3, 0): -1, (0, 11): -1,
            (5, 0): -1, (0, 4): -1, (3, 16): -1, (10, 0): -1,
            (8, 16): -1, (2, 16): -1, (16, 11): -1, (0, 0): -1,
            (16, 15): -1, (16, 4): -1, (6, 0): -1, (0, 12): -1,
            (11, 0): -1, (9, 16): -1, (16, 0): -1, (0, 5): -1,
            (16, 5): -1, (1, 0): -1, (0, 8): -1, (16, 12): -1,
            (0, 1): -1, (7, 0): -1, (14, 16): -1, (5, 16): -1,
            (12, 0): -1, (10, 16): -1, (16, 8): -1, (0, 13): -1,
            (6, 16): -1, (16, 1): -1, (2, 0): -1, (0, 9): -1, 
            (15, 16): -1, (16, 13): -1, (0, 2): -1, (13, 0): -1,
             (14, 0): -1
             }
        self.reward1 = {}
        m = map_generator()
        
        for obj in m.generate_map1():
            if obj.marker == 5:
                x = obj.position_x
                y = obj.position_y
                self.reward1[(x,y)] =- 506
            if obj.marker == 3:
                x = obj.position_x
                y = obj.position_y
                self.reward1[(x,y)] = 300    
        self.marker = marker
        self.position_x = agent_position_x
        self.position_y = agent_position_y
        self.trip_marker = trip_marker 
        #reward
        self.r = 0
        self.size = 15        
        #how much powerful agent`s fate into a new info
        self.gamma = 0.9
        #possible actions    
        self.actions = (1, 2, 3, 4)        
        #coords
        self.coordinates = []
        #state
        self.s = None
        self.s_ = None
        #start action
        self.a = 1
        self.a_ = None           
        self.choice = ''    
        self.Q = {}
        #for epsilon greedy algorithm
        self.epsilon = 1
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.eps_bool = False
        #learning rate alfa - less digit and agent will think less about future step`s advantages
        self.alfa = 0.95
    def get_reward(self):
        '''generate reward from state
        '''
        reward =- 10
        coord = (self.position_x, self.position_y)
        if coord in self.reward1:
            reward = self.reward1[coord] 
        return reward 
    
    def Q_init(self):
        '''generate Q dict randomly
        '''
        for y in range(0, self.size + 1 + 1):
            for x in range(0, self.size + 1 + 1):
                self.coordinates.append((y,x))
        for _ in self.coordinates:
            for a in self.actions:
                self.Q[_, a] = random.random()

    # methods for move
    def move_right(self):
        self.position_x += 1
        
    def move_left(self):
        self.position_x -= 1  
          
    def move_up(self):
        self.position_y -= 1
        
    def move_down(self):
        self.position_y += 1 
    #methods for taking position
    def get_pos_x(self):
        return self.position_x
    
    def get_pos_y(self):
        return self.position_y
    
    def make_move(self):
        '''generates move depending on 
        current action
        '''
        if self.a == 1:
            self.move_up()
        if self.a == 2:
            self.move_right()
        if self.a == 3:
            self.move_down()
        if self.a == 4:
            self.move_left()
            
    def look_around(self):
        '''for taking current state
        '''
        return (self.position_y, self.position_x)      
    
    def epsilon_greedy_algoritm(self):
        '''for generating randomly move
        with epsilon rate
        '''
        self.eps_bool = False
        if random.random() <= self.epsilon:
            self.a = random.randint(1, 4)
            self.make_move()
            self.s = self.look_around()
            self.eps_bool = True
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def init(self):
        '''init Q and current state
        '''
        self.Q_init()
        self.s = self.look_around()
    
    def run(self):
        '''main method for Q algorithm
        1). getting state S
        2). chose (a)ction from Q by (s)tate
        3). getting r(eward) after (a)ction realisation
        4). getting new current (s_)tate
        5). updating Q
        6). set s = s_
        7). repeat from 2).  
        '''
        buff = []
        for keys in self.Q.keys():
            if keys[0] == self.s:
                buff.append((keys[1], self.Q[keys]))
        subbuff = []
        for i in buff:
            subbuff.append(i[1])
        index = subbuff.index(max(subbuff))
        self.a = buff[index][0]
        self.make_move()
        self.r = self.get_reward()
        self.s_ = self.look_around()
        key = (self.s,self.a)
        
        buff = []
        for keys in self.Q.keys():
            if keys[0] == self.s_:
                buff.append((keys[1], self.Q[keys]))
        subbuff = []
        for i in buff:
            subbuff.append(i[1])
        index = subbuff.index(max(subbuff))
        tipa_a = buff[index][0]
        key_plus = (self.s_, tipa_a)
        self.Q[key] += self.alfa * (self.r + self.gamma * self.Q[key_plus] - self.Q[key])
        self.s = self.s_
        

class graphics():
    '''class for GUI creation
    '''
    def __init__(self):
        self.agent_image = None
        self.m_generator = map_generator()
        self.m1 = self.m_generator.generate_map1()
        self.m0 = self.m_generator.generate_map0()
        self.start_x = 1
        self.start_y = 14
        self.q_agent = Q_agent(agent_position_x = self.start_x, agent_position_y = self.start_y)
        self.game_finish = False
        self.reward = {}
        self.walls = []
        self.target = None
        self.rectangle_size = 50
        self.oval_size = 50
        self.width = self.rectangle_size * (self.m_generator.map_size + 1)
        self.height = self.width
        self.score = 0
        self.steps = 0
        self.local_steps = 0
        self.num_games = 0 
        self.root = Tk()
        self.can = Canvas(self.root, width=self.width, height=self.height, bg='lightblue')
        self.can.pack()
        self.label = Label(self.root) 
        self.label.pack(side = 'bottom')         
        self.init()
        
    def init(self):
        '''inits map, agent, reward
        '''
        self.create_map()
        self.init_agent()
        for obj in self.m0:
            if type(obj) == type(target()):
                    self.target = obj
                    self.reward[(obj.position_x, obj.position_y)] = 100      
            if type(obj) == type(wall()):
                    self.walls.append(obj)
                    self.reward[(obj.position_x, obj.position_y)] =- 1

    def write_score_steps(self,score,steps,local_steps,num_games):
        '''writing info on GUI
        '''
        info = 'SCORE: ' + str(score) + ' ;' + '\n' + 'STEPS: ' + str(steps) + ' ;'
        info1 = 'STEPS IN THIS GAME:  ' + str(local_steps) + ' ;' + '\n' + 'GAMES: ' + str(num_games) + ' ;'
        sum_info = info + info1
        self.label.config(text = sum_info)    

    def create_map(self):   
        '''creating graphical content
        '''
        fill = ''
        for _ in self.m1:
            if _.marker == 0:
                fill = 'white'
            if _.marker == 3:
                fill = 'green'
            if _.marker == 5:
                fill = 'black'
            self.can.create_rectangle(self.rectangle_size * _.position_x,
                                      _.position_y * self.rectangle_size,
                                      (_.position_x * self.rectangle_size) + self.rectangle_size,
                                      (_.position_y * self.rectangle_size) + self.rectangle_size,
                                      fill = fill,outline='blue')
            
    def init_agent(self):
        '''inits agent on level
        '''
        a=self.q_agent
        self.q_agent.init()
        self.agent_image = self.can.create_oval(self.oval_size * a.position_x,
                             a.position_y * self.oval_size,
                             (a.position_x * self.oval_size) + self.oval_size,
                             (a.position_y * self.oval_size) + self.oval_size,
                             fill = 'yellow', outline = 'blue')
        self.can.pack() 

    def move_agent(self):
        '''moves agent on level
        '''
        self.can.coords(self.agent_image,
                        self.q_agent.position_x * self.oval_size,
                        self.q_agent.position_y * self.oval_size,
                        (self.q_agent.position_x * self.oval_size) + self.oval_size,
                        (self.q_agent.position_y * self.oval_size) + self.oval_size)    
        self.local_steps += 1    

    def restart(self):
        '''resets agent coords to start position
        '''
        self.q_agent.position_x = self.start_x
        self.q_agent.position_y = self.start_y
        
    def check_rules(self):
        '''checking for finish
        '''
        for w in self.walls:
            if self.q_agent.get_pos_y() == w.position_y and self.q_agent.get_pos_x() == w.position_x:
                self.restart()
                break
        if  self.q_agent.position_y == self.target.position_y and self.q_agent.position_x == self.target.position_x:
            self.game_finish = True
            self.restart()
            self.num_games += 1
            self.local_steps = 0

    def run(self):
        '''main method with all math 
        and mechanics
        '''
        self.write_score_steps(self.score, self.steps, self.local_steps, self.num_games)
        self.check_rules()        
        self.q_agent.run()
        self.move_agent()
        #for watching ability
        time.sleep(0.02)

    def core_loop(self):        
        while True:
            self.run()

    def loop(self):        
        while True:
            self.root.mainloop()

g=graphics()
g.init()
t=threading.Thread(target=g.core_loop)
t.start()
g.root.mainloop()




