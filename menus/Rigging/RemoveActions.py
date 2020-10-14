import bpy
# from cgl.plugins.blender import lumbermill as lm

class RemoveActions(bpy.types.Operator):
    """
    Removes all actions in scene
    """
    bl_idname = 'object.remove_actions'
    bl_label = 'Remove Actions'

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
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

    print('Actions Removed')

