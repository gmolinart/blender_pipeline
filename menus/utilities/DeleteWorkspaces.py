import bpy
# from cgl.plugins.blender import lumbermill as lm

class DeleteWorkspaces(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.delete_workspaces'
    bl_label = 'Delete Workspaces'

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

    for ws in bpy.data.workspaces:
        if ws != bpy.context.workspace:
            bpy.data.batch_remove(ids=(ws,))
