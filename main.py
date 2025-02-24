import random
import math
import os
import visualiser

def write_agents(f, num_agents, road_width=20):
    #crossing pedestrians
    for i in range(num_agents):
        x = road_width if i % 2 == 0 else -road_width
        y = i * 0.3
        x_init = round(x, 2)
        y_init = round(y, 2)
        x_goal = round(-x, 2)
        y_goal = round(y, 2)

        #write init file
        f.write("\t" * 2 + "<Agent rad=\"0.3\" pref_speed=\"1.3\" max_speed=\"1.6\">\n")
        f.write("\t" * 3 + "<Policy id=\"0\"/>\n")
        f.write("\t" * 3 + "<pos x=\"" + str(x_init) + "\" y=\"" + str(y_init) + "\"/>\n")
        f.write("\t" * 3 + "<goal x=\"" + str(x_goal) + "\" y=\"" + str(y_goal) + "\"/>\n")
        f.write("\t" * 2 + "</Agent>\n")


def write_init(input_file, num_agents=5, recording_start=10, simulation_length=100):
    f = open(input_file, "w")

    # CREATE WORLD
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n")
    f.write("<Simulation delta_time=\"0.01\" end_time=\"" + str(simulation_length + recording_start) + "\">" + "\n")
    f.write("\t<World type=\"Infinite\" />\n")

    # CREATE AGENTS
    f.write("\t<Agents>\n")
    write_agents(f, num_agents, 25)
    f.write("\t</Agents>\n")

    # WRITE POLICIES
    f.write("\t<Policies>\n")
    f.write("\t\t<Policy id=\"0\" OptimizationMethod=\"global\" RelaxationTime=\"0.5\">\n")
    f.write("\t\t\t<costfunction range=\"5\" name=\"ORCA\" />\n")
    f.write("\t\t</Policy>\n\t</Policies>\n")
    f.write("</Simulation>\n")
    f.close()


if __name__ == '__main__':
    #crowd initialisation
    umans_path = "../../Projects/UMANS-master/build/UMANS-ConsoleApplication-Linux"
    scenario_file = "crowd_initialisation/test1.xml"
    write_init(scenario_file, 4, 8, 20)

    #run simulation
    command = "rm -rf crowd_simulations/*.csv"
    os.system(command)
    command = umans_path + " -i " + scenario_file + " -o crowd_simulations"
    os.system(command)

    #simple visualiser
    visualiser.draw_trajectories()
