import matplotlib.pyplot as plt
import random
import datetime
import os


def get_unique_id():
	return datetime.datetime.now().strftime("%y%m%d%H%M")

def draw_trajectories(filename="unknown", recording_start=10, collisions=False, collision_threshold=0.4):
	# FILES
	folder = "crowd_simulations/"
	unique_sim_id = get_unique_id()
	trajectory_files = os.listdir(folder)
	trajectories = [[[], []] for _ in range(len(trajectory_files))]
	# INITIALISATION
	collisions_x = []
	collisions_y = []
	current_agent = -1
	for file in trajectory_files:
		current_agent += 1
		if file[-1] != "v":
			continue
		time_step = -1
		for agent_t in open(folder + "/" + file).readlines():
			time_step += 1
			t1, x1, y1, _, _ = agent_t.strip().split(",")
			t1 = float(t1)
			if t1 < recording_start:
				continue
			x1 = float(x1)
			y1 = float(y1)
			trajectories[current_agent][0].append(x1)
			trajectories[current_agent][1].append(y1)
			# LOOK FOR COLLISIONS WITH NEIGHBOURS
			if not collisions:
				continue
			for neighbour_agent in trajectory_files[current_agent + 1:]:
				if neighbour_agent[-1] != "v" or file == neighbour_agent:
					continue
				neighbour_t = open(folder + "/" + neighbour_agent).readlines()[time_step]
				t2, x2, y2 = neighbour_t.split(",")
				if abs(float(t2) - t1) < 0.5 and (x1 - float(x2)) ** 2 + (y1 - float(y2)) ** 2 < collision_threshold ** 2:
					collisions_x.append(x1)
					collisions_y.append(y1)

	# ACTUALLY DRAW POSITIONS
	plt.figure(figsize=(5, 5))
	plt.axis("equal")
	#plt.axis("off")
	plt.scatter(collisions_x, collisions_y, color="black", zorder=0)
	for agent in trajectories:
		color = random.choice(["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"])
		firsttime = 0
		for time in range(len(agent[0]) - 1):
			if abs(agent[0][time] - agent[0][time + 1]) > 2 or abs(agent[1][time] - agent[1][time + 1]) > 2:
				plt.plot(agent[0][firsttime:time], agent[1][firsttime:time], zorder=1, color=color, linewidth=2)
				firsttime = time + 1
		plt.plot(agent[0][firsttime:-1], agent[1][firsttime:-1], zorder=1, color=color, linewidth=2)
		plt.scatter(agent[0][-1], agent[1][-1], s=80, zorder=2, color=color)

	# STORE FILE
	plt.savefig("figures/" + filename + "_" + unique_sim_id + ".png", dpi=150)
	plt.close('all')
