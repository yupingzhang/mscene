# parse the .mot data for single frame 
# write to xml
# <shape type="obj">
# <string name="filename" value="obs_00.obj"/>
# <transform name="toWorld"> 
# 	<rotate angle="0.000000" x="1.000000" y="1.000000" z="1.000000"/>
# 	<scale value="1.00000"/>
# 	<translate x="-0.500000" y="-1.400000" z="-0.959360"/>
# </transform>
# </shape>	

import os, sys, math

def loader(filename):
    vertices = []
    faces = []
    with open(filename) as f:
        for line in f:
            s = line.strip().split(' ')
            if s[0] == 'v':
                vertices.append(map(float, s[1:]))
            elif s[0] == 'f':
                faces.append(line)   # save string
    return vertices, faces


def mot_loader(filename, frame_num, total_frames):
	body = [] # 16
	quaternion = []  # 4
	tran = [] # 3
	# NumFrames: 716
	# body[0] position / rotation
	with open(filename) as f:
		# skip the first line
		lines = [line for line in f]
		lines.pop(0);
		# slice the rest into chuncks
		chuncks = [lines[x:x+total_frames + 2] for x in range(0, len(lines), total_frames + 2)]  # body title + blank line
		for chunck in chuncks:
			line = chunck[0]
			s = line.strip().split(' ')
			if s[0].find("NumFrames") != -1:
				if total_frames != map(float, s[1]):
					print "Inconsistant total frames in " + filename
					break
			if s[0].find("body") != -1:
				if s[1].find("position") != -1:
					tranlation = chunck[frame_num].strip().split(' ')
					tran = map(float, tranlation)
				elif s[1].find("orientation") != -1:
					quaternion = chunck[frame_num].strip().split(' ')
					# quaternion to axis angle
					qw = float(quaternion[0])
					qx = float(quaternion[1])
					qy = float(quaternion[2])
					qz = float(quaternion[3])
					angle = math.degrees(2 * math.acos(qw))
					x = qx / math.sqrt(1-qw*qw)
					y = qy / math.sqrt(1-qw*qw)
					z = qz / math.sqrt(1-qw*qw)
					tran.extend([angle, x, y, z])
			if len(tran) == 7:
				body.append(tran)
	return body


def write_to_xml(body):
	str = ""
	for i in range(0, len(body)):
		str += "<shape type=\"obj\"> \n"
		str += "<string name=\"filename\" value=\"female-objs/body" + "{:0>4}".format(i) + ".obj\"/> \n"
		str += "<transform name=\"toWorld\"> \n"
		str += "	<rotate angle=\"%f\" x=\"%f\" y=\"%f\" z=\"%f\"/> \n" % (body[i][3], body[i][4], body[i][5], body[i][6])
		str += "	<translate x=\"%f\" y=\"%f\" z=\"%f\"/> \n" % (body[i][0], body[i][1], body[i][2])
		str += "	<scale value=\"1.00000\"/> \n"
		str += "</transform> \n"
		str += "<bsdf type=\"diffuse\">\n"
		str += "	<rgb name=\"diffuseReflectance\" value=\"0.25, 0.95, 0.95\"/>\n"
		str += "</bsdf>\n"
		str += "</shape>\n"
	print str

def main():
	body = mot_loader("dance-paused.mot", 1, 716)
	write_to_xml(body)


if __name__ == '__main__':
	main()