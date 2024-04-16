import random
import math

# def create_random_array(length):
#     human_movement = 3
#     return [round(random.uniform(-human_movement, human_movement),1) for _ in range(length)]


# def human_mobility_model(x:float, y:float,timeStamp:int,boundary_x:float,boundary_y:float) -> list:
#     positions = []
#     random_x = create_random_array(x,timeStamp + 1)
#     random_y = create_random_array(y,timeStamp + 1)

#     for i in range(timeStamp):
#         new_x = round(x + random_x[i],1)
#         new_y = round(y + random_y[i],1)

#         if(new_x < -boundary_x):
#             new_x = -boundary_x
#         if(new_x > boundary_x):
#             new_x = boundary_x
#         if(new_y > boundary_y):
#             new_y = boundary_y
#         if(new_y < -boundary_y):
#             new_y = -boundary_y

#         positions.append({new_x,new_y})
#         x = new_x
#         y = new_y
    
#     return positions


class RandomWalker:
    def create_walk_with_angle(self, x, y, timeStamp, boundary):
        theta = random.uniform(0, 2*math.pi)
        distance = random.uniform(0,1)
        arr = []
        for i in range(timeStamp):
            new_x = round(x + distance * math.cos(theta), 1)
            new_y = round(y + distance * math.sin(theta), 1)
            while (new_x > boundary or new_y > boundary or new_x < -boundary or new_y < -boundary):
                theta = random.uniform(0, 2*math.pi)
                new_x = round(x + distance * math.cos(theta), 1)
                new_y = round(y + distance * math.sin(theta), 1)
            arr.append((new_x, new_y))
            x = new_x
            y = new_y

        return arr

    def human_walk_model(self, x: float, y: float, boundary: float, timeStamp: int) -> list:
        positions = self.create_walk_with_angle(x, y, timeStamp, boundary)
        return positions

# walker = RandomWalker()
# path = walker.human_walk_model(1,2,500,20)
# print(path)

# pos = human_mobility_model(2.4,5.5,10)
# print(pos)