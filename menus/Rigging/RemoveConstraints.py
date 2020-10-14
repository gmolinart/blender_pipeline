import bpy
# from cgl.plugins.blender import lumbermill as lm

class RemoveConstraints(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.remove_constraints'
    bl_label = 'RemoveConstraints'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


import bpy


def remove_constraint():
    objects = bpy.context.selected_pose_bones_from_active_object
    for obj in objects:
        for constraint in obj.constraints:
            obj.constraints.remove(constraint)



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    remove_constraint()
    print('Hello World!: button_template')

