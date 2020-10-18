import bpy
from cgl.plugins.blender import lumbermill as lm

class RemoveModifiers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.remove_modifiers'
    bl_label = 'RemoveModifiers'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


import bpy


def remove_modifier():
    objects = bpy.context.selected_objects
    for obj in objects:
        if 'instancer' not in obj.name:

            for mod in obj.modifiers:
                bpy.ops.object.modifier_remove(modifier=mod.name)




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    modifier_remove()
    print('Hello World!: button_template')

