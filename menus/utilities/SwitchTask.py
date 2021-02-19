import bpy
from cgl.plugins.blender import alchemy as alc

def get_items(self, context):
    from cgl.plugins.blender import alchemy as alc
    import os

    scene = alc.scene_object()

    tasks = scene.glob_project_element('task')
    print(tasks)

    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]

    return (value)


class SwitchTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.switch_task'
    bl_label = 'Switch Task'
    bl_property = "selected_task"
    selected_task = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_task)
        new_user = alc.scene_object().copy(task=self.selected_task, user ='publish',set_proper_filename=True).latest_version().path_root
        alc.open_file(new_user)
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
    bpy.utils.register_class(SwitchTask)
    bpy.ops.object.switch_task('INVOKE_DEFAULT')