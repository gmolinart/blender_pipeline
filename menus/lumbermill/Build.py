import bpy
import json
from os.path import isdir, isfile
from cgl.plugins.blender import lumbermill as lm
from cgl.plugins.blender import utils as utils


class Build(bpy.types.Operator):
    """
    Builds the shot with all the avilable elements
    """
    bl_idname = 'object.build'
    bl_label = 'Build'

    def execute(self, context):
        run()
        return {'FINISHED'}


def defaultShotSettings():
    scene = bpy.context.scene
    scene.eevee.taa_render_samples = 1
    scene.eevee.taa_samples = 1
    scene.eevee.shadow_cube_size = '2048'


def gather_dependencies():
    current = lm.scene_object()

    # Gather Dependencies
    light_file = current.copy(task='light', set_proper_filename=True).latest_version()

    ref_file = current.copy(task='ref', set_proper_filename=True).latest_version()

    anim_file = current.copy(task='anim', set_proper_filename=True).latest_version()
    modeling_file = current.copy(task='mdl', context='render', set_proper_filename=True).latest_version()

    layout_file = current.copy(task='lay',
                               set_proper_filename=True,
                               ext='json',
                               user='publish').latest_version()

    camera_file = current.copy(task='cam',
                               set_proper_filename=True,
                               ext='blend',
                               user='publish').latest_version()

    dependencies = [light_file, anim_file, layout_file, camera_file, ref_file, modeling_file]

    return dependencies


def required_dependencies():
    requirements = []
    current = lm.scene_object()

    if current.task == 'lay':
        requirements.append('lay')
        requirements.append('cam')

    if current.task == 'anim':
        requirements.append('lay')
        requirements.append('cam')

    if current.task == 'mdl':
        requirements.append('ref')

    if current.task == 'rig':
        requirements.append('ref')
        requirements.append('mdl')

    if current.task == 'light':
        requirements.append('lay')
        requirements.append('cam')
        requirements.append('anim')

    return requirements


def import_dependencies():
    for depObject in gather_dependencies():
        print(depObject.path_root)
        print(depObject.task)

        if depObject.task in required_dependencies():

            if depObject.task == 'lay':
                if isfile(depObject.path_root):
                    print('{} exists'.format(depObject.path_root))

                    print('_____LAYOUT______')
                    print(depObject.filename)
                    bpy.ops.object.read_layout()
                    burn_in_image()

            if depObject.task == 'cam':
                if isfile(depObject.path_root):
                    print('{} exists'.format(depObject.path_root))

                    print('_________CAMERA____________')
                    print(depObject.filename)
                    json = depObject.copy(ext='json')
                    print(json)
                    lm.import_file(depObject.path_root, type='CAMERA', linked=False,
                                   collection_name=depObject.filename_base)

                    if depObject.filename_base not in bpy.context.scene.collection.objects:
                        bpy.context.scene.collection.objects.link(bpy.data.objects[depObject.filename_base])
                    frame_start = set_shot_duration(json)

                    action = bpy.data.objects[depObject.filename_base].animation_data.action
                    for fcurve in action.fcurves:
                        for point in fcurve.keyframe_points:
                            point.co.x += 1000 - frame_start

                    try:

                        bpy.ops.action.view_frame()
                    except RuntimeError:
                        pass
            if depObject.task == 'anim':
                if isfile(depObject.path_root):
                    print('{} exists'.format(depObject.path_root))

                    print('_____ANIM______')
                    print(depObject.filename)
                    utils.read_layout()
                    burn_in_image()

            if depObject.task == 'mdl':
                if isfile(depObject.path_root):
                    print('{} exists'.format(depObject.path_root))
                    import_mesh_from_file(depObject)
                    burn_in_image()

            if depObject.task == 'ref':
                print('_____ref______')
                bpy.ops.object.import_references()
                burn_in_image()

            if depObject.task == 'rig':
                if isfile(depObject.path_root):
                    print('{} exists'.format(depObject.path_root))

                    print('_____rig______')
                    burn_in_image()



            else:
                print('{} object not Available'.format(depObject.path_root))


def burn_in_image():
    current = bpy.context.scene
    mSettings = current.render
    sceneObject = lm.scene_object()
    current.name = sceneObject.filename_base
    scene_info = bpy.context.scene.statistics(bpy.context.view_layer)
    try:
        mSettings.metadata_input = 'SCENE'
    except AttributeError:
        mSettings.use_stamp_strip_meta = 0

    mSettings.stamp_font_size = 26
    mSettings.use_stamp = 1
    mSettings.use_stamp_camera = 1
    mSettings.use_stamp_date = 0
    mSettings.use_stamp_frame = True
    mSettings.use_stamp_frame_range = 0
    mSettings.use_stamp_hostname = 0
    mSettings.use_stamp_labels = 0
    mSettings.use_stamp_lens = 1
    mSettings.use_stamp_marker = 0
    mSettings.use_stamp_memory = 0
    mSettings.use_stamp_note = 0
    mSettings.use_stamp_render_time = 0
    mSettings.use_stamp_scene = 1
    mSettings.use_stamp_sequencer_strip = 0
    mSettings.use_stamp_time = 1
    mSettings.use_stamp_note = True
    mSettings.stamp_note_text = scene_info

    print('sucess')


def set_shot_duration(camJson):
    # dependencies  = gather_dependencies()
    # print(dependencies)
    default_start_frame = 1000
    current = lm.scene_object()
    filename = camJson

    # filename = '{}_{}_{}.json'.format(current.seq, current.asset, 'cam')
    # outFile = lm.scene_object().copy(task='cam', filename=filename).path_root
    outFile = camJson.path_root

    with open(outFile) as json_file:
        data = json.load(json_file)

    bpy.context.scene.frame_start = 1001
    print('________________________frameset____________')
    print('{} start'.format(data['frame_start']))
    print('{} end'.format(data['frame_end']))

    endFrame = data['frame_end'] - data['frame_start']
    bpy.context.scene.frame_end = 1001 + int(endFrame)
    bpy.context.scene.frame_current = 1001
    print(endFrame)
    return (data['frame_start'])


def buildShot():
    bpy.ops.object.fix_collection_name()
    bpy.ops.object.correct_file_name()
    defaultShotSettings()
    import_dependencies()
    burn_in_image()
    # bpy.ops.object.setup_collections()

    # bpy.ops.object.setup_shader_color()


def gather_object_list(outFile):
    from cgl.plugins.blender.lumbermill import scene_object, LumberObject, import_file
    from cgl.core.utils.read_write import load_json
    import bpy

    if outFile == None:
        outFileObject = scene_object().copy(ext='json', ).latest_version()
        outFileObject.set_attr(filename='%s_%s_%s.%s' % (outFileObject.seq,
                                                         outFileObject.shot,
                                                         outFileObject.task,
                                                         'json'
                                                         ))
        outFile = outFileObject.path_root
    # outFile = scene_object().path_root.replace(scene_object().ext, 'json')

    data = load_json(outFile)

    for p in data:
        print(p)

    return data


def remove_object(name):
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        bpy.data.objects.remove(obj)


def import_mesh_from_file(file):
    print('_____MDL______')
    outFile = file.copy(ext='json')
    objects = gather_object_list(outFile.path_root)
    for obj in objects:
        remove_object(obj)
    lm.import_file(file.path_root, append=False, linked=False)
    for obj in objects:
        object = bpy.data.objects[obj]
        bpy.context.collection.objects.link(object)


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    buildShot()
    try:

        lm.confirm_prompt(message='Build Completed')
    except RuntimeError:
        pass


if __name__ == "__main__":
    run()