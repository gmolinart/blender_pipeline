import bpy
# from cgl.plugins.blender import Alchemy as lm

class ResetRigPublish(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.reset_rig_publish'
    bl_label = 'Reset Rig Publish'

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
    if (bpy.context.selected_objects[0].mode != 'POSE'):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(extend=True, type='ARMATURE')
        obj_sel = bpy.context.selected_objects[0]
        bpy.context.view_layer.objects.active = obj_sel
        obj_sel.select_set(state=True)
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode='OBJECT')

    print('Hello World!: button_template')

