import bpy
import os
from cgl.plugins.blender import lumbermill as lm


def get_items(self, context):
    from cgl.plugins.blender import lumbermill as lm

    scene = lm.scene_object()

    tasks = scene.glob_project_element('task')
    tasks.append('Base Mesh')
    print(tasks)

    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]
    # TODO - I'd like to have te task changed from short to long form
    return (value)


class ImportTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.import_task'
    bl_label = 'Import Task'
    bl_property = "selected_task"
    selected_task = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_task)

        if self.selected_task == 'Base Mesh':
            new_task = lm.scene_object().copy(context='render', task='mdl', type='lib', asset='baseMesh',
                                              user='publish',
                                              set_proper_filename=True).latest_version().path_root
        else:

            new_task = lm.scene_object().copy(context='render', task=self.selected_task, user='publish',
                                              set_proper_filename=True).latest_version().path_root
        if os.path.isfile(new_task):

            print(new_task)
            lm.import_file(new_task, linked=True, append=False)

        else:
            lm.confirm_prompt(
                message='publish not found, please check if the task has been published or import manually  ')

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    print('Hello World!: button_template')


if __name__ == '__main__':
    bpy.utils.register_class(ImportTask)
    bpy.ops.object.import_task('INVOKE_DEFAULT')