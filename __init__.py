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
from .color_by_axis import CBA_OT_Color_by_Axis
from .ui import CBA_PT_Main_Panel

classes = (
    CBA_OT_Color_by_Axis,
    CBA_PT_Main_Panel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    items = [
    ("GLOBAL", "Global", "", 1),
    ("LOCAL", "Local", "", 2),
    ("REFERENCE", "Reference", "", 3)
    ]

    bpy.types.Scene.axis_type = bpy.props.EnumProperty(items=items, name="Axis type", description="Choose axis type that will affect the overlay")
    
    

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.axis_type

if __name__ == "__main__":
    register()