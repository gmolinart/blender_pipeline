import bpy
# from cgl.plugins.blender import lumbermill as lm

class ImportAllObjects(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_all_objects'
    bl_label = 'Import All Objects'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



def import_environments():

    bpy.ops.object.make_local(type='ALL')

    env_collection = bpy.data.collections['env']

    for collection in env_collection.children:
        print('________collection {}______'.format(collection.name))
        for object in collection.objects:
            print(object.name)
            object.select_set(True)

    bpy.ops.object.duplicates_make_real()


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    import_environments()

