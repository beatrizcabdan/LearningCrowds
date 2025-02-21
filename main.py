def write_init(input_file, recording_start, simulation_length=100):
    f = open("crowd_initialisation/" + input_file, "w")

    # CREATE WORLD
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n")
    f.write("<Simulation delta_time=\"0.1\" end_time=\"" + str(simulation_length + recording_start) + "\">" + "\n")
    f.write("\t<World type=\"Infinite\" />\n")

    # CREATE AGENTS
    f.write("\t<Agents>\n")
    # self.two_flows(f, self._num_agents, degrees=degrees, noise_amplitude=0.005)
    f.write("\t</Agents>\n")

    # WRITE POLICIES
    f.write("\t<Policies>\n\t\t<Policy id=\"0\" OptimizationMethod=\"gradient\" RelaxationTime=\"0.5\">\n\t\t\t<costfunction range=\"5\" name=\"SocialForcesAvoidance\" />\n\t\t\t<costfunction name=\"GoalReachingForce\" />\n\t\t</Policy>\n\t</Policies>\n")
    f.write("</Simulation>\n")
    f.close()

write_init("test1.xml", 10, 20)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    umans_path = "../../Projects/UMANS-master/build/UMANS-ConsoleApplication-Linux"
    write_init("test1.xml", 10, 20)
