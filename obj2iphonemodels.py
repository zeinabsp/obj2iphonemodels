## This a python script to convert a wavefront .obj file to .h and .c files to be used in iOs applications.
#
## author: Zeinab Sadeghipour

import sys

# read info about vertex positions and normals and faces from the .obj file
# we only convert faces info into int, since the other info will be written to another file directly
def readObjFile(obj_filename):

    obj_file = open(obj_filename, 'r')
    model_info = obj_file.read().split('\n')

    vertices = []
    faces = []
    vertices_n = []

    for line in model_info:
        line_segs = line.split()
        if len(line_segs) > 0:
            #vertex
            if line_segs[0] == 'v':
                vertices.append(line_segs[1:])
            #vertex normal
            if line_segs[0] == 'vn':
                vertices_n.append(line_segs[1:])

            # face
            if line_segs[0] == 'f':
                f = []

                if line_segs[1].find('//') == -1:
                    f.append(int(line_segs[1]))
                    f.append(int(line_segs[2]))
                    f.append(int(line_segs[3]))
                else:
                    for seg in line_segs[1:]:
                        segs = seg.split('//')
                        f.append(int(segs[0]))

                faces.append(f)

    print len(vertices), len(vertices_n), len(faces)
    return vertices, vertices_n, faces

# write mesh info into .c and .h files in the required format
def writeIphoneModels(c_filename, h_filename, model_name, v, vn, f):

    #header file
    h_file = open(h_filename, 'w')
    h_file.write('// This is a .h file for the model: ' + model_name + '\n\n')
    h_file.write('// Positions: ' + str(len(v)) + '\n')
    h_file.write('// Normals: ' + str(len(vn)) + '\n')
    h_file.write('// Faces: ' + str(len(f)) + '\n')
    h_file.write('// Vertices: ' + str(len(f) * 3) + '\n\n')

    h_file.write('extern const int ' + model_name + 'Vertices;\n')
    h_file.write('extern const float ' + model_name + 'Positions[' + str(len(f) * 9) + '];\n');
    h_file.write('extern const float ' + model_name + 'Normals[' + str(len(f) * 9) + '];\n');

    h_file.close()

    # c file
    c_file = open(c_filename, 'w')
    c_file.write('// This is a .c file for the model: ' + model_name + '\n\n')
    c_file.write('#include "' + model_name + '.h"\n\n')
    c_file.write('const int ' + model_name + 'Vertices = ' + str(len(f) * 3) + ';\n\n')

    c_file.close()

if __name__ == '__main__':

    # model_name = 'adam_opt_lite'
    model_name = 'general_derm'

    obj_filename = 'obj/' + model_name + '.obj'
    c_filename = 'iphonemodels/' + model_name + '.c'
    h_filename = 'iphonemodels/' + model_name + '.h'

    v, vn, f = readObjFile(obj_filename=obj_filename)

    writeIphoneModels(c_filename, h_filename, model_name, v, vn, f)
