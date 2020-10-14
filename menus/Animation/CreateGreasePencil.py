import bpy
# from cgl.plugins.blender import lumbermill as lm

class CreateGreasePencil(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.create_grease_pencil'
    bl_label = 'Create Grease Pencil'

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

    if not any([m for m in bpy.data.objects if m.name == gpName]):

        gpData = bpy.data.grease_pencils.new(gpName)

        gpencil = bpy.data.objects.new(gpName, gpData)
        bpy.context.scene.collection.objects.link(gpencil)

        parent_set(gpencil, armature, poseBone.name)


    else:
        gpencil = bpy.data.objects[gpName]
        gpData = gpencil.data

    gpData.stroke_depth_order = '3D'
    gpData.zdepth_offset = 0.5
    for brushes in bpy.data.brushes:
        brushes.size = 6


    gpMaterial = 'MainGPMaterial'
    if gpMaterial not in bpy.data.materials:
        mat = bpy.data.materials.new(name=gpMaterial)
        bpy.data.materials.create_gpencil_data(mat)
    gpData.materials.append(bpy.data.materials[gpMaterial])

    return gpencil




def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    gp = gpParentCommand()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    gp.select_set(True)
    bpy.context.view_layer.objects.active = gp
    bpy.ops.object.mode_set(mode='PAINT_GPENCIL')
    bpy.context.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'


