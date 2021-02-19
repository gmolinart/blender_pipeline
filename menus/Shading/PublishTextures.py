import bpy


# from cgl.plugins.blender import Alchemy as alc

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
    from cgl.plugins.blender import alchemy as alc
    import bpy
    import os

    scene = alc.scene_object()

    texture_task = scene.copy(task='tex').latest_version()
    texture_task = texture_task.copy(version=texture_task.next_minor_version_number(), filename='')
    # print(texture_task_next.path_root)

    os.makedirs(texture_task.path_root)

    os.makedirs(texture_task.copy(context='render').path_root)
    ignore_list = ['b_painter_brush_img', 'Render Result']
    for image in bpy.data.images:
        filename = image.name.split(':')
        if len(filename) > 1:
            filename = filename[1]

        if image.name not in ignore_list:
            out_path = texture_task.copy(filename=filename, context='render', ext='exr').path_root
            image.save_render(out_path)
            image.filepath = out_path

    alc.save_file_as(texture_task.copy(context='source', set_proper_filename=True).path_root)
    alc.confirm_prompt(message='textures exported!!! ')
