import vtk
import numpy
from vtk.util import numpy_support
from vtk.numpy_interface import dataset_adapter as dsa

dimensions = (30,30,30)
spacing = (1,1,1)
origin = (0,0,0)

test_arr = numpy.random.random(dimensions)
data = numpy_support.numpy_to_vtk ( num_array=test_arr.flatten(), deep=True, array_type=vtk.VTK_FLOAT )

voxel = vtk.vtkImageData()
voxel.SetDimensions(dimensions)
voxel.SetOrigin(origin)
voxel.SetSpacing(spacing)
voxel.GetPointData().SetScalars(data)

voxelMapper = vtk.vtkDataSetMapper()
voxelMapper.SetInputData(voxel)

voxelActor = vtk.vtkActor()
voxelActor.SetMapper(voxelMapper)
voxelActor.GetProperty().SetOpacity(0.5)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(voxelActor)

camera = ren.GetActiveCamera()
camera.SetClippingRange(20,100)
camera.SetFocalPoint(12,12,12)
camera.SetPosition(-12,-12,-12)

renWin.SetSize(640,480)
renWin.Render()
iren.Initialize()
iren.Start()