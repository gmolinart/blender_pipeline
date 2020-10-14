from cgl.plugins.blender import lumbermill as lm
import bpy

class WriteMeshList(bpy.types.Operator):
    """
    writes out json file with all the objs mesh and locations
    """
    bl_idname = 'object.write_mesh_list'
    bl_label = 'Write Mesh List'

    def execute(self, context):
        run()
        return {'FINISHED'}


def create_render_folder(scene):
    import os
    render_folder = scene.copy(context='render', filename='').path_root

    if not os.path.isdir(render_folder):
        os.makedirs(render_folder)

    print('______________________RENDER CREATED_______________')

def set_matrix(obj):
    blender_transform = [obj.matrix_world.to_translation().x,
                         obj.matrix_world.to_translation().y,
                         obj.matrix_world.to_translation().z,
                         obj.matrix_world.to_euler().x,
                         obj.matrix_world.to_euler().y,
                         obj.matrix_world.to_euler().z,
                         obj.matrix_world.to_scale().x,
                         obj.matrix_world.to_scale().y,
                         obj.matrix_world.to_scale().z]
    return blender_transform

def write_mesh_list(outFile=None):
    """

    :param outFile:
    :return:
    """
    from cgl.plugins.blender.lumbermill import scene_object
    from cgl.core.utils.read_write import save_json
    import bpy

    scene = lm.scene_object()

    if outFile == None:
        outFile = scene_object().copy(ext='json', context='render').path_root
    data = {}

    for obj in bpy.data.collections[scene.asset].objects:
        name = obj.name
        print(obj.name)
        #            blender_transform = np.array(obj.matrix_world).tolist()
        blender_transform = set_matrix(obj)
        data[name] = {'name': obj.name,
                      'blender_transform': blender_transform}

    create_render_folder(scene)
    save_json(outFile, data)

    return (outFile)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    write_mesh_list()
