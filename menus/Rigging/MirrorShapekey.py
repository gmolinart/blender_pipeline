import bpy
# from cgl.plugins.blender import lumbermill as lm

class MirrorShapekey(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.mirror_shapekey'
    bl_label = 'MirrorShapekey'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():

    name = bpy.context.object.active_shape_key.name

    if '.r' in name:
        name = name.replace('.r', '.l')

    elif '.l' in name:
        name = name.replace('.l', '.r')

    mirror_shape = bpy.context.object.shape_key_add(name=name)
    mirror_index = bpy.context.object.data.shape_keys.key_blocks.keys().index(name)

    bpy.context.object.active_shape_key_index = mirror_index
    bpy.ops.object.shape_key_mirror(use_topology=True)