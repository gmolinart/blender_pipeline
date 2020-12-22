import bpy
# from cgl.plugins.blender import lumbermill as lm

class CorrectiveBlendShapes(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.corrective_blend_shapes'
    bl_label = 'CorrectiveBlendShapes'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}
def create_drive():
    import bpy
    selection = bpy.context.selected_objects

    # rigname = '{}_rig'.format(scene.assetname)

    rig = selection[1]
    mesh = selection[0]

    posebones = bpy.context.selected_pose_bones_from_active_object
    bone_a = posebones[1]
    bone_b = posebones[0]

    expresion = "poseBone['{}'].matrix.col[1] @ poseBone['{}'].matrix.col[1]".format(bone_a.name, bone_b.name)

    fcurve = rig.data.shape_keys.key_blocks[bone_a.name.replace('c_', '')].driver_add('value')
    driver = fcurve.driver
    driver.expression = expresion
    # poseBone = driver.variables.new()

    var = driver.variables.new()

    var.type = 'TRANSFORMS'
    var.type = "SINGLE_PROP"
    var.name = 'poseBone'
    var.targets[0].id = mesh
    var.targets[0].data_path = 'pose.bones'


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    create_drive()

