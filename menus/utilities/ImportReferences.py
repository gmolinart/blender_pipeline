import bpy


# from cgl.plugins.blender import lumbermill as lm

class ImportReferences(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_references'
    bl_label = 'Import References'

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def run():
    import bpy
    import os

    from cgl.plugins.blender import lumbermill as lm

    current_task = lm.scene_object()

    ref = current_task.copy(task='ref', user='publish', filename='', context='render').latest_version()

    if not os.path.isdir(ref.path_root):
        ref = current_task.copy(task='ref', filename='', context='render').latest_version()

    print(ref.path_root)

    if os.path.isdir(ref.path_root):

        images = os.listdir(ref.path_root)
        print(images)
        spacing = 0.0
        for obj in bpy.data.objects:
            if 'DEFAULT_ref' in obj.name:
                bpy.data.objects.remove(obj)

        for image in images:
            image_path = '{}/{}'.format(ref.path_root, image)
            try:
                bpy.ops.object.load_reference_image(filepath=image_path)
                bpy.context.object
                bpy.context.object.rotation_euler = (1.5707963705062866, 0.0, 0.0)
                spacing += 5
                bpy.context.object.name = 'DEFAULT_ref'
                bpy.context.object.location = (spacing, 0.0, 0.0)
            except RuntimeError:
                pass

