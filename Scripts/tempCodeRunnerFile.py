import os
import sys
from sys import stderr

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

try:
    import maya.cmds as mc
    import maya.mel as mel
except:
    pass


def split(strng, sep, pos):
    """Split a string. Insert 'pos' to tell when the splitter should start splitting

    Arguments:
        strng {string} -- String to do the split on
        sep {string} -- The sperator
        pos {string} -- Position from where the seperation should start

    Returns:
        string -- String that have been splitted
    """
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])


def list_subfolders(check_path, return_full_path=False):
    """Lists all subfolders of given path

    Arguments:
        check_path {string} -- Path to check for subfolders
        return_full_path {boolean} -- Wether it should return just the folder name or the full path

    Returns:
        list -- Returns a list of all subfolders
    """

    if return_full_path:
        folders = [os.path.join(check_path, d) for d in os.listdir(check_path)]
    else:
        folders = [dI for dI in os.listdir(check_path) if os.path.isdir(
                                            os.path.join(check_path, dI)
                                                                       )]
    return folders


def ensure_dir(file_path):
    """Function to check if a directory exists or not.
    Will create path if it does not exist

    Arguments:
        file_path {string} -- file path to check if it exists or not

    Returns:
        string -- returns the file path after going through the condition
    """

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    else:
        print "Directory exists"

    return file_path


def find_dir(start_from, dir_name):
    filepath = None
    # get parent of the .py running
    par_dir = os.path.dirname(start_from)
    while True:
        # get basenames of all the directories in that parent
        dirs = [os.path.basename(os.path.join(par_dir, d)) for d in os.listdir(par_dir) if os.path.isdir(os.path.join(par_dir, d))]
        # the parent contains desired directory
        if dir_name in dirs:
            filepath = par_dir
            break
        # back it out another parent otherwise
        par_dir = os.path.dirname(par_dir)

    return filepath


def export_to_sub():
    """Used for Prism Pipeline to export the selected geometry for Substance Painter.
    The exported fbx filename only includes the asset name and no padding.
    """

    objs_to_export = mc.ls(sl=True)

    if objs_to_export:
        try: mc.FBXExport
        except:
            try: mc.loadPlugin('fbxmaya')
            except:
                stderr.write('ERROR: FBX Export Plug-in was not detected.\n')
                return False

        export_folder = "/Export/shdExport/"

        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        new_path = filepath.replace(filename, "")
        asset_name = filename.split("_")[0]

        split_dir = split(new_path, asset_name, 2)

        # Check if the file is a character
        if "characters" in filepath:
            if "props" in filepath:
                path_dir = filepath.split(asset_name)[0] + asset_name + export_folder
            elif not split_dir[-1]:
                path_dir = filepath.split(asset_name)[0] + asset_name + export_folder
            else:
                path_dir = split(new_path, asset_name, 2)[0] + asset_name + export_folder
        else:
            path_dir = filepath.split(asset_name)[0] + asset_name + export_folder

        # Create path if it does not exist
        ensure_dir(path_dir)

        # Fbx export settings
        mel.eval('FBXExportFileVersion "FBX2019"') 
        mel.eval('FBXExportInputConnections -v 0')
        mel.eval('FBXExportUpAxis y')

        # Export selection
        mel.eval('FBXExport -f "{0}{1}" -s'.format(path_dir, asset_name))
        print path_dir
    else:
        mc.warning("No object is selected!")


def export_anim():
    """Used for Prism Pipeline to export the selected geometry for Substance Painter.
    The exported fbx filename only includes the asset name and no version number.
    """

    print "yes no work"
    objs_to_export = mc.ls(sl=True)

    if len(objs_to_export) == 1:
        try: mc.FBXExport
        except:
            try: mc.loadPlugin('fbxmaya')
            except:
                stderr.write('ERROR: FBX Export Plug-in was not detected.\n')
                return False

        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        new_path = filepath.replace(filename, "")
        asset_name = filename.split("_")[0]

        root_dir = find_dir(new_path, "00_Pipeline")
        print root_dir

        subfolders = list_subfolders(root_dir)

        seq_name = filename.split("_")[1].replace("-", "_")

        # Find the folder where live assets should be copied to
        for folder in subfolders:
            if "live" in folder:

                sel = mc.ls(sl=True)

                for obj in sel:
                    short_name = obj.split(":")[-1].split("_")[0]

                    export_name = seq_name + "_" + short_name

                    export_dir = ensure_dir(root_dir + "/" + folder + "/_anim/" + seq_name)

                    mel.eval('FBXExportFileVersion "FBX2019"') 
                    mel.eval('FBXExportInputConnections -v 0')
                    mel.eval('FBXExportUpAxis y')

                    # Export selection
                    mel.eval('FBXExport -f "{0}/{1}" -s'.format(export_dir, export_name))
                    print export_dir
    else:
        mc.warning("Select one object only!")


import truemax_export_ui
qtCreatorFile = "truemax_export_ui.ui"  # Enter file here.

#Ui_MainWindow, QtBaseClass = loadUiType(qtCreatorFile)


class TruemaxExport(QMainWindow, truemax_export_ui.Ui_Truemax):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.substance_button.clicked.connect(self.substance_export)
        self.anim_button.clicked.connect(self.anim_export)

    def substance_export(self):
        print "substance"

    def anim_export(self):
        print "anim"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TruemaxExport()
    window.show()
    sys.exit(app.exec_())
