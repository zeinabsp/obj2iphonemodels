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
    faces_n = []

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
                f_n = []

                if line_segs[1].find('//') == -1:
                    f.append(int(line_segs[1]))
                    f.append(int(line_segs[2]))
                    f.append(int(line_segs[3]))
                    f_n = f
                else:
                    for seg in line_segs[1:]:
                        segs = seg.split('//')
                        f.append(int(segs[0]))
                        f_n.append(int(segs[1]))

                faces.append(f)
                faces_n.append(f_n)

    print len(vertices), len(vertices_n), len(faces), len(faces_n)
    return vertices, vertices_n, faces, faces_n

# write mesh info into .c and .h files in the required format
def writeIphoneModels(c_filename, h_filename, model_name, v, vn, f, fn):

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

    #writing face vertices positions in order
    c_file.write('const float ' + model_name + 'Positions[' + str(len(f) * 9) + '] = \n{\n')
    for face in f:
        for face_v in face:
            vertex = v[face_v - 1]
            c_file.write(vertex[0] + ', ' + vertex[1] + ', ' + vertex[2] + ',\n')
    c_file.write('};\n\n')

    #writing face vertices normals in order
    c_file.write('const float ' + model_name + 'Normals[' + str(len(fn) * 9) + '] = \n{\n')
    for face_n in fn:
        for face_vn in face_n:
            vertex_norm = vn[face_vn - 1]
            c_file.write(vertex_norm[0] + ', ' + vertex_norm[1] + ', ' + vertex_norm[2] + ',\n')
    c_file.write('};\n')

    c_file.close()


if __name__ == '__main__':

    # model_name = 'adam_opt_lite_norm'
    model_name = 'general_derm'
    # model_name = 'unicube'
    # model_name = 'tricho'

    obj_filename = 'obj/' + model_name + '.obj'
    c_filename = 'iphonemodels/' + model_name + '.c'
    h_filename = 'iphonemodels/' + model_name + '.h'

    v, vn, f, fn = readObjFile(obj_filename=obj_filename)

    writeIphoneModels(c_filename, h_filename, model_name, v, vn, f, fn)
