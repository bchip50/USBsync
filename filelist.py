# Import the os module, for the os.walk function
import os
import pathlib


def get_ext(files: list, exts=['.mp3', '.wma']) -> str:
    extlist = {*exts}
    for f in files:
        if f.lower().endswith(extlist):
            return f[-3:]
        return ''


class FileList():
    def __init__(self, base_name: str, ext_list=['.mp3', '.wma']):
        self.base_name = base_name
        self.ext_list = [s.lower() for s in ext_list]

    def get_list(self) -> list:
        """ Compile of list of directories and sub-directories
            The list contains tuples with the name of the artist and album
            the number of files in the directory
            and the extension of the first file in the directory
            """
        out_list = []
        for base_name, subdirList, fileList in os.walk(self.base_name):
            dirName = os.path.normcase(base_name)
            # print('Found directory: %s' % base_name)
            splitName = dirName.split('\\')
            if len(splitName) == 2 and len(splitName[1]) > 0 and len(subdirList) > 0:
                src_parent = splitName[1]
                out_list.append((dirName[3:], splitName[1], '', len(subdirList), 'dir'))
            if len(splitName) == 3 and len(splitName[2]) > 0 and len(fileList) > 1:
                test_file = fileList[1]
                file_ext = test_file[-4:]
                if file_ext.lower() in self.ext_list:
                    out_list.append((dirName[3:], src_parent, splitName[2], len(fileList), file_ext))
        return (sorted(out_list, key=lambda x: x[0]))


def mergeLists(src_flist: list, usb_flist: list) -> list:
    tid = 0  # tree ID used in both trees
    sl = iter(src_flist)
    ul = iter(usb_flist)
    tlist = []  # tree construction list of tuples. First entry is ID, then flag (S, U, B), then entry contents
    sl_ent = next(sl)
    ul_ent = next(ul)
    empty_ent = ("zzzzzzz", "", "", 0, "")
    while True:
        if sl_ent[0] == empty_ent[0] and ul_ent[0] == empty_ent[0]:
            return (tlist)
        if sl_ent[0] == ul_ent[0]:
            tlist.append((tid, "B", sl_ent))
            tflag = "B"
        elif sl_ent[0] < ul_ent[0]:
            tlist.append((tid, "S", sl_ent))
            tflag = "S"
        else:
            tlist.append(((tid, "U", ul_ent)))
            tflag = "U"
        if tflag in ["B", "S"]:
            try:
                sl_ent = next(sl)
            except StopIteration:
                sl_ent = empty_ent
        if tflag in ["B", "U"]:
            try:
                ul_ent = next(ul)
            except StopIteration:
                ul_ent = empty_ent
        tid = tid + 1


import wmi


def drive_label(drive: str) -> str:
    c = wmi.WMI()
    for d in c.Win32_LogicalDisk():
        if d.Caption[0].strip().lower() == drive[0].strip().lower():
            return (str(d.VolumeName).strip())


if __name__ == '__main__':
    '''
    print the list of artists / albums found.
    '''
    inDir = input("Enter the drive:/path/ to be listed.")
    print(drive_label(inDir[0]))
    f_list = FileList(inDir)
    file_list = f_list.get_list()
    for f in file_list:
        print(f)

    src_dir = input("Enter the source path to be included.")
    src_fl = FileList(src_dir)
    src_flist = src_fl.get_list()
    usb_dir = input("Enter the USB drive.")
    usb_fl = FileList(usb_dir)
    usb_flist = usb_fl.get_list()
    mrgdList = mergeLists(src_flist, usb_flist)
    for e in mrgdList:
        print(e)
