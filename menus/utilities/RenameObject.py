import bpy
from cgl.plugins.blender import lumbermill as lm

class RenameObject(bpy.types.Operator):
    """
    simple renamer.. really basic
    """
    bl_idname = 'object.rename_object'
    bl_label = 'Rename Object'
    selection = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run(self.selection)
        return {'FINISHED'}


def run(selection=''):
    """
    simple renamer.. really basic .
    :return:
    """


    current_scene = lm.scene_object()

    if selection == '':
        selection = bpy.context.selected_objects

    else:
        selection = [bpy.data.objects[selection]]

    for i in selection:
        asset = current_scene.shot

        if '_' in i.name:
            i.name = '{}_{}'.format(asset, i.name.split('_')[1])

        if '.' in i.name:
            i.name = i.name.split('.')[0]

        else:
            i.name = asset

