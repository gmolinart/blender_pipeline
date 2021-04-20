import bpy
from cgl.plugins.blender import alchemy as alc


class ParentMeshToRig(bpy.types.Operator):
    """
    takes in group of mesh and adds it ot the rig .
    """
    bl_idname = 'alchemy.parent_mesh_to_rig'
    bl_label = 'Parent Mesh To Rig'
    assetName = bpy.props.StringProperty()

    def execute(self, context):
        run()
        return {'FINISHED'}




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    from cgl.plugins.blender.tasks.rig import parent_mdl_to_rig
    parent_mdl_to_rig()

