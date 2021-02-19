import bpy
from cgl.plugins.blender import alchemy as alc

class Snapshot(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.snapshot'
    bl_label = 'Snapshot'

    def execute(self, context):
        run()
        return {'FINISHED'}




def set_framerange(start=1, end=1, current=False):
    bpy.context.scene.frame_start = start
    bpy.context.scene.frame_end = end

    current = bpy.context.scene.frame_current
    if current:
        bpy.context.scene.frame_start = current
        bpy.context.scene.frame_end = current


def switch_overlays(visible=False):
    for window in bpy.context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_overlays = visible


def burn_in_image():
    current = bpy.context.scene
    mSettings = current.render
    sceneObject = alc.scene_object()
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

def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    burn_in_image()
    previewRenderTypes = ['anim', 'rig', 'mdl', 'lay']

    #switch_overlays(visible=False)
    scene = alc.scene_object
    scene.start_frame = bpy.context.scene.frame_start
    scene.end_frame = bpy.context.scene.frame_end

    set_framerange(current=True)

    if alc.scene_object().task in previewRenderTypes:

        alc.render(preview=True)



    else:
        alc.render()

    set_framerange(scene.start_frame, scene.end_frame)

    # switch_overlays(visible = True)


if __name__ == "__main__":
    run()