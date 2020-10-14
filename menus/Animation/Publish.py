import bpy
# from cgl.plugins.blender import lumbermill as lm

class Publish(bpy.types.Operator):
    """
    from selected object renames action and publishes the current file
    """
    bl_idname = 'object.publish'
    bl_label = 'Publish'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


import bpy
from cgl.plugins.blender import lumbermill as lm


def renanme_action():
    objects = bpy.context.selected_objects
    # selected_object = bpy.context.object
    for selected_object in objects:
        action = selected_object.animation_data.action
        currentScene = lm.scene_object()

        newActionName = '_'.join([currentScene.filename_base, selected_object.name, currentScene.version])
        action.name = newActionName
        print(newActionName)


def write_anim(outFile=None):
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject, import_file
    import bpy
    from pathlib import Path
    import json
    if outFile == None:
        outFile = scene_object().copy(ext='json').path_root
    data = {}

    for obj in bpy.data.objects:
        if 'proxy' in obj.name:
            name = obj.name
            print('___________' + name)
            #            blender_transform = np.array(obj.matrix_world).tolist()
            blender_transform = [obj.matrix_world.to_translation().x,
                                 obj.matrix_world.to_translation().y,
                                 obj.matrix_world.to_translation().z,
                                 obj.matrix_world.to_euler().x,
                                 obj.matrix_world.to_euler().y,
                                 obj.matrix_world.to_euler().z,
                                 obj.matrix_world.to_scale().x,
                                 obj.matrix_world.to_scale().y,
                                 obj.matrix_world.to_scale().z]
            libraryPath = bpy.path.abspath(obj.proxy_collection.instance_collection.library.filepath)
            filename = Path(bpy.path.abspath(libraryPath)).__str__()
            libObject = LumberObject(filename)

            data[name] = {'name': libObject.asset,
                          'source_path': libObject.path,
                          'blender_transform': blender_transform,
                          'blender_action': obj.animation_data.action.name}

    with open(outFile, "w") as library_data_file:
        json.dump(data, library_data_file, indent=4, sort_keys=True)

    return (outFile)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    write_anim()


