import sys
import math




# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class pos:
    def __init__ (self,x:int,y:int):
        self.x = x
        self.y = y
        

class unit:
    def __init__ (self,id:int,pos:pos,owner:int,type:int,health:int):
        self.id = id
        self.pos = pos
        self.owner = owner
        self.type = type
        self.health = health
        


class site:
    def __init__ (self,id:int,pos:pos,radius:int,gold:int = None,maxMineSize: int = None,type:int = None,owner:int = None,turns:int = None,building:int = None,param_1:int = None,param_2:int = None) :
        self.id = id
        self.pos = pos
        self.radius = radius
        self.gold = gold
        self.maxMineSize = maxMineSize
        self.type = type
        self.owner = owner
        self.turns = turns
        self.building = building
        self.param_1 = param_1
        self.param_2 = param_2

def dist(a:pos,b:pos) -> float :
    return (math.sqrt(((a.x-b.x)**2)+((a.y-b.y)**2)))

def closest_unbuilt_site(unit):
    closest_dist = 100000000
    closest = -1
    for s in sites:
        distance = dist(unit.pos,sites[s].pos)
        if distance < closest_dist and sites[s].type == -1:
            closest_dist = distance
            closest = s
    return sites[closest]

def closest_mineable_site(unit):
    closest_dist = 100000000
    closest = -1
    
    for s in sites:
        mineable = False
        distance = dist(unit.pos,sites[s].pos)
        if sites[s].type == 0 and (sites[s].maxMineSize > sites[s].param_1):
            mineable = True
        if sites[s].type == -1:
            mineable = True
        if sites[s].owner != 0:
            mineable = True
        if sites[s].gold == 0:
            mineable = False
        if distance < closest_dist and mineable == True:
            closest_dist = distance
            closest = s
    return sites[closest]

def closest_site(unit):
    closest_dist = 100000000
    closest = -1
    for s in sites:
        distance = dist(unit.pos,sites[s].pos)
        if distance < closest_dist:
            closest_dist = distance
            closest = s
    return sites[closest]   

def closest_archer_to_foe():
    closest_dist = 100000000
    closest = "none"
    for s in sites:
        distance = dist(units[foe_queen].pos,sites[s].pos)
        # print(str(s) +" = " + str(distance), file=sys.stderr, flush=True)
        if distance < closest_dist and sites[s].type == 2 and sites[s].owner == 0 and sites[s].param_2 ==  1:
            closest_dist = distance
            closest = s
            # print("s= " + str(s), file=sys.stderr, flush=True)
    if closest == "none":
        return ""
    else:
        return " "+str(closest)  
    
def closest_knight_to_foe():
    closest_dist = 100000000
    closest = "none"
    for s in sites:
        distance = dist(units[foe_queen].pos,sites[s].pos)
        # print(str(s) +" = " + str(distance), file=sys.stderr, flush=True)
        if distance < closest_dist and sites[s].type == 2 and sites[s].owner == 0 and sites[s].param_2 ==  0:
            closest_dist = distance
            closest = s
            # print("s= " + str(s), file=sys.stderr, flush=True)
    if closest == "none":
        return ""
    else:
        return " "+str(closest)  

def closest_site_to_queen():
    # return the closets site to the foe queen that she is not touching
    closest_dist = 100000000
    closest = -1
    for s in sites:
        distance = dist(units[foe_queen].pos,sites[s].pos)
        if distance < closest_dist and dist(units[foe_queen].pos,sites[s].pos)>(sites[s].radius+50):
            closest_dist = distance
            closest = s
            # print("s= " + str(s), file=sys.stderr, flush=True)
    return sites[closest] 

def closest_unit(unit):
    pass



# game initialization - 1 time

sites:dict[int,site] = {}
units:list[unit] = []
game_phase = 0
turn = 0
my_start_point = pos(0,0)

num_sites = int(input())
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id]=site(site_id,pos(x,y),radius)

# game loop


while True:
    turn += 1
    units = []
    my_queen = -1
    foe__queen = -1
    my_knights = 0
    foe_knights = 0
    my_archers = 0
    foe_archers = 0
    my_abars = 0
    my_kbars = 0
    avail_kbars = 0
    avail_abars = 0
    my_mines = 0
    my_revenue = 0
    target_revenue = 5
    
    
    # touched_site: -1 if none
    my_gold, touched_site = [int(i) for i in input().split()]
    for i in range(num_sites):
        # ignore_1: used in future leagues
        # ignore_2: used in future leagues
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, gold, maxMineSize, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        sites[site_id].gold = gold
        sites[site_id].maxMineSize = maxMineSize
        sites[site_id].type = structure_type
        sites[site_id].owner = owner
        sites[site_id].param_1 = param_1
        sites[site_id].param_2 = param_2
        if owner == 0:
            if structure_type == 2 and param_2 == 0:
                my_kbars += 1
                if param_1 == 0:
                    avail_kbars += 1
            if structure_type == 2 and param_2 == 1:
                my_abars += 1
                if param_1 == 0:
                    avail_abars += 1
            if structure_type == 0:
                my_mines += 1
                my_revenue += param_1
            
        
    num_units = int(input())
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        units.append(unit(i,pos(x,y),owner,unit_type,health))
        if owner == 0 and unit_type == 1:
            my_archers +=1
        if owner == 0 and unit_type == 0:
            my_knights +=1
        if owner == 1 and unit_type == 1:
            foe_archers +=1
        if owner == 1 and unit_type == 0:
            foe_knights +=1
                
        if owner ==0 and unit_type == -1:
            my_queen = i
            if turn == 1:
                my_start_point = pos(x,y)
        if owner ==1 and unit_type == -1:
            foe_queen = i

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    
    if my_revenue <target_revenue:
        queen_action = "BUILD " + str(closest_mineable_site(units[my_queen]).id) + " MINE"
    elif my_kbars < 2:
        queen_action = "BUILD " + str(closest_unbuilt_site(units[my_queen]).id) + " BARRACKS-KNIGHT"
    elif my_abars <2:
        queen_action = "BUILD " + str(closest_unbuilt_site(units[my_queen]).id) + " BARRACKS-ARCHER"
    elif avail_kbars < 2:
        queen_action = "BUILD " + str(closest_site_to_queen().id) + " BARRACKS-KNIGHT"
    elif avail_kbars < 2:
        queen_action = "BUILD " + str(closest_site_to_queen().id) + " BARRACKS-ARCHER"
    else:
        queen_action = "BUILD " + str(closest_unbuilt_site(units[my_queen]).id) + " TOWER"
        #queen_action = "MOVE " + str(my_start_point.x) + " " + str(my_start_point.y)
        
    train_action = "TRAIN"
    if my_knights <= foe_knights and my_gold > 100:
        train_action += str(closest_archer_to_foe())
        my_gold -= 100 
    if my_gold > 80:
        train_action += str(closest_knight_to_foe())
    
    # First line: A valid queen action
    # Second line: A set of training instructions
    print(queen_action)
    print(train_action)
