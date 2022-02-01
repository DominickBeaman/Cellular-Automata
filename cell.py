from random import randrange

class Cell:
    def __init__(self, pos, alivethreshold, agingspeed, chanceofage, ageenabled, singleage, randombirth, randomdeath):
        self.pos = pos
        self.ageenabled = ageenabled
        self.singleage = singleage
        self.randomdeath = randomdeath
        self.chanceofage = chanceofage
        self.random_age()
        self.age = self.random_age()
        if(self.singleage is not None):
            self.age = [self.age[self.singleage], self.age[self.singleage], self.age[self.singleage]]
        self.newage = [0,0,0]
        self.alivethreshold = alivethreshold
        self.agingspeed = agingspeed
        self.randombirth = randombirth
    
    def random_age(self):
        val = [0,0,0]
        chance = randrange(1001)/1000
        if(chance < self.chanceofage and self.ageenabled[0]):
            val[0] = randrange(1001)/ 1000
        if(chance < self.chanceofage and self.ageenabled[1]):
            val[1] = randrange(1001)/ 1000
        if(chance < self.chanceofage and self.ageenabled[2]):
            val[2] = randrange(1001)/ 1000
        return val

    def clean_random_age(self, min):
        val = [0,0,0]
        if(self.ageenabled[0]):
            val[0] = randrange(int(1000*(1 - min)))/ 1000 + min
        if(self.ageenabled[1]):
            val[1] = randrange(int(1000*(1 - min)))/ 1000 + min
        if(self.ageenabled[2]):
            val[2] = randrange(int(1000*(1 - min)))/ 1000 + min
        return val

    def store_neighbors(self, board, width, height, roundrobin):
        x = self.pos[0]
        y = self.pos[1]
        self.neighbors = []
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                self.neighbors.append(board[(i + width) % width, (j + height) % height])
    
    def get_neighbor_count(self):
        return len(self.neighbors)

    def get_color(self):
        return (int(self.age[0] * 255),int(self.age[1] * 255),int(self.age[2] * 255))
    
    def get_neighbor_age_avg(self, mult):
        vals = [0,0,0]
        num = 0
        for n in self.neighbors:
            if(n.get_alive()):
                num += 1
                vals[0] += n.age[0]
                vals[1] += n.age[1]
                vals[2] += n.age[2]
        for i in range(0, len(vals)):
            vals[i] = vals[i]/num*mult
            if(vals[i] > 1):
                vals[i] = 1
        return vals

    
    def get_alive(self):
        return self.age[0] + self.age[1] + self.age[2] >= self.alivethreshold

    def update(self, timestep):
        ne = self.get_alive_neighbors()
        if(self.get_alive()):
            if(self.ageenabled[0]):
                self.update_red(timestep, ne)
            if(self.ageenabled[1]):
                self.update_green(timestep, ne)
            if(self.ageenabled[2]):
                self.update_blue(timestep, ne)
            if(randrange(1001)/1000 < self.randomdeath):
                self.newage = [0,0,0]
        else:
            if ne > 3:
                self.newage = self.get_neighbor_age_avg(1.3)
            else:
                self.newage = [0,0,0]
            if(randrange(1001)/1000 < self.randombirth):
                self.newage = self.clean_random_age(.5)
    
    def update_age(self):
        if self.singleage is None:
            self.age = self.newage
        else:
            self.age = [self.newage[self.singleage], self.newage[self.singleage], self.newage[self.singleage]]

    def update_red(self, timestep, ne):
        self.newage[0] = self.age[0] - timestep * self.agingspeed
        if(self.newage[0] < 0):
            self.newage[0] = 0
        if(self.newage[0] > 1):
            self.newage[0] = 1

    def update_green(self, timestep, ne):
        self.newage[1] = self.age[1] - timestep * self.agingspeed
        if(self.newage[1] < 0):
            self.newage[1] = 0
        if(self.newage[1] > 1):
            self.newage[1] = 1

    def update_blue(self, timestep, ne):
        self.newage[2] = self.age[2] - timestep * self.agingspeed
        if(self.newage[2] < 0):
            self.newage[2] = 0
        if(self.newage[2] > 1):
            self.newage[2] = 1


    
    def get_alive_neighbors(self):
        amt = 0
        for n in self.neighbors:
            if n.get_alive():
                amt += 1
        return amt

