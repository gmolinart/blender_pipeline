import bpy
import sys
import os
import bpy
from importlib import reload

bl_info = {
    "name": "Production Alchemy",
    "author": "Tom Mikota & Guillermo Molina",
    "version": (1, 3),
    "blender": (2, 80, 3),
    "location": "View3D ",
    "description": "Production Alchemy infrastruture",
    "warning": "",
    "wiki_url": "",
    "category": "Generic",
}


def run():
    from os.path import expanduser

    home = expanduser('~')
    source_dir = r"{}\PycharmProjects\cglumberjack".format(home)
    if source_dir not in sys.path:
        sys.path.insert(0, source_dir)
    cgl_dir = r"D:\CGLUMBERJACK\COMPANIES\master\config\master"
    if cgl_dir not in sys.path:
        sys.path.insert(0, cgl_dir)
    if os.path.isdir('C:\Python37'):
        
        python_dev_packages = r'C:\Python37\Lib\site-packages'
    if os.path.isdir('C:\Python38'):
        python_dev_packages = r'C:\Python38\Lib\site-packages'
    if python_dev_packages not in sys.path:
        sys.path.insert(0, python_dev_packages)
    import cgl.plugins.blender.custom_menu as cm
    reload(cm)
    try:
        cm.LumberMenu().delete_menus()
    except RuntimeError:
        print('No Shelves to Delete, skipping')

    cm.LumberMenu().load_menus()


# class LumbermillLoad(bpy.types.Operator):
#    """Tooltip"""
#    bl_idname = "object.lumbermillload"
#    bl_label = "Alchemy"

#    #@classmethod
#    #def poll(cls, context):
#        

#    def execute(self, context):
#        main(context)
#        return {'FINISHED'}


def register():
    run()
    # bpy.utils.register_class(LumbermillLoad)
    # bpy.ops.object.lumbermillload()


def unregister():
    import cgl.plugins.blender.custom_menu as cm
    cm.LumberMenu().delete_menu
    # bpy.utils.unregister_class(LumberMenu)


if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.object.lumbermillload()
