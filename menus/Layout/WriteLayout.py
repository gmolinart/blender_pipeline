import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
import os



class WriteLayout(bpy.types.Operator):
    """
    Writes out the current scene to a json file
    """
    bl_idname = 'object.write_layout'
    bl_label = 'Write Layout'


    def execute(self, context):
        run()
        return {'FINISHED'}


def write_layout(outFile=None):
    """

    :param outFile:
    :return:
    """
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject
    from cgl.core.utils.read_write import save_json
    import bpy
    from pathlib import Path

    if outFile == None:
        outFile = scene_object().copy(ext='json', task='lay', user='publish').path_root
    data = {}

    for obj in bpy.context.view_layer.objects:
        if obj.is_instancer:
            print(5 * '_' + obj.name + 5 * '_')
            name = obj.name
            #            blender_transform = np.array(obj.matrix_world).tolist()
            blender_transform = [obj.matrix_world.to_translation().x,
                                 obj.matrix_world.to_translation().y,
                                 obj.matrix_world.to_translation().z,
                                 obj.matrix_world.to_euler().x,
                                 obj.matrix_world.to_euler().y,
                                 obj.matrix_world.to_euler().z,
                                 obj.matrix_world.to_scale().x,
                                 obj.matrix_world.to_scale().y,
                                 obj.matrix_world.to_scale().z]

            instanced_collection = obj.instance_collection
            if instanced_collection:
                collection_library = return_linked_library(instanced_collection.name)

                if collection_library:

                    libraryPath = bpy.path.abspath(collection_library.filepath)
                    filename = Path(bpy.path.abspath(libraryPath)).__str__()
                    libObject = LumberObject(filename)

                    data[name] = {'name': libObject.asset,
                                  'source_path': libObject.path,
                                  'blender_transform': blender_transform}
                else:
                    print('{} has no instanced collection'.format(obj.name))

            else:
                print('{} has no instanced collection'.format(obj.name))

    save_json(outFile, data)

    return (outFile)


def return_linked_library(collection):
    '''
    A desperate attempt to get the stupid linked libraries manually
    '''

    libraries = bpy.data.libraries
    collection_name = collection.split('.')[0]

    for i in libraries:
        if collection in i.name:
            return (i)


def run():
    """
    Writes out the current scene to a json file
    :return:
    """
    current_scene = lm.scene_object().copy(context='render')
    folder = current_scene.copy(filename='')

    outfile = current_scene = lm.scene_object().copy(context='render',
                                                     ext='json',
                                                     set_proper_filename=True)

    if not os.path.isdir(current_scene.copy(filename='').path_root):
        os.makedirs(folder.path_root)

    write_layout(outfile.copy(context='render').path_root)
    write_layout(outfile.copy(context='source').path_root)

    print('___________Layout Export___________')
    print(outfile.path_root)
