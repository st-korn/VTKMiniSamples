#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.

import vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import sys


def main():
    colors = vtkNamedColors()
 
    points = vtkPoints()
    points.InsertNextPoint([0,0,0])
    points.InsertNextPoint([1,0,0])
    points.InsertNextPoint([2,-1,0])
    points.InsertNextPoint([3,0,0])
    points.InsertNextPoint([4,0,0])

    points.InsertNextPoint([0,0,1])
    points.InsertNextPoint([1,0,1])
    points.InsertNextPoint([2,-0.5,1])
    points.InsertNextPoint([3,0,1])
    points.InsertNextPoint([4,0,1])
 
    points.InsertNextPoint([0,0,2])
    points.InsertNextPoint([1,0,2])
    points.InsertNextPoint([2,0,2])
    points.InsertNextPoint([3,0,2])
    points.InsertNextPoint([4,0,2])
 
    points.InsertNextPoint([0,0,3])
    points.InsertNextPoint([1,0,3])
    points.InsertNextPoint([2,0,3])
    points.InsertNextPoint([3,0,3])
    points.InsertNextPoint([4,0,3])
 
    points.InsertNextPoint([0,0,4])
    points.InsertNextPoint([1,0,4])
    points.InsertNextPoint([2,0,4])
    points.InsertNextPoint([3,0,4])
    points.InsertNextPoint([4,0,4])
 
    polyData = vtkPolyData()
    polyData.SetPoints(points)
 
    (xmin,xmax,ymin,ymax,zmin,zmax) = polyData.GetBounds()
    rangex = xmax-xmin
    rangey = ymax-ymin
    rangez = zmax-zmin

    normals = vtk.vtkPCANormalEstimation()
    normals.SetInputData(polyData)
    normals.SetSampleSize(10)
    normals.SetNormalOrientationToGraphTraversal()
    normals.FlipNormalsOn()
    distance = vtk.vtkSignedDistance()
    distance.SetInputConnection(normals.GetOutputPort())
    distance.SetRadius(2)
    distance.SetDimensions(256,256,256)
    distance.SetBounds(-0.5,4.5,-1.5,0.5,-0.5,4.5)
    surface = vtk.vtkExtractSurface()
    surface.SetInputConnection(distance.GetOutputPort())
    surface.SetRadius(2)
    surface.Update()
    
    arrow= vtk.vtkArrowSource()
    glypha = vtk.vtkGlyph3D()
    glypha.SetInputConnection(normals.GetOutputPort())
    glypha.SetSourceConnection(arrow.GetOutputPort())
    glypha.SetVectorModeToUseNormal()
    glypha.SetScaleModeToScaleByVector()
    glypha.SetScaleFactor(1)
    mappera = vtk.vtkPolyDataMapper()
    mappera.SetInputConnection(glypha.GetOutputPort())
    actora = vtk.vtkActor()
    actora.SetMapper(mappera)
    actora.GetProperty().SetColor(1, 0, 0)

    source = vtkSphereSource()
    source.SetRadius(0.025)
    glyph = vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(source.GetOutputPort())
    glyph.ScalingOff()
    glyph.Update()
    pointsMapper = vtkPolyDataMapper()
    pointsMapper.SetInputConnection(glyph.GetOutputPort())
    pointsActor = vtkActor()
    pointsActor.SetMapper(pointsMapper)
    pointsActor.GetProperty().SetColor(colors.GetColor3d("Banana"));


    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Green"))

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(pointsActor)
    ren.AddActor(actora)
    ren.AddActor(actor)
    ren.SetBackground(colors.GetColor3d("Blue"))
    renWin.SetSize(300, 300)

    iren.Initialize()

    ren.ResetCamera()
    renWin.Render()

    iren.SetInteractorStyle(vtk.vtkInteractorStyleTerrain())
    iren.Start()


print(sys.version)
if __name__ == '__main__':
    main()