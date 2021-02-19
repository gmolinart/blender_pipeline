import os
import bpy
from cgl.plugins.blender import alchemy as alc
from shutil import copyfile


def get_name_from_task():
    from cgl.core.config.config import ProjectConfig
    import getpass

    CONFIG = ProjectConfig().project_config
    task = getpass.gettask().lower()
    target_tasks = CONFIG['project_management']['ftrack']['tasks'][task]['first']
    print(target_tasks)
    return target_tasks

def get_items(self, context):
    from cgl.plugins.blender import alchemy as alc
    scene = alc.scene_object()

    tasks = scene.glob_project_element('task')

    target_tasks = ['lay','anim','light','rig']
    for task in target_tasks:
        if task not in tasks:
            tasks.append(task)

    print(tasks)

    value = [(tasks[i], tasks[i], '') for i in range(len(tasks))]

    return (value)


class CopyToTask(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.copy_to_task'
    bl_label = 'Copy To Task'
    bl_property = "selected_task"
    selected_task = bpy.props.EnumProperty(items=get_items)
    def execute(self, context):
        self.report({'INFO'}, "Selected: %s" % self.selected_task)
        new_task = alc.scene_object()

        task_version = new_task.copy(task=self.selected_task)
        task_version_dir = task_version.copy(filename='')
        new_version = task_version_dir.new_minor_version_object()
        if os.path.isdir(new_version.path_root):
            new_version = new_version.new_minor_version_object()

        else :
            new_version = new_version.copy(major = '000', minor = '000')
        os.makedirs(new_version.path_root)
        alc.save_file_as(new_version.copy(set_proper_filename=True).path_root)
        alc.open_file(new_version.copy(set_proper_filename=True).path_root)
        if os.path.isfile(alc.scene_object().copy(extension='json').path_root):
            print("______________Json File Saved____________")
            copyfile(alc.scene_object().copy(extension='json').path_root,
                     new_version.copy(set_proper_filename=True, ext='json').path_root)
        else:
            print("______________No Json File on: ____________")
            print(alc.scene_object().copy(extension='json').path_root)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CopyToTask)


def unregister():
    bpy.utils.unregister_class(CopyToTask)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.copy_to_task('INVOKE_DEFAULT')