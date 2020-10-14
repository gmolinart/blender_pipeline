import bpy
# from cgl.plugins.blender import lumbermill as lm


class FourWayController(bpy.types.Operator):
    """
    This class is required to register a button in blender.
    """
    bl_idname = 'object.four_way_controller'
    bl_label = 'FourWayController'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}



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

    for i in controllers:
        new_bone = bpy.data.objects['LORA_rig'].data.edit_bones.new('newBone')
        new_bone.head = bone.head
        new_bone.tail = bone.tail

        offset = controllers[i]['separation'] * controllers[i]['positive']
        new_bone.head[controllers[i]['direction']] += offset
        new_bone.tail[controllers[i]['direction']] += offset
        new_bone.name = '{}_{}'.format(bone.name, controllers[i]['name'])
        new_bone.parent = bone.parent
        rig.pose.bones[new_bone.name].bone_group_index = rig.pose.bones[bone.name].bone_group_index


def run():
    create_controller()
    print('4 way Controller created')

