import bpy
# from cgl.plugins.blender import lumbermill as lm

class MirrorVertexGroups(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.mirror_vertex_groups'
    bl_label = 'Mirror Vertex Groups'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    import bpy

    obj_vertex_groups = bpy.context.object.vertex_groups
    vertex_group = obj_vertex_groups.active
    new_name = None
    bpy.ops.object.vertex_group_copy()
    new_vertex_group = bpy.context.object.vertex_groups['{}_copy'.format(vertex_group.name)]

    if '.l ' in vertex_group.name:
        new_name = vertex_group.name.replace('.l', '.r')

    else:
        new_name = vertex_group.name.replace('.r', '.l')


    if new_name:
        obj_vertex_groups.remove(obj_vertex_groups[new_name])
        new_vertex_group.name = new_name
        obj_vertex_groups.active = new_vertex_group
        bpy.ops.object.vertex_group_mirror(flip_group_names=False)

        print(new_vertex_group.name)