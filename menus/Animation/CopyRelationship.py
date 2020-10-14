import bpy
from mathutils import Matrix
from os.path import isfile
from cgl.core.utils.read_write import save_json, load_json


class CopyRelationship(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.copy_relationship'
    bl_label = 'Copy Relationship'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def flatten(mat):
    dim = len(mat)
    return [mat[j][i] for i in range(dim)
            for j in range(dim)]


def unflatten(c):
    matrix = Matrix((([c[0], c[4], c[8], c[12]],
                      [c[1], c[5], c[9], c[13]],
                      [c[2], c[6], c[10], c[14]],
                      [c[3], c[7], c[11], c[15]]
                      )))

    return matrix


def get_selection_order(obj_a, obj_b, bones=False):
    objects = []

    if obj_a == None:
        if bones:
            obj_a = bpy.context.active_pose_bone

        else:
            obj_a = bpy.context.active_object

        objects.append(obj_a)

    if obj_b is None:
        if bones:
            for object in bpy.context.selected_objects:

                for bone in object.pose.bones:
                    if bone.bone.select and bone != obj_a:
                        print(bone)
                        obj_b = bone
            # selection = bpy.context.selected_pose_bones_from_active_object

        else:
            selection = bpy.context.selected_objects

            for i in selection:
                if i != obj_a:
                    obj_b = i

        objects.append(obj_b)

    print('_________{} and {} selected____________'.format(
        objects[0].name, objects[1].name))
    return objects


def save_relationship(filepath, obj_a=None, obj_b=None, bones=False):
    if bones is False:
        obj_a, obj_b = get_selection_order(obj_a, obj_b, bones)
        obj_a_mat = obj_a.matrix
        obj_b_mat = obj_b.matrix

    else:
        obj_a, obj_b = get_selection_order(obj_a, obj_b, bones)
        obj_a_mat = obj_a.matrix
        obj_b_mat = obj_b.matrix
        obj_a_mat_world = obj_a.matrix
        obj_b_mat_world = obj_b.matrix
        difference_local = obj_b_mat_world.inverted() @ obj_a_mat_world

    difference = obj_b_mat.inverted() @ obj_a_mat

    if bones:
        print('difference world')
        print(obj_a_mat_world)
        print(obj_b_mat_world)
        difference = obj_a_mat_world.inverted() @ obj_b_mat_world

    print('difference')
    print(difference)

    data = {}
    data.update({'{} {}'.format(obj_a.name, obj_b.name): flatten(difference)})
    data.update({'{} {}'.format(obj_b.name, obj_a.name)
                 : flatten(difference.inverted())})

    updated_json = data
    if isfile(filepath):
        print('file_ existis')
        current_json = load_json(filepath)
        print(current_json)
    else:
        current_json = {}

    if current_json:
        updated_json = {**data, **current_json}
        print('file updated')
        print(updated_json)

    save_json(filepath, updated_json)


def read_relationship(filepath, obj_a=None, obj_b=None, bones=False):
    """reads the relationship matrix from filepath

    Args:
        filepath ([type]): [description]
        obj_a ([type], optional): [description]. Defaults to None.
        obj_b ([type], optional): [description]. Defaults to None.
        bones (bool, optional): [description]. Defaults to False.
    """
    obj_a, obj_b = get_selection_order(obj_a, obj_b, bones)

    print(obj_a, obj_b)

    if bones is False:

        obj_a_mat = obj_a.matrix_world
        obj_b_mat = obj_b.matrix_world

    else:

        obj_a_mat = obj_a.bone.matrix_local
        obj_obj_b_mat = obj_b.bone.matrix_local

    identity = Matrix(
        (([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])))
    matrix = load_json(filepath)
    current = '{} {}'.format(obj_a.name, obj_b.name)

    c = matrix[current]

    difference = unflatten(matrix[current])

    if bones is False:

        obj_a.matrix_world = obj_b.matrix_world @ difference
        print(obj_b.matrix_world)

    else:

        new_matrix = obj_a.matrix @ difference

    print(obj_a.name, obj_b.name)
    print('DIFFERENCE')
    print(difference)

    print(obj_a.name)
    print(obj_a.matrix)

    print(obj_b.name)
    print(obj_b.matrix)

    print('NEW MATRIX')
    print(new_matrix)

    obj_b.matrix = new_matrix


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    filepath = bpy.data.filepath.replace('.blend', '.json')
    save_relationship(filepath, bones=True)


if __name__ ==  '__main__':
    run()
    # filepath = bpy.data.filepath.replace('.blend', '.json')
    # read_relationship(filepath , bones = True)