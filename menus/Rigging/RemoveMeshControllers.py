import bpy
# from cgl.plugins.blender import lumbermill as lm

class RemoveMeshControllers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.remove_mesh_controllers'
    bl_label = 'Remove Mesh Controllers'

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

    obj = bpy.context.object

    vertex_groups = bpy.context.object.vertex_groups

    for group in vertex_groups:
        if 'fs:' in group.name:
            vg = obj.vertex_groups.get(group.name)
            if vg is not None:
                obj.vertex_groups.remove(vg)
                print(group.name)

        # vertex_groups.remove(group)


