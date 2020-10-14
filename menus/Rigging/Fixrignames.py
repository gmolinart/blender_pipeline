import bpy
from cgl.plugins.blender import lumbermill as lm

class Fixrignames(bpy.types.Operator):
    """
    takes in object and fixes the rigNames , currently for auto rigger pro
    """
    bl_idname = 'object.fixrignames'
    bl_label = 'Fixrignames'
    selection = bpy.props.StringProperty()
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        run(self.selection)
        return {'FINISHED'}


def fix_rig_names(selection=''):

    if selection == '':

        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                if not 'add' in obj.data.name:
                    selection = obj
    else:
        selection = bpy.data.objects[selection]

    currentScene = lm.scene_object()
    assetName = lm.scene_object().shot
    selection.name = '{}_rig'.format(assetName)
    selection.data.name = '{}_rig'.format(assetName)
    try:

        selection.parent.name = '{}_grp'.format(assetName)

    except:
        print('{}_grp not found'.format(assetName))
        pass

    try :
        children_obj = selection.parent.children
        if lm.scene_object().type == 'char':

            for children in children_obj:
                if children != selection:
                    children.name = '{}_rig_add'.format(assetName)
                    children.data.name = '{}_rig_add'.format(assetName)

        for child in selection.children:
            if 'mesh' in child.name:
                child.name = '{}_mesh_grp'.format(assetName)
    except(AttributeError):
        print('armature has not children')

    selection.users_collection[0].name = assetName


def run(selection=''):
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """

    fix_rig_names(selection)
    print('Rignames corrected')

