#!/usr/bin/env python

'''
 Renders vtk surfaces
'''
import vtk
from vtk import *
from vtk.util.misc import vtkGetDataRoot
from vtk.util.colors import *
import fileinput
import os
from os import path
import sys
from optparse import OptionParser

def main(options, args):

    # Create the graphics structure. The renderer renders into the render
    # window. The render window interactor captures mouse events and will
    # perform appropriate camera or actor manipulation depending on the
    # nature of the events.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    num_args = len(args);
    print 'number of surfaces = '+str(num_args);
    vtk_reader = [];
    mesh_mapper = [];
    mesh_actor = [];
    color_list = dir(vtk.util.colors);

    for obj in xrange(num_args):
        if eval('options.ftype_%01d.lower()'%obj) == 'polydata':
            if options.verbose:
                print 'rendering %s as surface  in color %s'%  (args[obj],color_list[6+3*obj]);
        
            vtk_reader.append( vtk.vtkPolyDataReader());
            vtk_reader[obj].SetFileName(args[obj]);

            # The mapper is responsible for pushing the geometry into the graphics
            # library. It may also do color mapping, if scalars or other
            # attributes are defined.
            mesh_mapper.append(vtk.vtkPolyDataMapper());
            mesh_mapper[obj].SetInput(vtk_reader[obj].GetOutput())

        elif eval('options.ftype_%01d.lower()'%obj) == 'unstruct':
            if options.verbose:
                print 'rendering %s as unstructured binary grid in color %s'% (args[obj],color_list[6+3*obj]);
        
            vtk_reader.append( vtk.vtkUnstructuredGridReader());
            vtk_reader[obj].SetFileName(args[obj]);
            vtk_reader[obj].Update() # Needed because of GetScalarRange
            output = vtk_reader[obj].GetOutput()
            scalar_range = output.GetScalarRange()

            # Create the mapper that corresponds the objects of the vtk file
            # into graphics elements
            mesh_mapper.append(vtkDataSetMapper())
            mesh_mapper[obj].SetInput(output)
            mesh_mapper[obj].SetScalarRange(scalar_range)
        
        # The LOD actor is a special type of actor. It will change appearance
        # in order to render faster. At the highest resolution, it renders
        # ewverything just like an actor. The middle level is a point cloud,
        # and the lowest level is a simple bounding box.
        mesh_actor.append(vtk.vtkLODActor())
        mesh_actor[obj].SetMapper(mesh_mapper[obj])
        mesh_actor[obj].GetProperty().SetColor(eval(color_list[6+3*obj]))
        mesh_actor[obj].GetProperty().SetOpacity(0.2);
        mesh_actor[obj].RotateX(30.0)
        mesh_actor[obj].RotateY(-45.0)  
            
        # Add the actors to the renderer, set the background and size
        ren.AddActor(mesh_actor[obj])
    
    ren.SetBackground(0.0, 0.0, 0.0)
    renWin.SetSize(200, 200)
    
    ## add an axis actor
    #axis_actor = vtk.vtkCubeAxesActor();
    #axis_actor = vtk.vtkAxesActor();
    #axis_actor.SetCamera(ren.GetActiveCamera());
    #axis_actor.SetBounds(0,50,0, 50,0,50);    
    #ren.AddActor(axis_actor);
    #if options.verbose:
    #    print 'axis actor placed at' + str(axis_actor.GetPosition()) \
    #            + 'with scale ' + str(axis_actor.GetScale());

    axes = vtk.vtkAxesActor();

    orientation_widget = vtk.vtkOrientationMarkerWidget();
    orientation_widget.SetOutlineColor( 0.9300, 0.5700, 0.1300 );
    orientation_widget.SetOrientationMarker( axes );
    orientation_widget.SetInteractor( iren );
    orientation_widget.SetViewport( 0.0, 0.0, 0.4, 0.4 );
    orientation_widget.SetEnabled( 1 );
    orientation_widget.InteractiveOff();
    if options.verbose:
        print 'axis actor placed at' + str(axes.GetPosition()) \
                + 'with scale ' + str(axes.GetScale());


    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)



    # This starts the event loop.
    iren.Initialize()
    renWin.Render()
    iren.Start()

   
     

if __name__ == "__main__":
    usage = \
''' %prog [options] filename.vtk 
    Plot vtk files'''
    
    option_parser = OptionParser(usage)
    option_parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True) 
    option_parser.add_option("-0", "--filetype_0=[polydata, unstruct]", dest="ftype_0", default="polydata")
    option_parser.add_option("-1", "--filetype_1=[polydata, unstruct]", dest="ftype_1", default="polydata")
    option_parser.add_option("-2", "--filetype_2=[polydata, unstruct]", dest="ftype_2", default="polydata")
    
    (options, args) = option_parser.parse_args()
    
    if len(args) < 1:
        option_parser.print_help()
        sys.exit();

    main(options, args);
