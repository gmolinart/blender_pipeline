import bpy
from cgl.plugins.blender import lumbermill as lm

class GreasePencilSwitch(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.grease_pencil_switch'
    bl_label = 'Grease Pencil Switch'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

def deselect():
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

def run():

    object = bpy.context.active_object

    if object.type == 'ARMATURE':
        poseBone = bpy.context.selected_pose_bones_from_active_object[0]
        gpname = '{}_{}_GP'.format(object.name, poseBone.name)

        print(gpname)

        if gpname in bpy.data.objects:
            gp_object = bpy.data.objects[gpname]
            deselect()
            bpy.ops.object.mode_set(mode='OBJECT')

            gp_object.select_set(True)
            bpy.context.view_layer.objects.active = gp_object
            bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

        else:
            bpy.ops.object.create_grease_pencil()

        bpy.ops.id.skin_selection()
        bpy.context.space_data.overlay.show_bones = False




    elif object.type == 'GPENCIL':
        deselect()
        bpy.ops.object.mode_set(mode='OBJECT')
        if 'proxy' in object.name:
            rigname = object.name.split('_proxy')[0] + '_proxy'
        else:
            rigname = object.name.split('_rig')[0] + '_rig'

        bpy.data.objects[rigname].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[rigname]
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.id.skin_selection()
