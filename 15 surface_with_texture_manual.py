#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersSources import (vtkPlaneSource, vtkSphereSource)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkIOImage import vtkImageReader2Factory
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkCamera,
    vtkTexture
)
import sys
import numpy

def main():
    colors = vtkNamedColors()

    fileName = 'squares.jpg'
    readerFactory = vtkImageReader2Factory()
    textureFile = readerFactory.CreateImageReader2(fileName)
    textureFile.SetFileName(fileName)
    textureFile.Update()

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
    reverse.Update()

    polyData = reverse.GetOutput()
    
    src_ar = polyData.GetPoints()
    dst_ar = vtk.vtkFloatArray()
    dst_ar.SetNumberOfComponents(2)
    for i in range(src_ar.GetNumberOfPoints()):
        pnt = src_ar.GetPoint(i)
        print(pnt)
        #if pnt[0]<0 or pnt[0]>4:
        #    continue
        #if pnt[2]<0 or pnt[2]>4:
        #    continue
        dst_ar.InsertNextTuple2(pnt[0]/4,pnt[2]/4)
        print("=",pnt[0]/4,pnt[2]/4)
    polyData.GetPointData().SetTCoords(dst_ar)

    atext = vtkTexture()
    atext.SetInputConnection(textureFile.GetOutputPort())
    atext.InterpolateOn()

    planeMapper = vtkPolyDataMapper()
    planeMapper.SetInputData(polyData)
    planeMapper.ScalarVisibilityOff()
    planeActor = vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetTexture(atext)

    source = vtkSphereSource()
    source.SetRadius(0.05)
    glyph = vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(source.GetOutputPort())
    glyph.ScalingOff()
    glyph.Update()

    pointsMapper = vtkPolyDataMapper()
    pointsMapper.SetInputConnection(glyph.GetOutputPort())
    pointsActor = vtkActor()
    pointsActor.SetMapper(pointsMapper)
    pointsActor.GetProperty().SetColor(colors.GetColor3d("Green"));


    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(planeActor)
    ren.AddActor(pointsActor)
    ren.SetBackground(colors.GetColor3d("Blue"))

    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()

    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Elevation(45)
    #ren.GetActiveCamera().Yaw(180)
    #ren.GetActiveCamera().Azimuth(180)
    renWin.Render()

    # Start the event loop.
    #iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTerrain())
    #iren.SetInteractorStyle(vtk.vtkInteractorStyleMultiTouchCamera())
    iren.Start()


print(sys.version)
if __name__ == '__main__':
    main()
