import bpy
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils
from cgl.core.utils.read_write import save_json
import os
import json

class SaveMaterials(bpy.types.Operator):
    """
    Saves materials of selected object into the shader directory for the current asset
    """
    bl_idname = 'object.save_materials'
    bl_label = 'Save Materials'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

def run():

    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    path_object = utils.create_task_on_asset('shd')
    jsonFile = path_object.copy(ext='json')
    outFile = path_object.copy(ext='json').path_root
    print(path_object.path_root)
    save_json(outFile, data=utils.get_materials_dictionary())
    lm.save_file_as(path_object.copy(set_proper_filename=True).path_root)
    bpy.ops.object.build()
    lm.save_file()
    lm.confirm_prompt(message='Shaders Exported !!')


if __name__ == "__main__":
    run()