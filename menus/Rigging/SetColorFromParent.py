import bpy
# from cgl.plugins.blender import lumbermill as lm

class SetColorFromParent(bpy.types.Operator):
    """
    Inherits controller color from parent
    """
    bl_idname = 'object.set_color_from_parent'
    bl_label = 'Set Color From Parent'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def set_bone_index_to_parent():
    bones = bpy.context.selected_pose_bones_from_active_object
    rig = bpy.context.object

    for bone in bones:
        parent = rig.data.bones[bone.name].parent
        print(parent.name)
        bone.bone_group_index = rig.pose.bones[parent.name].bone_group_index



def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    set_bone_index_to_parent()

