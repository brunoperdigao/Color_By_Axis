# Color By Axis - Blender Add-on

Color by Axis is a Blender add-on that allows you to check whether the edges of an object are aligned with the X, Y or Z axis, by creating a color overlay.

⚠ This add-on is still a work in progress. Currently tested on Blender 3.0 and above.

## Instalation

Download the source code as "zip" an install like any other Blender add-on.

![image](https://user-images.githubusercontent.com/57102715/161441645-727c19ab-a606-49e9-a42d-6bf2fd8510d8.png)


## How it works

The add-on will create a Panel in the N-Panel, called Color by Axis. The panel has three items:
- Color by Axis button:
  - **It only works in "Edit Mode".**
  - Activates the operator that creates the overlay.  
  - Once created, it will allow will to navigate the viewport, but will be turned off as soon as you type or click.

- Axis type option:
  - GLOBAL: Compare your object's edges with global axis.
  - LOCAL: Compare your object's edges with its local axis.
  - REFERENCE: Compare your object's edges with a selected reference object. Won't work if no object is selected.

- Reference object:
  - Select the object which will be used by the REFERENCE axis type.

## Quick example
- Add a default cube, make a copy and rotate it 30 degrees in Z axis.
- Add an empty and rotate it 30 degrees in Z axis.
- Select both cubes and enter "Edit Mode". 
- Click the button "Color by Axis" in the N-panel. The edges of the cube will be colored according to the global axis that they are parallel to.

![image](https://user-images.githubusercontent.com/57102715/161441790-e76ce8cd-2ab5-44cc-9200-bc76afcc0481.png)

---
- If "LOCAL" Axis Type is selected, it will color the edges based on the local coordinates of the objects.

![image](https://user-images.githubusercontent.com/57102715/161441804-806acddd-43f5-49c9-84ff-6a6a4b09843c.png)

---
- If "REFERENCE" Axis Type is selected, choose the empty object as reference. It will color the edges based on the local coordinates of the reference object.

![image](https://user-images.githubusercontent.com/57102715/161441840-5dac9f47-da16-4b9a-a89d-e8e7f7e0811a.png)




