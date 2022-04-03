bl_info = {
    "name": "Line Strips",
    "author": "",
    "description": "",
    "blender": (2, 80, 0),
    "location": "",
    "warning": "",
    "category": ""
}

import bpy
from .color_by_axis import OT_color_by_axis

def register():
    bpy.utils.register_class(OT_color_by_axis)

def unregister():
    bpy.utils.unregister_class(OT_color_by_axis) 

if __name__ == "__main__":
    register()