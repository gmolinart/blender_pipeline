import bpy
# from cgl.plugins.blender import lumbermill as lm

class ImportRig(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_rig'
    bl_label = 'Import Rig'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


import bpy


def import_selected_rig():
    rig = bpy.context.object
    if 'proxy' in rig.name:

        object_name = rig.name.replace('_proxy', '')
    elif 'rig' in rig.name:
        object_name = rig.name.replace('_rig', '')
    object = bpy.data.objects[object_name]

    action = rig.animation_data
    if not action:
        print('NO ANIMATION')
        object.animation_data_create()

        return

    else:
        action = rig.animation_data.action.name

    rig.select_set(False)
    object.select_set(True)

    bpy.ops.object.duplicates_make_real()

    imported_rig_name = '{}_rig'.format(object_name)

    return (imported_rig_name, action)


def link_animation(object, action):
    imported_rig = bpy.data.objects[object]
    action = bpy.data.actions[action]
    imported_rig.animation_data_create()
    imported_rig.animation_data.action = action


def run():

    object, action = import_selected_rig()
    print(object, action)
    link_animation(object, action)

    link_animation(object, action)

    # link_animation('MILVIO_rig', 'MILVIO_proxyAction')