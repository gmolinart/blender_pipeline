import bpy
# from cgl.plugins.blender import alchemy as alc

class SwitchRigResolution(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_rig_resolution'
    bl_label = 'Switch Rig Resolution'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        switch_resolution()
        return {'FINISHED'}

def switch_resolution():
    from cgl.plugins.blender.tasks import anim
    from cgl.plugins.blender.utils import get_selection, switch_item_on_library

    print(1)
    print('selection', get_selection())
    for i in anim.get_rigs_in_scene():
        library = i.instance_collection.library
        if not get_selection()[0] == i:
            print(i)
            switch_item_on_library(i, 'resolution', 'low')
        else:
            switch_item_on_library(i, 'resolution', 'high')

