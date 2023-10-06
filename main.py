# USBsync application manages creating a list of music to copy from a master to the selected USB drive

# Import the os module, for the os.walk function
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkscrolledframe import ScrolledFrame
from tkinter import messagebox

import filelist as fl


class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''

    def __init__(self, root, widget, text='widget info'):
        self.widget = widget
        self.root = root
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() - 30
        # creates a toplevel window
        self.tw = tk.Toplevel(self.root)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        tk.Label(self.tw, text=self.text, justify='left',
                 background='yellow', relief='solid', borderwidth=1,
                 font=("times", "10", "normal")).pack()

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


# sizes of widgets
WINDOW_WIDTH = 977
WINDOW_HEIGHT = 703
MENUBAR_WIDTH = 786
MENUBAR_HEIGHT = 32
PLAYLIST_WIDTH = 427
PLAYLIST_HEIGHT = 40
FILETYPE_WIDTH = 179
FILETYPE_HEIGHT = 40
SRCFRAME_WIDTH = 427
SRCFRAME_HEIGHT = 501
SRCTREE_WIDTH = 427
SRCTREE_HEIGHT = 530
USBFRAME_WIDTH = 427
USBFRAME_HEIGHT = 501
USBTREE_WIDTH = 427
USBTREE_HEIGHT = 530

tkroot = tk.Tk()
tkroot.title("Copy Music to USB Drive")
tkroot.geometry("977x703")

tkroot.rowconfigure(0, weight=1)
tkroot.columnconfigure(0, weight=1)
# Fetch the source music files
src_dir = filedialog.askdirectory(title='Select source directory.',
                                  initialdir='MyComputer', parent=tkroot)
src_fl = fl.FileList(src_dir)
# tk.messagebox.showinfo(title='Loading Source Drive information', message=f"Source Drive: {src_fl.drive_name}")
src_flist = src_fl.get_list()
# Fetch the USB drive files
usb_dir = filedialog.askdirectory(title='Select USB Destination.',
                                  initialdir='MyComputer', parent=tkroot)
usb_fl = fl.FileList(src_dir)
usb_flist = usb_fl.get_list()
# merge the two lists and set up the id to be used in the two trees
mrgd_flist = fl.mergeLists(src_flist, usb_flist)
# Create the source tree
src_tree_frame = ScrolledFrame(tkroot, width=SRCTREE_WIDTH, height=SRCTREE_HEIGHT)
src_tree_frame.bind_arrow_keys(tkroot)
src_tree_frame.bind_scroll_wheel(tkroot)
src_tree_frame.grid()
src_tree = ttk.Treeview(src_tree_frame)
src_tree.heading('#0', text=src_dir)

# Set the directory you want to start from
rootDir = src_dir
for f in mrgd_flist:
    if f[2][2] == '':
        src_parent = src_tree.insert('', tk.END, iid=str(f[0]), text=f[2][1], open=True)
    else:
        src_tree.insert(src_parent, tk.END, iid=str(f[0]), text=f[2][2], open=False)

src_tree.grid(row=0, column=0, sticky=tk.NSEW)

tkroot.mainloop()
