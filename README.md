# CS447P_Final_Project_R_H
## Coding Language
### Python
## Python Packages
### PyOpenGL
### PyGame
## Other Tools
### Blender
---
# Topic: An Amusement Park
## Due: 5PM 12/06 at the latest
## The Basic Task
### This project will provide you with experience at modeling objects for computer graphics, and introduce you to many more of the features of OpenGL. The starting point is a small virtual space that consists of a grassy square with a roller-coaster track running around it. A carriage (a box for now) runs around the track. Your task is to model and render the carriages and other objects in the environment.
### This project defines a set of sub-goals with points awarded for each goal.
## The Tasks
### Each task requires modeling one or more objects using a specific technique from class. The points available for each technique varies according to the difficulty of the task. In all cases, you get a base number of points for implementing one object with a technique.
- For undergraduate students, you can get an extra 5 points for each additional, but distinct, object with the same technique. You can score points for a maximum of three objects with any one technique. For instance, if you create a texture mapped polygonal ticket booth and a texture-mapped polygonal roller-coaster carriage, you get 20 + 5 = 25 points.
- For graduate students, you can only get the base number of points.
### If an object involves more than one thing, such as a texture mapped, swept surface, then you can score points for both texture mapping and sweep objects.
### The maximum number of points is 100. You can do as much as you like, and we will truncate to 100 as the final step in computing the grade.
## The individual tasks, point value, and example objects are:

| Technique | Requirements | Base Points | Suggestions |
| :-------- | :----------- | :---------- | :---------- |
| Texture Mapping | Add texture mapped polygonal objects to the environment. Each "object" for grading purposes consists of at least 5 polygons all texture mapped. Different objects require different maps. | 20 | Buildings, walls, roadways |
| Hierarchical Animated Model | Add a hierarchical, animated model. The model must combine multiple components in a transformation hierarchy. Different models need different hierarchies. | 25 | Ferris Wheel, any number of other fairground rides. |
| Parametric Instancing | Add an object described by parameters. You must create multiple instances with different parameters, and each class of model counts for separate points, not each instance. | 20 | Trees (cones on sticks), buildings, even rides |
| Sweep Objects | Add an object created as a sweep, either an extrusion or a surface of revolution. The important thing is that it be created by moving some basic shape along a path. The overall object must use at least three different uses of the swept polygon. In other words, something like a cylinder isn't enough, but something like two cylinders joined to form an elbow is.| 25 | Rails for the roller-coaster, trash bins, trees |
| Subdivision | An object defined using subdivision schemes. You must include a key press that refines the model, so that we can see the improved quality. The sphere example from class can help, somewhat, with this. You can either implement the ones we talk about in our class, or any others. | 50 | The roller-coaster car, organic looking roofs, ... |
| Change the Navigation System | The navigation system now is not great. Change it to something better. To get the points in this category, you must have a mode where the viewer rides the roller-coaster.| 20 | Ride the roller coaster, hotkeys to jump to specific views (good for demos), many possibilities. |
| Modeling using software | You can use software like Blender  or Maya to model complex objects. Based on the complexity and aesthetics of the objects, you can get extra points ranging from 10~20. (Blender is free and Maya is not.) | 10~20 | |
| Aesthetics | You can get extra points ranging from 0 to 15 based on the aesthetics of your design. It is subjective; however, we will make grading as fair as possible. | 0~15 | |
## Current Controls
| Key | Function |
| :---: | :------ |
| W | Move Forward |
| S | Move Backward |
| A | Move Left|
| D | Move Right |
| J | Move Up|
| K | Move Down |
| R | Hold to Trigger Auto-Rotation |
| Up Arrow | Rotate Up|
| Down Arrow | Rotate Down|
| Left Arrow | Rotate Left|
| Right Arrow | Rotate Right|
| Spacebar | Reset to Initial Coordinates|
| Escape | Leave |
## Managing Repo
### To Update Changes: 
#### git pull
### To Push Changes: 
#### git add . 
#### git commit -m "Message"
#### git push
# Eval before grading
## Texture Mapping
### Check Walls, Corners, entrance, exit, ride and roller coaster car
## Hierarchical animated model
### if we can get ferris wheel to work, check that
## parametric instancing
### check trees and walls
## Sweep Objects
### Check archway and possibly when Ryan puts it in, elbow statues
## Subdivision
### Still need to do
## Change the Navigation System
### Still need to do
## Modeling Using Software
### Check everything except platform
## Aesthetics
### Medieval???