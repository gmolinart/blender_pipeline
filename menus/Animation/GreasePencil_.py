import bpy
# from cgl.plugins.blender import lumbermill as lm

class GreasePencil_(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.grease_pencil_'
    bl_label = 'GreasePencil'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}

def gpParentCommand():
    armature = bpy.context.selected_objects[0]
    poseBone = bpy.context.selected_pose_bones_from_active_object[0]
    gpName = '%s_%s_GP' % (bpy.context.selected_objects[0].name, poseBone.name)

    def parent_set(object, armature, bone):
        object.parent = armature
        object.parent_bone = bone
        object.parent_type = 'BONE'

    gpData = bpy.data.grease_pencils.new(gpName)
    gpencil = bpy.data.objects.new(gpName, gpData)

    bpy.context.scene.collection.objects.link(gpencil)

    parent_set(gpencil, armature, poseBone.name)

    gpData.stroke_depth_order = '3D'
    gpData.zdepth_offset = 0.5
    bpy.data.brushes['Draw Noise'].size = 3

    gpMaterial = 'MainGPMaterial'
    if gpMaterial not in bpy.data.materials:
        mat = bpy.data.materials.new(name=gpMaterial)
        bpy.data.materials.create_gpencil_data(mat)
    gpData.materials.append(bpy.data.materials[gpMaterial])


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    gpParentCommand()

