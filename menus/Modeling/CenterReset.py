import bpy
# from cgl.plugins.blender import lumbermill as lm

class CenterReset(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.center_reset'
    bl_label = 'Center Reset'

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
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    obj = bpy.context.object
    loc = bpy.data.objects.new('parent', None)
    bpy.context.collection.objects.link(loc)
    loc.location = obj.location
    loc.location[2] = 0

    for obj in bpy.context.selected_objects:
        obj.select_set(True)

    loc.select_set(True)  # select the object for the 'parenting'

    bpy.context.view_layer.objects.active = loc  # the active object will be the parent of all selected object

    bpy.ops.object.parent_set(keep_transform=True)

    loc.matrix_world.identity()
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.context.collection.objects.unlink(loc)

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
