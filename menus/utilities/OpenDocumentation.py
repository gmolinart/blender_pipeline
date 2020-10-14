import bpy
from bpy.types import Header, Menu, Panel
import os

def dump(obj, text):
    print('-'*40, text, '-'*40)
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))



def getDoc(name):
    name = name.replace(' ', '')
    documentation = 'https://app.tettra.co/teams/lonecoconut/pages/{}'.format(name)

    return documentation

class OpenDocumentation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = 'object.open_documentation'
    bl_label = 'Open Documentation'

    #
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        if hasattr(context, 'button_pointer'):
            btn = context.button_pointer
            dump(btn, 'button_pointer')

        if hasattr(context, 'button_prop'):
            prop = context.button_prop
            dump(prop, 'button_prop')

        if hasattr(context, 'button_operator'):
            op = context.button_operator
            dump(op, 'button_operator')
            print(getDoc(op.bl_rna.name))
            os.system('explorer {}'.format(getDoc(op.bl_rna.name)))

        return {'FINISHED'}

# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(Menu):
    bl_label = "Add Viddyoze Tag"

    def draw(self, context):
        pass

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OpenDocumentation.bl_idname, icon='URL')

def register():
    bpy.types.WM_MT_button_context.append(menu_func)

def unregister():
    bpy.types.WM_MT_button_context.remove(menu_func)


from bpy.utils import register_class
classes = [OpenDocumentation,WM_MT_button_context]
for cls in classes:
    register_class(cls)
register()