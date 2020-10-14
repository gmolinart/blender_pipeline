import bpy
from cgl.plugins.blender import lumbermill as lm
import os


class PublishLow(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.publish_low'
    bl_label = 'Publish Low'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def convert_low_to_main_collection(assetName=''):
    if assetName == '':
        assetName = lm.scene_object().shot

    for collection in bpy.data.collections:
        if collection.name == assetName:
            collection.name = '{}_high'.format(assetName)

        elif collection.name == '{}_low'.format(assetName):
            collection.name = assetName

        elif lm.scene_object().resolution == 'low':
             lm.confirm_prompt(message='ALERT: you are currently in the low version nothing to do here')

        elif lm.scene_object().resolution == 'high':
            lm.confirm_prompt(title='ERROR',
                              message='ERROR: no low collection found, please create {}_low collection'.format(
                                  assetName))



def save_low():
    low_path_object = lm.scene_object().copy(resolution='low')
    low_dir = low_path_object.copy(filename='').path_root
    if not os.path.isdir(low_dir):
        os.makedirs(low_dir)
    lm.save_file_as(low_path_object.path_root)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    convert_low_to_main_collection()
    save_low()
    bpy.ops.object.cleanup_scene()
    bpy.ops.object.build()
