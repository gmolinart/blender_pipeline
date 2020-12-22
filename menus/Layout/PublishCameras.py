import bpy
import math
from cgl.plugins.blender import lumbermill as lm


class PublishCameras(bpy.types.Operator):
    """
    Publishes Cameras from aster Layout files .
    """
    bl_idname = 'object.publish_cameras'
    bl_label = 'Publish Cameras'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def run():
    from cgl.plugins.blender.tasks import cam

    camera = cam.get_selected_camera()
    cam.publish_selected_camera(camera,fbx=True)


if __name__ == "__main__":
    run()