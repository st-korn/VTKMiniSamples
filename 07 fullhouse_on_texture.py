#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import (vtkPlaneSource, vtkSphereSource)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkIOImage import vtkImageReader2Factory
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture
)
import sys
import numpy

def main():
    colors = vtkNamedColors()

    # Load in the texture map. A texture is any unsigned char image. If it
    # is not of this type, you will have to map it through a lookup table
    # or by using vtkImageShiftScale.
    #
    fileName = 'texture.png'
    readerFactory = vtkImageReader2Factory()
    textureFile = readerFactory.CreateImageReader2(fileName)
    textureFile.SetFileName(fileName)
    textureFile.Update()
    atext = vtkTexture()
    atext.SetInputConnection(textureFile.GetOutputPort())
    atext.InterpolateOn()

    # This creates a polygonal cylinder model with eight circumferential
    # facets.
    plane = vtkPlaneSource()
    plane.SetOrigin(0,0,10)
    plane.SetPoint1(14,0,10)
    plane.SetPoint2(0,0,0)
    plane.SetXResolution(1)
    plane.SetYResolution(1)
    plane.Update()
    planeMapper = vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort())
    planeActor = vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetTexture(atext)

    polydata = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    for y in numpy.arange(0,0.1,0.01):
        for x in numpy.arange(7,7.2,0.01):
            for z in numpy.arange(2.66,2.71,0.01):
                points.InsertNextPoint(x,y,z)
    polydata.SetPoints(points)

    polydata2 = vtk.vtkPolyData()
    points2 = vtk.vtkPoints()
    for x in numpy.arange(7,7.2,0.01):
        for z in numpy.arange(3.7,3.8,0.01):
            points2.InsertNextPoint(x,0.01,z)
    polydata2.SetPoints(points2)

    source = vtkSphereSource()
    source.SetRadius(0.005)
    glyph = vtkGlyph3D()
    glyph.SetInputData(polydata)
    glyph.SetSourceConnection(source.GetOutputPort())
    glyph.ScalingOff()
    glyph.Update()

    pointsMapper = vtkPolyDataMapper()
    pointsMapper.SetInputConnection(glyph.GetOutputPort())
    pointsActor = vtkActor()
    pointsActor.SetMapper(pointsMapper)
    pointsActor.GetProperty().SetColor(colors.GetColor3d("Banana"));

    source2 = vtkPlaneSource()
    source2.SetOrigin(0,0,0)
    source2.SetPoint1(0.01,0,0)
    source2.SetPoint2(0,0.01,0)
    #source2.SetRadius(0.02)
    glyph2 = vtkGlyph3D()
    glyph2.SetInputData(polydata2)
    glyph2.SetSourceConnection(source2.GetOutputPort())
    glyph2.ScalingOff()
    glyph2.Update()

    pointsMapper2 = vtkPolyDataMapper()
    pointsMapper2.SetInputConnection(glyph2.GetOutputPort())
    pointsActor2 = vtkActor()
    pointsActor2.SetMapper(pointsMapper2)
    pointsActor2.GetProperty().SetColor(colors.GetColor3d("Green"))
    pointsActor2.GetProperty().SetOpacity(0.3)

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(planeActor)
    ren.AddActor(pointsActor)
    ren.AddActor(pointsActor2)
    ren.SetBackground(colors.GetColor3d("Blue"))
    renWin.SetSize(300, 300)
    renWin.SetWindowName('CylinderExample')
    #renWin.SetInter

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
    
    iren.Start()


print(sys.version)
if __name__ == '__main__':
    main()