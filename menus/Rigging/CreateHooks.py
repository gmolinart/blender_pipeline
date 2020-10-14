import bpy
# from cgl.plugins.blender import lumbermill as lm

class CreateHooks(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.create_hooks'
    bl_label = 'CreateHooks'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



# change_locator_shape()

def change_locator_shape():

    for obj in bpy.context.selected_objects:
        obj.empty_display_type = 'CUBE'
        obj.empty_display_size = 0.2

def change_modifier_property(value):

    modifieres = bpy.context.object.modifiers

    for mod in modifieres:
        mod.falloff_type = value

def deselect_all_bezier_point(curveObj):
    for bezier_pt in curveObj.data.splines[0].bezier_points:
        bezier_pt.select_control_point = False
        bezier_pt.select_left_handle = False
        bezier_pt.select_right_handle = False

def run():


    curve = bpy.context.object
    hooks = []
    i = 0
    hook_objects = []
    for bpoint in curve.data.splines[0].bezier_points:
        locator = bpy.data.objects.new('{}.hook'.format(curve.name), None)
        bpy.context.scene.collection.objects.link(locator)
        locator.location = curve.matrix_world @ bpoint.co

        hooks.append(locator)
        hookModifier = bpy.context.object.modifiers.new(locator.name, 'HOOK')
        hookModifier.vertex_indices_set([i, i + 1, i + 2])
        print([i, i + 1, i + 2])
        hookModifier.object = locator
        hookModifier.strength = 1
        hookModifier.center = bpoint.co
        i += 3

    bpy.ops.object.mode_set(mode='EDIT')

    for m in curve.modifiers:
        bpy.ops.object.hook_reset(modifier=m.name)
        hook_objects.append(m.object)

    bpy.ops.object.mode_set(mode='OBJECT')

    for hooks in hook_objects:
        hooks.select_set(True)
        curve.select_set(True)
        bpy.ops.object.transforms_to_deltas(mode='ALL')
        bpy.ops.object.parent_set(keep_transform=True)

        hooks.empty_display_type = 'CUBE'
        hooks.empty_display_size = 0.2

        bpy.ops.object.select_all(action='DESELECT')
        curve.users_collection[0].objects.link(hooks)

        bpy.context.scene.collection.objects.unlink(hooks)
    curve.select_set(True)
    change_modifier_property(value='SPHERE')

