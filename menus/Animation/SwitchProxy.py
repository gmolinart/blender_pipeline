import bpy
# from cgl.plugins.blender import Alchemy as lm

class SwitchProxy(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_proxy'
    bl_label = 'Switch Proxy'

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

    from cgl.plugins.blender.alchemy import scene_object
    master = scene_object().project_info['main_controller']

    if master in bpy.context.object.pose.bones:

        if bpy.context.object.pose.bones[master]['proxy'] == 0.0:
            bpy.context.object.pose.bones[master]['proxy'] = 1.0
            print('Turning on')
        else:
            bpy.context.object.pose.bones[master]['proxy'] = 0
            print('Turning off')


    bpy.context.object.update_tag()