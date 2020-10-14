import bpy


# from cgl.plugins.blender import lumbermill as lm

class AddControllers(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.add_controllers'
    bl_label = 'Add Controllers'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


def set_bone_index_to_parent():
    bones = bpy.context.selected_pose_bones_from_active_object
    rig = bpy.context.object

    for bone in bones:
        parent = rig.data.bones[bone.name].parent
        print(parent.name)
        bone.bone_group_index = rig.pose.bones[parent.name].bone_group_index


def create_controller():
    bone = bpy.context.selected_bones[0]
    rig = bpy.context.object

    controllers = {'up': {'name': 'up',
                          'direction': 2,
                          'positive': 1,
                          'separation': 0.05},

                   'down': {'name': 'down',
                            'direction': 2,
                            'positive': -1,
                            'separation': 0.07},

                   'front': {'name': 'front',
                             'direction': 1,
                             'positive': -1,
                             'separation': 0.06},

                   'back': {'name': 'back',
                            'direction': 1,
                            'positive': 1,
                            'separation': 0.03},
                   }

    bones = []
    for i in controllers:
        new_bone_name = '{}_{}'.format(bone.name, controllers[i]['name'])
        new_bone = rig.data.edit_bones.new(new_bone_name)
        new_bone.head = bone.head
        new_bone.tail = bone.tail

        offset = controllers[i]['separation'] * controllers[i]['positive']
        new_bone.head[controllers[i]['direction']] += offset
        new_bone.tail[controllers[i]['direction']] += offset
        rig.data.bones.update()
        new_bone.parent = bone.parent
        # bpy.context.object.pose.bones[new_bone.name].bone_group_index = rig.pose.bones[bone.name].bone_group_index

        # bpy.ops.object.mode_set(mode='EDIT')
    return bones


def run():
    create_controller()
    print('4 way Controller created ')


