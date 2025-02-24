import random
import math
import os
import visualiser

import csv


def convert_umans_to_chaos(folder, output_folder):
    trajectory_files = os.listdir(folder)
    for input_file in trajectory_files:
        with open(folder+input_file, mode='r', newline='', encoding='utf-8') as fin:
            with open(output_folder+input_file, mode='w', newline='', encoding='utf-8') as fout:
                reader = csv.reader(fin)
                writer = csv.writer(fout)
                for row in reader:
                    writer.writerow(row[:3])

def simple_crossing(f, num_agents, road_width, distance):
    #crossing pedestrians
    for i in range(num_agents):
        x = (road_width + 0.3 * (i % 3)) * (1 if i % 2 else -1)
        y = i * 0.4
        x_init = round(x, 2)
        y_init = round(distance + y, 2)
        x_goal = round(-x, 2)
        y_goal = round(distance + y, 2)

        #write init file
        f.write("\t" * 2 + "<Agent rad=\"0.2\" pref_speed=\""+str(0.8+0.1*i%3)+"\" max_speed=\"1.3\">\n")
        f.write("\t" * 3 + "<Policy id=\"0\"/>\n")
        f.write("\t" * 3 + "<pos x=\"" + str(x_init) + "\" y=\"" + str(y_init) + "\"/>\n")
        f.write("\t" * 3 + "<goal x=\"" + str(x_goal) + "\" y=\"" + str(y_goal) + "\"/>\n")
        f.write("\t" * 2 + "</Agent>\n")

def single_flow(f, num_agents, road_width, distance, go_left=True):
    #crossing pedestrians
    for i in range(num_agents):
        x = (road_width + 0.3 * (i % 2)) * (1 if go_left else -1)
        y = i * 0.4
        x_init = round(x, 2)
        y_init = round(distance + y, 2)
        x_goal = round(-x, 2)
        y_goal = round(distance + y, 2)

        #write init file
        f.write("\t" * 2 + "<Agent rad=\"0.2\" pref_speed=\""+str(0.8+0.1*i%3)+"\" max_speed=\"1.3\">\n")
        f.write("\t" * 3 + "<Policy id=\"0\"/>\n")
        f.write("\t" * 3 + "<pos x=\"" + str(x_init) + "\" y=\"" + str(y_init) + "\"/>\n")
        f.write("\t" * 3 + "<goal x=\"" + str(x_goal) + "\" y=\"" + str(y_goal) + "\"/>\n")
        f.write("\t" * 2 + "</Agent>\n")


def write_agents(f, num_agents, distance, case=2, road_width=8):
    """
    case0,1 pedestrian or group crosses perpendicularly to road left to right or right to left
    case2 pedestrians or group of pedestrians cross each other while crossing the road
    """

    #crossing pedestrians
    if case == 0:
        single_flow(f, num_agents, road_width, distance)
    elif case == 1:
        single_flow(f, num_agents, road_width, distance, go_left=False)
    elif case == 2:
        simple_crossing(f, num_agents, road_width, distance)


def write_init_umans(input_file, num_agents=5, recording_start=10, simulation_length=100, case=1, distance_to_pedestrians=0, road_width=7):
    f = open(input_file, "w")

    # CREATE WORLD
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n")
    f.write("<Simulation delta_time=\"0.1\" end_time=\"" + str(simulation_length + recording_start) + "\">" + "\n")
    f.write("\t<World type=\"Infinite\" />\n")

    # CREATE AGENTS
    f.write("\t<Agents>\n")
    write_agents(f, num_agents, case=case, road_width=road_width, distance=distance_to_pedestrians)
    f.write("\t</Agents>\n")

    # WRITE POLICIES
    f.write("\t<Policies>\n")
    f.write("\t\t<Policy id=\"0\" OptimizationMethod=\"global\" RelaxationTime=\"0.5\">\n")
    f.write("\t\t\t<costfunction range=\"5\" name=\"ORCA\" />\n")
    f.write("\t\t</Policy>\n\t</Policies>\n")
    f.write("</Simulation>\n")
    f.close()

