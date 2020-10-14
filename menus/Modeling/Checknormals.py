import bpy
from cgl.plugins.blender import lumbermill as lm

class Checknormals(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.checknormals'
    bl_label = 'Checknormals'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

import bpy

def applyModifierToMultiUser(scene):
    active = scene.objects.active
    if (active == None):
        print("Select an object")
        return
    if (active.type != "MESH"):
        print("Select an mesh object")
        return
    mesh = active.to_mesh(scene, True, 'PREVIEW')
    linked = []
    selected = []
    for obj in bpy.data.objects:
        if obj.data == active.data:
                linked.append(obj)
    for obj in bpy.context.selected_editable_objects:
        selected.append(obj)
        obj.select = False

    for obj in linked:
        obj.select = True
        obj.modifiers.clear()
    active.data = mesh
    bpy.ops.object.make_links_data(type='OBDATA')

    for obj in linked:
        obj.select = False
    for obj in selected:
        obj.select = True


def check_normals(selection = None):

    try:

        for obj in bpy.context.selected_objects:
            obj.data.use_auto_smooth = True
            mod = obj.modifiers.new("weighted_normal", 'WEIGHTED_NORMAL')
            scn = bpy.context.scene
            applyModifierToMultiUser(scn)
    except(AttributeError):
        pass
def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    check_normals()
    print('Hello World!: button_template')

