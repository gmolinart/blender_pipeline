import bpy
# from cgl.plugins.blender import lumbermill as lm

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


    master = bpy.context.object.pose.bones["c_root_master.x"]['proxy']

    if "c_root_master.x" in bpy.context.object.pose.bones:

        if master == 0.0:
            bpy.context.object.pose.bones["c_root_master.x"]['proxy'] = 1.0
            print('Turning on')
        else:
            bpy.context.object.pose.bones["c_root_master.x"]['proxy'] = 0
            print('Turning off')


    bpy.context.object.update_tag()