import bpy
from cgl.plugins.blender import lumbermill as lm

class RenameCameras(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.rename_cameras'
    bl_label = 'Rename Cameras'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def rename_cameras():
    selected_cam = bpy.context.selected_objects
    currentScene = lm.scene_object()
    shotIncrement = 10
    for camera in selected_cam:
        if camera.type == 'CAMERA':
            camName  = '%s_%04d_cam' % (currentScene.seq, shotIncrement)
            camera.name = camName
            camera.data.name =  camName
            shotIncrement += 10


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    rename_cameras()

