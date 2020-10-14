import bpy
# from cgl.plugins.blender import lumbermill as lm

class ReplaceBeshMesh(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.replace_besh_mesh'
    bl_label = 'Replace Besh Mesh'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

import bpy



def get_selection_order():
    objects = []

    obj_a = bpy.context.active_object
    objects.append(obj_a)

    selection = bpy.context.selected_objects

    for i in selection:
        if i != obj_a:
            obj_b = i

    objects.append(obj_b)

    print('_________{} and {} selected____________'.format(
        objects[0].name, objects[1].name))
    return objects




def keep_single_user_collection(obj, assetName=None):
    if not assetName:
        assetName = lm.scene_object().shot

    try:
        bpy.data.collections[assetName].objects.link(obj)

    except(RuntimeError):
        pass

    for collection in obj.users_collection:
        if collection.name != assetName:
            collection.objects.unlink(obj)






def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    basemesh, target = get_selection_order()

    basemesh.name = target.name
    bpy.ops.object.join_shapes()
    bpy.data.shape_keys['Key'].key_blocks[1].value = 1


