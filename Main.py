import json, os, argparse


input_path = 'JSONS'
output_path = "Output"


parser = argparse.ArgumentParser(description = 'Takes keypoint JSONs and moves headpoints to position (0, 0) '
                                              'and keeps relative distances.')

parser.add_argument('--input', type = str,  help = 'input folder location')
parser.add_argument('--output', type = str, help = 'output folder location')

args = parser.parse_args()

if args.input != None:
    input_path = args.input

if args.output != None:
    output_path = args.output

input_files = [pos_json for pos_json in os.listdir(input_path) if pos_json.endswith('.json')]


class Heads:
    def __init__(self, x, y):
        self.x = x
        self.y = y


head_list = []         #First index is the frame number, second is the person number
json_list = []         #Index is frame number
new_json = []          #Index is frame number


# finds all the heads and puts them into headList
def head_maker():
    for i, j in enumerate(input_files):
        with open(os.path.join(input_path, j)) as json_file:
            json_list.append(json.load(json_file))
            heads_for_frame = []
            for j in range(0, len(json_list[i]['people'])):
                heads_for_frame.append(Heads(json_list[i]['people'][j]['pose_keypoints_2d'][0],
                                             json_list[i]['people'][j]['pose_keypoints_2d'][1]))
            head_list.append(heads_for_frame)

def aligner():
    for index in range(0, len(json_list)):
        for j in range(0, len(json_list[index]['people'])):

            for k in range(2, len(json_list[index]['people'][j]['pose_keypoints_2d'])):
                if (k % 3) == 0:
                    json_list[index]['people'][j]['pose_keypoints_2d'][k] -= head_list[index][j].x
                elif (k % 3) == 1:
                    json_list[index]['people'][j]['pose_keypoints_2d'][k] -= head_list[index][j].y
            json_list[index]['people'][j]['pose_keypoints_2d'][0] = 0
            json_list[index]['people'][j]['pose_keypoints_2d'][1] = 0


def json_writer():
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for i in range(0, len(json_list)):
        fileName = output_path + "\output_" + str(i).zfill(12) + ".json"
        with open(fileName, 'w') as output_file:
            json.dump(json_list[i], output_file)




head_maker()

#for i in range(0, len(json_list)):
   # print(json_list[i])


aligner()

#for i in range(0, len(json_list)):
   # print(json_list[i])

json_writer()