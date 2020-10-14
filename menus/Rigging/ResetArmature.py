import bpy
from cgl.plugins.blender import lumbermill as lm

class ResetArmature(bpy.types.Operator):
    """
    Resets all bones and ik defaults
    """
    bl_idname = 'object.reset_armature'
    bl_label = 'Reset Armature'
    armature = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run(self.armature)
        return {'FINISHED'}


def reset_bones(armature=''):

    import bpy
    from mathutils import Vector, Quaternion
    from mathutils import Matrix
    ik_switches = ["c_foot_ik.l", "c_foot_ik.r", "c_hand_ik.r", "c_hand_ik.l"]

    if armature == '':
        assetName = lm.scene_object().shot
        rigname = '{}_rig'.format(assetName)
        rig = bpy.data.objects[rigname]
        armature = rig.pose.bones
    else:

        armature_name = '{}_rig'.format(armature)
        armature = bpy.data.objects[armature_name].pose.bones

    for pb in armature:
        try:
            pb.matrix_basis = Matrix()  # == Matrix.Identity(4)

        except(AttributeError):
            pass

        if pb.name in ik_switches:

            if 'hand' in pb.name:
                pb["ik_fk_switch"] = 1

            elif 'foot' in pb.name:
                pb["ik_fk_switch"] = 0


def run(armature =''):
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    reset_bones(armature)
    print('resets all bones and ik defaults')

