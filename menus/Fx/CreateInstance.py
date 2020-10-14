import bpy
from cgl.plugins.blender import lumbermill as lm

class CreateInstance(bpy.types.Operator):
    """
    Select object to be instanced and then the surface that will have the elements added to
    """
    bl_idname = 'object.create_instance'
    bl_label = 'Create Instance'

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

    active = bpy.context.active_object

    selection = bpy.context.selected_objects
    instanced_collection = None
    for obj in selection:
        if not obj == active:
            if obj.is_instancer:
                instanced_collection = bpy.data.collections[obj.name.split('.')[0]]

    bpy.ops.object.particle_system_add()
    instance = active.particle_systems['ParticleSettings']
    instance.name = 'instance'
    settings = instance.settings
    settings.type = 'HAIR'
    settings.use_advanced_hair = True
    settings.use_rotations = True
    settings.rotation_mode = 'GLOB_Y'
    settings.render_type = 'COLLECTION'

    settings.use_whole_collection = True
    if instanced_collection:

        settings.instance_collection = instanced_collection
        instance.name = obj.name.split('.')[0]
        lm.confirm_prompt(message='Instance Created')
    else:

        lm.confirm_prompt(message='instance created please select collection in the render section ')
