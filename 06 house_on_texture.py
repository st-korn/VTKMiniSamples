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
    #plane.SetCenter(0,0,0)
    #plane.SetNormal(0,0,1)
    plane.SetOrigin(0,0,0)
    plane.SetPoint1(14,0,0)
    plane.SetPoint2(0,10,0)
    plane.SetXResolution(1)
    plane.SetYResolution(1)
    plane.Update()
    planeMapper = vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort())
    planeActor = vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetTexture(atext)
    #planeActor.RotateX(30.0)

    x=7
    y=7.29
    dx=0.2
    dy=0.05
    dz=0.1
    polydata = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    points.InsertNextPoint(x,y,0)
    points.InsertNextPoint(x+dx,y,0)
    points.InsertNextPoint(x+dx,y+dy,0)
    points.InsertNextPoint(x,y+dy,0)
    points.InsertNextPoint(x,y,dz)
    points.InsertNextPoint(x+dx,y,dz)
    points.InsertNextPoint(x+dx,y+dy,dz)
    points.InsertNextPoint(x,y+dy,dz)
    polydata.SetPoints(points)
    print(polydata.GetNumberOfPoints())

    '''generator = vtk.vtkPolyDataPointSampler()
    generator.SetInputData(polydata)
    generator.SetDistance(0.001)
    generator.GenerateVertexPointsOn()
    generator.GenerateEdgePointsOn ()
    generator.GenerateInteriorPointsOn()
    generator.GenerateVerticesOn ()
    generator.InterpolatePointDataOn ()
    generator.SetPointGenerationModeToRandom()
    #generator.SetPointGenerationModeToRegular()
    generator.Update()
    print(generator.GetOutput().GetNumberOfPoints())'''

    source = vtkSphereSource()
    source.SetRadius(0.025)
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

    '''source2 = vtkSphereSource()
    source2.SetRadius(0.02)
    glyph2 = vtkGlyph3D()
    glyph2.SetInputConnection(generator.GetOutputPort())
    glyph2.SetSourceConnection(source2.GetOutputPort())
    glyph2.ScalingOff()
    glyph2.Update()

    pointsMapper2 = vtkPolyDataMapper()
    pointsMapper2.SetInputConnection(glyph2.GetOutputPort())
    pointsActor2 = vtkActor()
    pointsActor2.SetMapper(pointsMapper2)
    pointsActor2.GetProperty().SetColor(colors.GetColor3d("Red"));'''

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(planeActor)
    ren.AddActor(pointsActor)
    #ren.AddActor(pointsActor2)
    ren.SetBackground(colors.GetColor3d("Blue"))
    renWin.SetSize(300, 300)
    renWin.SetWindowName('CylinderExample')

    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    iren.Initialize()

    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    #ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()

    # Start the event loop.
    iren.Start()


print(sys.version)
if __name__ == '__main__':
    main()