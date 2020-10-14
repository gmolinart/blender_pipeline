import bpy
# from cgl.plugins.blender import lumbermill as lm

class PublishTextures(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.publish_textures'
    bl_label = 'Publish Textures'

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
    from cgl.plugins.blender import lumbermill as lm
    import bpy
    import os

    scene = lm.scene_object()

    texture_task = scene.copy(task='tex').latest_version()
    texture_task = texture_task.copy(version=texture_task.next_minor_version_number(), filename='')
    # print(texture_task_next.path_root)

    os.makedirs(texture_task.path_root)

    os.makedirs(texture_task.copy(context='render').path_root)

    for image in bpy.data.images:
        out_path = texture_task.copy(filename=image.name, context='render').path_root
        image.save_render(out_path)

    lm.save_file_as(texture_task.copy(context='source', set_proper_filename=True).path_root)
    lm.confirm_prompt(message='textures exported!!! ')
