import bpy
# from cgl.plugins.blender import lumbermill as lm

class CreateDefaultController(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.create_default_controller'
    bl_label = 'CreateDefaultController'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}




def run():
    default_controller_name = 'c_box_default'

    if not any([m for m in bpy.data.objects if m.name == default_controller_name]):

        bpy.data.objects.new(default_controller_name, None)
        print('default controller created')

    else:
        print('default controller already in scene')

    cs_object = bpy.data.objects[default_controller_name]
    cs_object.empty_display_type = 'CUBE'



    for bone in bpy.context.selected_pose_bones_from_active_object:
        bone.custom_shape = cs_object
        bone.custom_shape_scale = 0.3

