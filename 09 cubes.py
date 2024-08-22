#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import (vtkPlaneSource, vtkCubeSource)
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
    for n in range(0,19):
        for m in range(0,19):
            for y in numpy.arange(0,0.1,0.01):
                for x in numpy.arange(n*0.3+7,n*0.3+7.2,0.01):
                    for z in numpy.arange(m*0.3+2.66,m*0.3+2.71,0.01):
                        points.InsertNextPoint(x,y,z)
    polydata.SetPoints(points)

    polydata2 = vtk.vtkPolyData()
    points2 = vtk.vtkPoints()
    for n in range(0,19):
        for m in range(0,19):
            for x in numpy.arange(n*0.3+7,n*0.3+7.2,0.01):
                for z in numpy.arange(m*0.3+3.7,m*0.3+3.8,0.01):
                    points2.InsertNextPoint(x,0.01,z)
    polydata2.SetPoints(points2)

    polydata3 = vtk.vtkPolyData()
    points3 = vtk.vtkPoints()
    for n in range(0,19):
        for m in range(0,19):
            for y in numpy.arange(0,0.1,0.01):
                for x in numpy.arange(n*0.3,n*0.3+0.2,0.01):
                    for z in numpy.arange(m*0.3+2.66,m*0.3+2.71,0.01):
                        points3.InsertNextPoint(x,y,z)
    polydata3.SetPoints(points3)

    polydata4 = vtk.vtkPolyData()
    points4 = vtk.vtkPoints()
    for n in range(0,19):
        for m in range(0,19):
            for x in numpy.arange(n*0.3,n*0.3+0.2,0.01):
                for z in numpy.arange(m*0.3+3.7,m*0.3+3.8,0.01):
                    points4.InsertNextPoint(x,0.01,z)
    polydata4.SetPoints(points4)

    source = vtkCubeSource()
    source.SetXLength(0.009)
    source.SetYLength(0.009)
    source.SetZLength(0.009)
    glyph = vtkGlyph3D()
    glyph.SetInputData(polydata)
    glyph.SetSourceConnection(source.GetOutputPort())
    glyph.ScalingOff()
    glyph.Update()

    pointsMapper = vtkPolyDataMapper()
    pointsMapper.SetInputConnection(glyph.GetOutputPort())
    pointsActor = vtkActor()
    pointsActor.SetMapper(pointsMapper)
    pointsActor.GetProperty().SetColor(colors.GetColor3d("Green"));

    source2 = vtkPlaneSource()
    source2.SetOrigin(0,0,0)
    source2.SetPoint1(0.009,0,0)
    source2.SetPoint2(0,0,0.009)
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

    source3 = vtkCubeSource()
    source3.SetXLength(0.009)
    source3.SetYLength(0.009)
    source3.SetZLength(0.009)
    glyph3 = vtkGlyph3D()
    glyph3.SetInputData(polydata3)
    glyph3.SetSourceConnection(source3.GetOutputPort())
    glyph3.ScalingOff()
    glyph3.Update()

    pointsMapper3 = vtkPolyDataMapper()
    pointsMapper3.SetInputConnection(glyph3.GetOutputPort())
    pointsActor3 = vtkActor()
    pointsActor3.SetMapper(pointsMapper3)
    pointsActor3.GetProperty().SetColor(colors.GetColor3d("Red"));

    source4 = vtkPlaneSource()
    source4.SetOrigin(0,0,0)
    source4.SetPoint1(0.009,0,0)
    source4.SetPoint2(0,0,0.009)
    glyph4 = vtkGlyph3D()
    glyph4.SetInputData(polydata4)
    glyph4.SetSourceConnection(source4.GetOutputPort())
    glyph4.ScalingOff()
    glyph4.Update()

    pointsMapper4 = vtkPolyDataMapper()
    pointsMapper4.SetInputConnection(glyph4.GetOutputPort())
    pointsActor4 = vtkActor()
    pointsActor4.SetMapper(pointsMapper4)
    pointsActor4.GetProperty().SetColor(colors.GetColor3d("Red"))
    pointsActor4.GetProperty().SetOpacity(0.3)

    light = vtk.vtkLight()
    light.SetLightTypeToSceneLight()
    light.SetPosition(14/2,1,10/2)
    light.SetFocalPoint(14/2,0,10/2)
    light2 = vtk.vtkLight()
    light2.SetLightTypeToSceneLight()
    light2.SetPosition(14*3/4,1,10*3/4)
    light2.SetFocalPoint(14/2,0,10/2)
    #light2.SetIntensity(0.3)
    light3 = vtk.vtkLight()
    light3.SetLightTypeToSceneLight()
    light3.SetPosition(14/4,1,10/4)
    light3.SetFocalPoint(14/2,0,10/2)
    #light3.SetIntensity(0.3)
    #light.SetPositional(True)
    #light.SetAttenuationValues(0,0,0)
    #light.SetConeAngle(10)
    #lightActor = vtk.vtkLightActor()
    #lightActor.SetLight(light)

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(planeActor)
    ren.AddActor(pointsActor)
    ren.AddActor(pointsActor2)
    ren.AddActor(pointsActor3)
    ren.AddActor(pointsActor4)
    ren.AddLight(light)
    ren.AddLight(light2)
    ren.AddLight(light3)
    #ren.AddViewProp(lightActor)
    ren.SetBackground(colors.GetColor3d("Blue"))
    renWin.SetSize(300, 300)
    renWin.SetWindowName('CylinderExample')

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
