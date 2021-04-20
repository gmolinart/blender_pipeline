import bpy
# from cgl.plugins.blender import alchemy as alc

class ExportFile(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.export_file'
    bl_label = 'Export File'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():

    print(alc.scene_object().copy(variant = bpy.types.Scene.inputDialogText ).path_root)


