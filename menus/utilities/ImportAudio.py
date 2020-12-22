import bpy
# from cgl.plugins.blender import lumbermill as lm

class ImportAudio(bpy.types.Operator):
    """
    Imports audio fro the scene
    """
    bl_idname = 'object.import_audio'
    bl_label = 'Import Audio'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


from cgl.plugins.blender import lumbermill as lm
import bpy


def import_audio(path, name):
    scn = bpy.context.scene

    if not scn.sequence_editor:
        scn.sequence_editor_create()

    sequences = scn.sequence_editor.sequences

    sequences.new_sound(
        name=name,
        filepath=path,
        channel=0, frame_start=1
    )


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    audio = lm.scene_object().copy(task='audio', ext='mp3', latest=True, set_proper_filename=True)

    import_audio(audio.path_root, audio.filename_base)

