from expand import expand

def dequeue_here (priority_queue, dis_map, end):  # function to perform dequeue on priority queue
	if len(priority_queue) == 0:
		return None

	if len(priority_queue) == 1:
		return 0

	min_node_index = 0

	for node_index in range(1, len(priority_queue)):
		if priority_queue[node_index][1] < priority_queue[min_node_index][1]:
			min_node_index = node_index
		elif priority_queue[node_index][1] == priority_queue[min_node_index][1]:
			if dis_map[priority_queue[node_index][0]][end] == None:
				min_node_index = node_index
			elif dis_map[priority_queue[min_node_index][0]][end] == None:
				pass
			elif dis_map[priority_queue[node_index][0]][end] < dis_map[priority_queue[min_node_index][0]][end]:
				min_node_index = node_index

	return min_node_index


def a_star_search (dis_map, time_map, start, end):
	priority_queue = [(start, dis_map[start][end], 0, [start])]
	visited_nodes = set()
	ans_found = False

	while priority_queue:
		#print(priority_queue)
		dequeue_index = dequeue_here(priority_queue, dis_map, end)
		curr_node = priority_queue[dequeue_index]
		
		del priority_queue[dequeue_index]
		if curr_node[0] in visited_nodes:
			continue
		visited_nodes.add(curr_node[0])


		if curr_node[0] == end:
			if ans_found and ans[1] > curr_node[1]:
				ans = curr_node
			else:
				ans = curr_node
				ans_found = True

		if ans_found and ans != curr_node and ans[1] <= curr_node[1]:
			break
		if curr_node[0] != end:
			neighbour_nodes = expand(curr_node[0], time_map)

			for node in neighbour_nodes:
				if node not in visited_nodes:
					priority_queue.append(
									(node, 
									curr_node[2] + time_map[curr_node[0]][node] + dis_map[node][end], 
									curr_node[2] + time_map[curr_node[0]][node],
									curr_node[3] + [node])
								)
	if ans_found:
		return ans[-1]

	return "No path found"





def dfs(time_map, start, end, visited):   # recursive function for performing the dfs

	if start in visited:
		return
	visited.add(start)

	if start == end:
		return [start]

	neighbor_nodes = expand(start, time_map)
	for neighbor in neighbor_nodes:
		next_node = dfs(time_map, neighbor, end, visited)
			
		if next_node:
			return [start] + next_node

def depth_first_search(time_map, start, end):
	visited = set()

	path = dfs(time_map, start, end, visited)

	if path:
		return path
	else:
		return "No path found"







def breadth_first_search(time_map, start, end):
	visited_nodes = set()
	helper_queue = [(start, start)]

	paths_dict = {start: [[start]]}

	for node in helper_queue:

		if node[1] in visited_nodes:
			continue
		else:
			visited_nodes.add(node[1])
			if node[1] in paths_dict.keys():
				paths_dict[node[1]].append(paths_dict[node[0]][-1] + [node[1]])
			else:
				paths_dict[node[1]] = [paths_dict[node[0]][-1] + [node[1]]]

		if node[1] == end:
			#print(paths_dict)
			#print(helper_queue)
			return paths_dict[node[1]][-1][1:]

		neighbor_nodes = expand(node[1], time_map)
		for neighbor in neighbor_nodes:
			helper_queue.append((node[1], neighbor))
	

	return "No path found"
