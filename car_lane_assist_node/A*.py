import numpy as np
import heapq
import matplotlib.pyplot as plt


grid_width = 1 # meters
grid_height = 1 # meters
grid_resolution = 0.02 # meters/cell


num_x_cells = int(grid_width / grid_resolution)
num_y_cells = int(grid_height / grid_resolution)


grid = np.zeros((num_x_cells, num_y_cells), dtype=bool)

#tial data
lidar_data = [(0.5, 0.8),(0.9, 0.5), (0.5, 0.5),(0.6,0.3),(0.5,0.02),(0.45,0.55), (0.3,0.6)]
for point in lidar_data:
    
    if point[0] >= 0 and point[0] < grid_width and point[1] >= 0 and point[1] < grid_height:
        
        x = int(np.round(point[0] / grid_resolution))
        y = int(np.round(point[1] / grid_resolution))
        
        grid[x, y] = True


occupied_cells = np.argwhere(grid).tolist()
print("Occupied cells: ", occupied_cells)

def heuristic(node1, node2):
   
    return np.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

def plan_path(start_node, goal_node, occupied_cells):
    
    
    heap = []
    heapq.heappush(heap, (0, start_node))

    
    visited = set()
    costs = {start_node: 0}
    parents = {}

    while heap:
        
        current = heapq.heappop(heap)[1]

        
        if current == goal_node:
            
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            path.reverse()
            return path, start_node, goal_node

        
        visited.add(current)

        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                
                if dx == 0 and dy == 0:
                    continue
                neighbor_node = (current[0]+dx, current[1]+dy)
                if neighbor_node[0] < 0 or neighbor_node[0] >= num_x_cells or neighbor_node[1] < 0 or neighbor_node[1] >= num_y_cells:
                    continue
                if grid[neighbor_node[0], neighbor_node[1]]:
                    continue
                neighbor_cost = costs[current] + heuristic(current, neighbor_node)
                if neighbor_node not in costs or neighbor_cost < costs[neighbor_node]:
                    costs[neighbor_node] = neighbor_cost
                    parents[neighbor_node] = current
                    priority = neighbor_cost + heuristic(neighbor_node, goal_node)
                    heapq.heappush(heap, (priority, neighbor_node))
        
    
    return None, start_node, goal_node


start_node = (num_x_cells // 2, num_y_cells - 1)
goal_node = (num_x_cells // 2, 0)

# create a path
path, start, goal = plan_path(start_node, goal_node, occupied_cells)
if path is None:
    print("No path found.")
else:
    print("Path found:", path)
    print("Start node:", start)
    print("Goal node:", goal)




fig, ax = plt.subplots()
ax.imshow(grid.T, origin='lower')
ax.scatter([x[0] for x in occupied_cells], [x[1] for x in occupied_cells], color='red', s=10)
ax.scatter(start_node[0], start_node[1], color='blue', s=50, marker='o')
ax.scatter(goal_node[0], goal_node[1], color='green', s=50, marker='o')
ax.set_xticks(np.arange(0, num_x_cells, 1))
ax.set_yticks(np.arange(0, num_y_cells, 1))
#ax.set_xticklabels(np.arange(0, grid_width, grid_resolution))
#ax.set_yticklabels(np.arange(0, grid_height, grid_resolution))
ax.grid(linestyle='-', linewidth=0.5, color='gray', alpha=0.2)
#plt.show()


if path is not None:
    
    x_coords = [node[0] for node in path]
    y_coords = [node[1] for node in path]
    ax.plot(x_coords, y_coords, color='green')
    plt.show()

