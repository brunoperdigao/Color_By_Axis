# Color By Axis - Blender Add-on

Color by Axis is a Blender add-on that allows you to check whether the edges of an object are aligned with the X, Y or Z axis, by creating a color overlay.

⚠ This add-on is still a work in progress. Currently tested on Blender 3.0 and above.

## Instalation

Download the source code as "zip" and install it like any other Blender add-on.

![image](https://user-images.githubusercontent.com/57102715/161441645-727c19ab-a606-49e9-a42d-6bf2fd8510d8.png)


## How it works

The add-on will create a Panel in the N-Panel, called Color by Axis. Here is an explanation about the main items:
- Color by Axis checkbox:
  - Activates the overlay over any selected object.  
  - Once created, it will allow will to navigate the viewport, but will be turned off as soon as you type or click.

- Axis type option:
  - GLOBAL: Compare your object's edges with global axis.
  - LOCAL: Compare your object's edges with its local axis.
  - REFERENCE: Compare your object's edges with a selected reference object. If no reference is provided it will work as LOCAL.

- Reference object:
  - Select the object which will be used by the REFERENCE axis type.

**Note**: the colors of the overlay are attached to Blender's default theme, for consistency. If you want to change this, you have to change `preference > themes > user interface > axis & gizmos colors > Axis x, y, z`


## Quick example
- Add a default cube, make a copy and rotate it 30 degrees in Z axis.
- Add an empty and rotate it 30 degrees in Z axis.
- Select both cubes and enter "Edit Mode". 
- Click the checkbox "Color by Axis" in the N-panel. The edges of the cube will be colored according to the global axis that they are parallel to.

![image](https://user-images.githubusercontent.com/57102715/172069203-bb65f4c0-7cab-491c-81fe-6d5c83047d97.png#vtrinedev)

---
- If "LOCAL" Axis Type is selected, it will color the edges based on the local coordinates of the objects.

![image](https://user-images.githubusercontent.com/57102715/172069210-11403a4f-d245-474a-9e1a-27f5a51b2db9.png)

---
- If "REFERENCE" Axis Type is selected, choose the empty object as reference. It will color the edges based on the local coordinates of the reference object.

![image](https://user-images.githubusercontent.com/57102715/172069225-52725791-0879-4b5b-a027-f78b39ff914d.png)





