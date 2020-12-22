import bpy
from cgl.plugins.blender import lumbermill as lm
import pprint
from os import makedirs
from os.path import isdir
import json
from cgl.plugins.blender import utils as utils
import cgl.core.path as path


class PublishCameras(bpy.types.Operator):
    """
    Publishes Cameras from aster Layout files .
    """
    bl_idname = 'object.publish_cameras'
    bl_label = 'Publish Cameras'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run()
        return {'FINISHED'}


import bpy
from cgl.plugins.blender import lumbermill as lm


def rename_cameras():
    timeline_markers = bpy.context.scene.timeline_markers
    list = []
    for i in timeline_markers:
        list.append((i.frame, i))

    organized_markers = sorted(list, key=lambda tup: tup[0])

    selected_cam = bpy.context.selected_objects
    currentScene = lm.scene_object()

    shotIncrement = 10
    for i in organized_markers:
        camName = '%s_%04d_cam' % (currentScene.seq, shotIncrement)
        shotIncrement += 10
        i += (camName,)
        i[1].camera.name = i[2]
        i[1].camera.data.name = i[2]
        i[1].name = 'F_{}'.format(i[1].frame)

    return organized_markers


def export_cameras():
    exportedCameras = []
    markerDic = create_cam_dictionaries()
    for cameraToExport in bpy.context.selected_objects:
        if cameraToExport.type == 'CAMERA':

            if len(bpy.context.scene.timeline_markers) == 1:

                newShot = lm.scene_object().copy(filename=markerDic[cameraToExport.name]['name'],
                                                 version='000.000')

                newCamera = newShot.copy(task='cam', user='publish')
                camFolder = newCamera.copy(filename='').path_root



            else:

                newShot = lm.scene_object().copy(filename=markerDic[cameraToExport.name]['name'],
                                                 asset=markerDic[cameraToExport.name]['shot_number'],
                                                 version='000.000')

                newCamera = newShot.copy(task='cam', user='publish')

                camFolder = newCamera.copy(filename='').path_root

            if not isdir(camFolder):
                makedirs(camFolder)

            else:
                print(camFolder + ' Exists')
                newCamera.next_major_version()
                newCamera = newCamera.next_major_version()
                camFolder = newCamera.copy(filename='').path_root
                makedirs(camFolder)
                print(newCamera.path)

            fbxPath = newCamera.copy(ext='fbx')

            # fbxLatest = fbxPath.latest_version()

            data = markerDic[cameraToExport.name]

            # for i in markerDic:
            #    print(i)

            print(data)
            outFile = fbxPath.copy(ext='json').path_root

            with open(outFile, "w") as library_data_file:
                json.dump(data, library_data_file, indent=4, sort_keys=True)

            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            cameraToExport.select_set(True)
            lm.export_selected(fbxPath.path_root)
            lm.save_file_as(newCamera.copy(ext= 'blend').path_root)

            layout_file = newCamera.copy(filename=newCamera.filename.replace('cam', 'lay'), task='lay', ext='json',
                                         user='publish')
            layout_dir = layout_file.copy(filename='').path_root
            # newShot.publish()
            # newShotCam.publish()
            # if not isdir(layout_dir):
            #     makedirs(layout_dir)
            path.CreateProductionData(path_object=layout_file.copy(filename=''), create_default_file=True)
            # lm.create_file_dirs(layout_dir)
            utils.write_layout(outFile=layout_file.path_root)
            exportedCameras.append(cameraToExport.name)
        camerasText = ' '.join([str(elem) for elem in exportedCameras])
        outputText = 'Published cameras:{}'.format(camerasText)
        print(outputText, layout_file.path)
        # lm.confirm_prompt(title='Publish Cameras ', message='Camera Publish Complete')


def create_cam_dictionaries():
    pp = pprint.PrettyPrinter(indent=4)
    selected_cam = bpy.context.selected_objects
    currentScene = lm.scene_object()
    f_start = bpy.context.scene.frame_start
    f_end = bpy.context.scene.frame_end

    print('________markers_________')
    markerDic = {}
    if len(bpy.context.scene.timeline_markers) == 0:
        print('please add timeline markers')

    bpy.context.scene.frame_set(1)
    timeline_markers = bpy.context.scene.timeline_markers

    if '' in timeline_markers:
        timeline_markers.remove(timeline_markers[''])

    organized_markers = rename_cameras()

    iteration = 1
    for marker in organized_markers:

        shotNumber = marker[1].camera.name.split('_')[2]

        if iteration < len(organized_markers):

            end_frame = organized_markers[iteration][1].frame - 1
        else:
            end_frame = f_end

        markerDic[marker[1].camera.name] = {'name': marker[1].camera.name,
                                            'frame_start': marker[1].frame,
                                            'frame_end': end_frame,
                                            'shot_number': shotNumber,
                                            'source_layout': currentScene.path}
        print('{}'.format(marker[1].name))
        iteration += 1

    pp.pprint(markerDic)
    bpy.context.scene.frame_set(1)  #############REMOVE

    return markerDic


def run():
    """
    This run statement is what's executed when your button is pressed in blender.
    :return:
    """
    # create_cam_dictionaries()
    export_cameras()


if __name__ == "__main__":
    run()