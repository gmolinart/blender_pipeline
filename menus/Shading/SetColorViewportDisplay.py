import bpy
from cgl.plugins.blender.tasks.shd import set_preview_color

class SetColorViewportDisplay(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.setcolorviewportdisplay'
    bl_label = 'SetColorViewportDisplay'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
	set_preview_color()