def write_init_chaos(input_file, recording_start, simulation_len):
    f = open(input_file, "w")

    # CREATE WORLD
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n")
    f.write("<ConfigData xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">" + "\n")
    f.write("\t<env_filesPath>./Scenarios/Test/</env_filesPath>" + "\n")
    #f.write("\t<env_obstFile>./Scenarios/Decor/obstExampleTwoColors.xml</env_obstFile>" + "\n")
    f.write("\t<env_stageInfos stageName=\"\">\n\t\t<file />\n\t\t<position x=\"0\" y=\"0\" z=\"0\" />\n\t\t<rotation x=\"0\" y=\"0\" z=\"0\" />\n\t\t</env_stageInfos>" + "\n")
    f.write("\t<cam>\n\t\t<cameraType typeID=\"0\" />" + "\n")
    f.write("\t\t<position x=\"0\" y=\"-5\" z=\"1\" />" + "\n")
    f.write("\t\t<rotation x=\"0\" y=\"0\" z=\"0\" />" + "\n")
    f.write("\t\t<lookAtAgent agentID=\"-1\" />" + "\n")
    f.write("\t\t<followAgent agentID=\"-1\" followOnX=\"false\" followOnY=\"false\" lockFirstPerson=\"false\" smoothFirstPerson=\"true\" />" + "\n")
    f.write("\t\t<CamResolution x=\"-1\" y=\"-1\" />" + "\n")
    f.write("\t</cam>" + "\n")
    f.write("\t<recording start=\""+str(recording_start)+"\" end=\""+str(recording_start+simulation_len)+"\" framerate=\"15\" width=\"720\" height=\"480\">" + "\n")
    f.write("\t\t<saveImgOriginal record=\"true\" quality=\"8\" width=\"-1\" height=\"-1\" />" + "\n")
    f.write("\t\t<saveImgSegmentation record=\"false\" quality=\"8\" width=\"-1\" height=\"-1\" />" + "\n")
    f.write("\t\t<saveImgOpticalFlow record=\"false\" quality=\"8\" width=\"-1\" height=\"-1\"  motionVector=\"false\" />" + "\n")
    f.write("\t\t<saveDir>./Output/Test/</saveDir>" + "\n")
    f.write("\t</recording>" + "\n")
    f.write("\t<AgentColorList />\n" + "\n")
    f.write("</ConfigData>")

    f.close()


if __name__ == '__main__':
    #add here the path to your build for UMANS, all info: https://project.inria.fr/crowdscience/project/ocsr/umans/
    umans_path = "../../Projects/UMANS-master/build/UMANS-ConsoleApplication-Linux"
    umans_path = "..\\..\\Projects\\UMANS-master\\build\\Debug\\UMANS-ConsoleApplication-Windows.exe"
    scenarios_path = "..\\..\\Projects\\chaos-master\\Scenarios\\"
    chaos_path = "..\\..\\Projects\\chaos-master\\ChAOS.exe"
    ffmpeg_path = "..\\..\\Projects\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"

    #crowd initialisation
    recording_start = 1
    simulation_length = 10

    for pedestrian_distance in [0,10,20]:
        for number_pedestrians in [2,9,1]:
            for case in [2,1,0]:

                # delete prev simulations
                os.system("del crowd_simulations\*.csv") #in mac i was using "rm -rf crowd_simulations/*.csv"
                os.system("del ..\\..\\Projects\\chaos-master\\Output\\Test /q /s")
                os.system("del "+scenarios_path+"\\Test\\*.csv")

                sim_id = "case"+str(case)+"_noped"+str(number_pedestrians)+"_dist"+str(pedestrian_distance)
                scenario_file = "crowd_initialisation/" + sim_id + ".xml"

                #run simulation using UMANS
                write_init_umans(scenario_file, num_agents=number_pedestrians, recording_start=recording_start, simulation_length=simulation_length, case=case, distance_to_pedestrians=pedestrian_distance, road_width=7)
                os.system(umans_path + " -i " + scenario_file + " -o crowd_simulations")
                convert_umans_to_chaos("crowd_simulations\\", scenarios_path+"Test\\")

                #simple 2D plot visualisation
                visualiser.draw_trajectories(sim_id, recording_start)

                #advanced visualisation with ChAOS
                write_init_chaos(scenarios_path+sim_id+".xml", recording_start=recording_start, simulation_len=simulation_length)
                os.system("cd ..\\..\\Projects\\chaos-master && ChAOS.exe -s Scenarios\\"+sim_id+".xml -batchmode && "+ffmpeg_path+" -i Output\\Test\\Images\\%4d.png Output\\Test\\"+sim_id+"_images.gif && "+ffmpeg_path+" -i Output\\Test\\Segmentation\\%4d.png Output\\Test\\"+sim_id+"_segmentation.gif && "+ffmpeg_path+" -i Output\\Test\\OpticalFlow\\%4d.png Output\\Test\\"+sim_id+"_opticalflow.gif") #traveling to ChAOS directory because of inner workings
                os.system("xcopy /e ..\\..\\Projects\\chaos-master\\Output\\Test\\ frames\\"+sim_id+"\\")
