import Blender
from Blender import NMesh
from Blender import Object
from Blender import Scene
from Blender import *

import sys as s
s.path.append(".")

from Constants import *

print "opening: " + s.argv[3]
testFile = open(s.argv[3], 'r')
spSize = float(testFile.readline())

z = float(2)

scene = Scene.GetCurrent()

for o in scene.objects:
	scene.objects.unlink(o)

nameTag = 0

def isnumeric(value):
	copy = value;
  	return str(copy).replace(".", "").replace("-", "").isdigit()

for line in testFile:

	i,j,level,neighbors = line.split()

	if(isnumeric(i)):
	
		i = float(i)
		j = float(j)
		level = int(level)
	
		nameTag = nameTag + 1	

		name = "myMesh" + str(nameTag)
	
		#me = NMesh.GetRaw()
		me = NMesh.New(name)
	
		v0=NMesh.Vert(i,j,z*level)
		v1=NMesh.Vert(i+spSize,j,z*level)
		v2=NMesh.Vert(i+spSize,j,0.0)
		v3=NMesh.Vert(i,j,0.0)
		v4=NMesh.Vert(i,j+spSize,0.0)
		v5=NMesh.Vert(i,j+spSize,z*level)
		v6=NMesh.Vert(i+spSize,j+spSize,z*level)
		v7=NMesh.Vert(i+spSize,j+spSize,0.0)
	
		me.verts.append(v0)
		me.verts.append(v1)
		me.verts.append(v2)
		me.verts.append(v3)
		me.verts.append(v4)
		me.verts.append(v5)
		me.verts.append(v6)
		me.verts.append(v7)
		
		fA=NMesh.Face()
		fB=NMesh.Face()
		fC=NMesh.Face()
		fD=NMesh.Face()
		fE=NMesh.Face()
		fF=NMesh.Face()
	
		fA.v.append(me.verts[0])
		fA.v.append(me.verts[1])
		fA.v.append(me.verts[6])
		fA.v.append(me.verts[5])	
		me.faces.append(fA)
	
		fC.v.append(me.verts[3])
		fC.v.append(me.verts[2])
		fC.v.append(me.verts[7])
		fC.v.append(me.verts[4])
		me.faces.append(fC)
	
		if (neighbors[0] == '1'):
			fE.v.append(me.verts[4])
			fE.v.append(me.verts[5])
			fE.v.append(me.verts[6])
			fE.v.append(me.verts[7])	
			me.faces.append(fE)
	
		if (neighbors[1] == '2'):
			fB.v.append(me.verts[1])
			fB.v.append(me.verts[2])
			fB.v.append(me.verts[7])
			fB.v.append(me.verts[6])
			me.faces.append(fB)			
		
		if (neighbors[2] == '3'):
			fF.v.append(me.verts[0])
			fF.v.append(me.verts[1])
			fF.v.append(me.verts[2])
			fF.v.append(me.verts[3])
			me.faces.append(fF)
		
		if (neighbors[3] == '4'):
			fD.v.append(me.verts[4])
			fD.v.append(me.verts[5])
			fD.v.append(me.verts[0])
			fD.v.append(me.verts[3])
			me.faces.append(fD)

		ob = Object.New("Mesh", name)
		ob.link(me)
		scene.objects.link(ob)

	else:
		shape, i, j, radius = line.split()
		
		i = float(i)
		j = float(j)
		#height,radius = heightradius.split('/')
		height = 2
		diameter = float(radius) * 2

		if shape == 'sphere':

			sphere = Mesh.New("sphere")
			sphere = Mesh.Primitives.UVsphere(32,32,diameter)
		
			cube = Mesh.New("sphere")
			cube = Mesh.Primitives.Cube(diameter)

			sphereObject = Object.New("Mesh")
			sphereObject.link(sphere)

			cubeObject = Object.New("Mesh")
			cubeObject.link(cube)

			scene.objects.link(sphereObject)
			scene.objects.link(cubeObject)

			#TODO: FIX THIS
			sphereObject.setLocation(i,j,(z*height))
			cubeObject.setLocation(i,j,(z*height)-(diameter/2))

			mod = sphereObject.modifiers.append(Blender.Modifier.Type.BOOLEAN)
			mod[Modifier.Settings.OBJECT] = cubeObject
			mod[Modifier.Settings.OPERATION] = 2
	
			sphereObject.makeDisplayList()
	
			Window.RedrawAll()

			#TODO: FIX THIS
			scene.objects.unlink(cubeObject)
			#sphereObject.unlink(sphere)

			Window.RedrawAll()
			
		elif shape == 'cone':
			cone = Mesh.New("cone")
			# TODO: allow user to input height instead of reusing diameter
			cone = Mesh.Primitives.Cone(32, diameter, -diameter)
			
			coneObject = Object.New("Mesh")
			coneObject.link(cone)
			
			scene.objects.link(coneObject)

			#TODO: FIX THIS
			coneObject.setLocation(i,j,z*height+(diameter/2))
			
			Window.RedrawAll()
		
		elif shape == 'cylinder':
			cylinder = Mesh.New("cylinder")
			# TODO: allow user to input height instead of reusing diameter
			cylinder = Mesh.Primitives.Cylinder(32, diameter, -diameter)
			
			cylinderObject = Object.New("Mesh")
			cylinderObject.link(cylinder)
			
			scene.objects.link(cylinderObject)
			
			#TODO: FIX THIS
			cylinderObject.setLocation(i,j,z*height+(diameter/2))
			
			Window.RedrawAll()

Blender.Redraw()

for o in scene.objects:
	o.sel = 1

selectedObjects = Blender.Object.GetSelected()

print "Blender: Fusing elements of world domination..."

#ob.join(scene.objects)

testFile.close()

print "Blender: Saving the world..."

Blender.Save(BLENDER_OUT, 1)

#Blender.Quit()
