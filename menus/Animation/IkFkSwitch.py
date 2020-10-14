import bpy
# from cgl.plugins.blender import lumbermill as lm

class IkFkSwitch(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.ik_fk_switch'
    bl_label = 'Ik Fk Switch'

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

    pose_bone = bpy.context.active_pose_bone
    name = pose_bone.name.split('.')

    leg_names = ['thigh', 'foot', 'leg']

    if any(item in name[0] for item in leg_names):
        if name[1] == 'r':

            bpy.ops.pose.arp_leg_switch_snap(side=".r")

        else:
            bpy.ops.pose.arp_leg_switch_snap(side=".l")


    else:
        if name[1] == 'r':
            bpy.ops.pose.arp_arm_switch_snap(side=".r")

        else:
            bpy.ops.pose.arp_arm_switch_snap(side=".l")

