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
from vtkmodules.vtkIOImage import vtkImageReader2Factory
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
    points.InsertNextPoint([2,-0.5,0])
    points.InsertNextPoint([3,0,0])
    points.InsertNextPoint([4,0,0])

    points.InsertNextPoint([0,0,1])
    points.InsertNextPoint([1,0,1])
    points.InsertNextPoint([2,-0.25,1])
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

    surface = vtk.vtkSurfaceReconstructionFilter()
    surface.SetNeighborhoodSize(2)
    surface.SetSampleSpacing(2)
    surface.SetInputData(polyData)
    cf = vtk.vtkContourFilter()
    cf.SetInputConnection(surface.GetOutputPort())
    cf.SetValue(0, 0.0)
    reverse = vtk.vtkReverseSense()
    reverse.SetInputConnection(cf.GetOutputPort())
    reverse.ReverseCellsOn()
    reverse.ReverseNormalsOn()


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
    mapper.SetInputConnection(reverse.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Green"))

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(pointsActor)
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