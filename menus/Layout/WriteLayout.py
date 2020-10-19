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

    utils.write_layout(outfile.copy(context='render').path_root)
    utils.write_layout(outfile.copy(context='source').path_root)

    print('___________Layout Export___________')
    print(outfile.path_root)