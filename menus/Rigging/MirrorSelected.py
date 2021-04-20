import bpy
# from cgl.plugins.blender import alchemy as alc

class MirrorSelected(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'alchemy.mirror_selected'
    bl_label = 'Mirror Selected'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def custom_mirror():
    import bpy
    from cgl.plugins.blender.utils import selection, get_object

    vertex_group = bpy.context.active_object.vertex_groups
    vertex_group_selected = bpy.context.object.vertex_groups.active
    print(vertex_group)

    object = bpy.context.object
    new_object = get_object('{}_mirror'.format(object.name))

    if new_object:
        bpy.data.objects.remove(new_object)
    print(object)
    new_object = object.copy()
    new_object.data = object.data.copy()
    new_object.name = '{}_mirror'.format(object.name)
    bpy.context.collection.objects.link(new_object)
    new_object.scale = (-1.0, 1.0, 1.0)

    for vertex_group in new_object.vertex_groups:
        if not vertex_group.name == vertex_group_selected.name:
            new_object.vertex_groups.remove(vertex_group)

    for vertex_group in new_object.vertex_groups:
        if '.l' in vertex_group.name:
            vertex_group.name = vertex_group.name.replace('.l', '.r')
        elif '.r' in vertex_group.name:
            vertex_group.name = vertex_group.name.replace('.r', '.l')

    selection(new_object, clear=True)
    selection(object)
    bpy.ops.object.copy_skin_weights()
    bpy.data.objects.remove(new_object)



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    custom_mirror()


