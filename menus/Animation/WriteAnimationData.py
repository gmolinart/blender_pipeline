import bpy
from cgl.plugins.blender import alchemy as alc


class WriteAnimationData(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.write_animation_data'
    bl_label = 'WriteAnimationData'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def renanme_action():
    objects = bpy.context.selected_objects
    # selected_object = bpy.context.object
    for selected_object in objects:
        action = selected_object.animation_data.action
        if action:

            currentScene = alc.scene_object()

            newActionName = '_'.join([currentScene.filename_base, selected_object.name, currentScene.version])
            action.name = newActionName
            print(newActionName)

        else:
            alc.confirm_prompt(message='No action linked to object')


def write_anim(outFile=None):
    from cgl.plugins.blender.alchemy import scene_object, PathObject, import_file
    from cgl.core.utils.read_write import load_json, save_json
    import bpy
    from pathlib import Path

    if outFile == None:
        outFile = scene_object().copy(ext='json').path_root
    data = {}

    data = load_json(outFile)

    valid_rigs = []

    for obj in bpy.data.objects:

        if 'proxy' in obj.name:
            animation_data = obj.animation_data
            if animation_data:
                action = animation_data.action
                if action:
                    valid_rigs.append(obj)

    for obj in valid_rigs:
        name = obj.name.split('_proxy')[0]
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
        libObject = PathObject(filename)

    sourcePath = alc.scene_object()

    data[name] = {'name': libObject.asset,
                  'source_path': libObject.path,
                  'blender_transform': blender_transform,
                  'blender_action': obj.animation_data.action.name,
                  'blender_action_path': sourcePath.path}

    save_json(outFile, data)

    print(data)
    return (outFile)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    renanme_action()

    write_anim()
    alc.save_file()


if __name__ == "__main__":
    run()