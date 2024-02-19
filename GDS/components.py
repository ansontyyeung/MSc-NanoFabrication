from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.spiral import Spiral
from gdshelpers.parts.splitter import DirectionalCoupler
from gdshelpers.parts.text import Text

from parameters import *

# Do not delete or change!
# TODO: Find a less hacky fix SC
CORNERSTONE_GRATING_IDENTIFIER = 0

class CornerstoneGratingCoupler:
    """Class for linear grating coupler design
    compliant with Cornerstone fab.
    SC/QP 12/01/22"""

    def __init__(self):
        """
        :param origin: Position of the instance of the class
        :param coupler_params: Coupler parameters for this instance
        """
        self.coupler_params = None
        self.origin = None
        self.port = None
        self.cell = None

    def create_coupler(self, origin, coupler_params, name=None):
        """
        Function to create the Cornerstone compliant grating cell.
        """
        GC_proto = GratingCoupler.make_traditional_coupler(origin=origin,
                                                           extra_triangle_layer=False,
                                                           **coupler_params)
        GC_proto_shape_obj = GC_proto.get_shapely_object()
        GC_outline = GC_proto_shape_obj.convex_hull
        GC_teeth = GratingCoupler.make_traditional_coupler(origin=origin,
                                                           extra_triangle_layer=True,
                                                           **teeth_coupler_parameters)
        global CORNERSTONE_GRATING_IDENTIFIER
        cell = Cell("GC_period_{}_coords_{}_{}_{}".format(coupler_params['grating_period'],
                                                          origin[0],
                                                          origin[1], CORNERSTONE_GRATING_IDENTIFIER))
        CORNERSTONE_GRATING_IDENTIFIER += 1

        # add outline to draw layer
        cell.add_to_layer(WAVEGUIDE_LAYER, GC_outline)
        cell.add_to_layer(GRATING_LAYER, GC_teeth)

        self.cell = cell
        self.port = GC_proto.port

        return self

    @classmethod
    def create_cornerstone_coupler_at_port(self, port, **kwargs):
        """
        SC 20/01/22
        Make a grating coupler at a port.

        This function is identical to :func:`create_coupler`. Parameters of the port
        can also be overwritten via keyword arguments.

        :param port: The port at which the coupler shall be created.
        :type port: Port
        :param kwargs: Keyword arguments passed to :func:`make_traditional_coupler`.
        :return: The constructed traditional grating coupler.
        :rtype: GratingCoupler
        """

        if 'width' not in kwargs:
            kwargs['width'] = port.width

        if 'angle' not in kwargs:
            kwargs['angle'] = port.angle

        coup_params = kwargs

        return self.create_coupler(self,
                                   origin=port.origin,
                                   coupler_params=coup_params)


def grating_checker(gratings):
    """
    Utility function which checks that grating couplers are
    appropriately placed. SC 20/01/22.
    :param gratings: List of all the gratings in the device
    :return: x_diff, y_diff so these can be used to adjust position of gratings
    """

    y_diff = np.around(gratings[0].port.origin[1], 9) - np.around(gratings[1].port.origin[1], 9)
    x_diff = np.around(gratings[0].port.origin[0], 9) - np.around(gratings[1].port.origin[0], 9)

    if y_diff != 0:
        print(" \n \n WARNING: The gratings being checked have a y separation of {}  \n \n ".format(y_diff))
    if (np.abs(x_diff) % GRATING_PITCH) !=0:
        print(" \n \n WARNING: The gratings being checked have a x separation of {}. Recommended is {} \n \n "
              .format(np.abs(x_diff), GRATING_PITCH))

    return x_diff, y_diff


def grating_coupler(coupler_parameters, position=(0, 0), name='grating_coupler'):
    """
    Function which returns a cell containing
    two connected gratings.
    :param position: x,y coordinates of loopback - leave as (0,0), overwritten by layout
    :param coupler_params: dict of specs for coupler
    :param name: String which uniquely identifies the cell
    :return: Cell containing the loopback
    """

    # Create the cell that we are going to add to
    grating_coupler_cell = Cell(name)

    # Create Text
    grating_coupler_cell.add_to_layer(LABEL_LAYER,
                                     Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,angle=LABEL_ANGLE_VERTICAL,
                                          text=name)
                                      )

    # Create the left hand side grating
    left_grating = CornerstoneGratingCoupler().create_coupler(
        origin=(position[0], position[1]),
        coupler_params=coupler_parameters)

    # Add the left grating coupler cell to our loopback cell
    grating_coupler_cell.add_cell(left_grating.cell)

    # Join our grating couplers together
    wg = Waveguide.make_at_port(port=left_grating.port)  # Create waveguide at the left grating port location
    wg.add_straight_segment(length=10)  # Do some routing
    wg.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg.add_straight_segment(length=GRATING_PITCH - 2 * BEND_RADIUS + 19)
    wg.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg.add_straight_segment(length=10)
    grating_coupler_cell.add_to_layer(WAVEGUIDE_LAYER, wg)  # Add the waveguide to the loopback cell

    # Create the right grating coupler at the waveguide port location
    right_grating = CornerstoneGratingCoupler().create_cornerstone_coupler_at_port(
        port=wg.current_port,
        **coupler_parameters)
    # Add the right grating to the loopback cell
    grating_coupler_cell.add_cell(right_grating.cell)

    # Grating checker
    grating_checker([left_grating, right_grating])

    return grating_coupler_cell


def spiral_winding(coupler_parameters, number, gap_size, inner_gap_size, position=(0,0), name='SPIRAL'):
    # Create the cell
    spiral_winding_cell = Cell(name)

    # Create Text
    spiral_winding_cell.add_to_layer(LABEL_LAYER,
                                     Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,angle=LABEL_ANGLE_VERTICAL,
                                          text=name+'\nNo_loops_'+str(number)+'\nGapbetween_waveguides_'+str(gap_size)+
                                          '\nInner_circle_radius_'+str(inner_gap_size))
                                     )

    # Create the left hand side grating
    left_grating = CornerstoneGratingCoupler().create_coupler(origin=(position[0], position[1]),
                                                              coupler_params=coupler_parameters)

    # Add waveguide
    wg1 = Waveguide.make_at_port(port=left_grating.port)
    wg1.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg1.add_bend(angle=pi / 2, radius=BEND_RADIUS)

    # Add the spiral
    spiral = Spiral.make_at_port(port=wg1.current_port, num=number, gap=gap_size, inner_gap=inner_gap_size)
    spiral_length = spiral.length
    spiral_obj = spiral.get_shapely_object()
    spiral_size = abs(spiral_obj.bounds[1] - spiral_obj.bounds[3])

    # Add waveguide at output
    wg2 = Waveguide.make_at_port(port=spiral.out_port)
    wg2.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg2.add_bend(angle=-pi, radius=BEND_RADIUS)

    # Routing to the next multiple of 127
    for j in range(VGA_NUM_CHANNELS):
        if (spiral_size/2) < j * GRATING_PITCH:
            wg2.add_straight_segment(length=j*GRATING_PITCH+GRATING_TAPER_ROUTE)
            break

    # Add right hand bend
    wg2.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg2.add_straight_segment(length=GRATING_TAPER_ROUTE+spiral_size+2*BEND_RADIUS-WAVEGUIDE_WIDTH)

    # Create right grating coupler
    right_grating = CornerstoneGratingCoupler().create_cornerstone_coupler_at_port(port=wg2.current_port,
                                                                                   **coupler_parameters, angle=wg2.angle)

    spiral_winding_cell.add_cell(left_grating.cell)
    spiral_winding_cell.add_cell(right_grating.cell)
    spiral_winding_cell.add_to_layer(WAVEGUIDE_LAYER, wg1)
    spiral_winding_cell.add_to_layer(WAVEGUIDE_LAYER, wg2)
    spiral_winding_cell.add_to_layer(WAVEGUIDE_LAYER, spiral)

    # Grating checker
    # grating_checker([left_grating, right_grating])

    return spiral_winding_cell



def asymmetric_spiral_mzi(coupler_parameters, coupling_length, coupling_gap, upper_spiral_no, lower_spiral_no, spiral_gap,
                          spiral_inner_gap, position=(0,0), name='ASYMMETRIC SPIRAL-ARM MZI'):

    # Create the cell
    asymmetric_spiral_mzi_cell = Cell(name)

    # Create the first left hand side grating
    left_grating1 = CornerstoneGratingCoupler().create_coupler(origin=(position[0], position[1]),
                                                              coupler_params=coupler_parameters)

    # Create the second left hand side grating
    left_grating2 = CornerstoneGratingCoupler().create_coupler(origin=(GRATING_PITCH, position[1]),
                                                              coupler_params=coupler_parameters)

    # Route the second left-hand grating coupler to DC
    wg2 = Waveguide.make_at_port(port=left_grating2.port)
    wg2.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg2.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg2.add_straight_segment(length=GRATING_TAPER_ROUTE)


    # Create DC at the waveguide attached to the second left-hand grating coupler
    DC = DirectionalCoupler.make_at_port(port=wg2.current_port, length=coupling_length,gap=coupling_gap, bend_radius=BEND_RADIUS)

    # Route the first left-hand grating coupler to the DC
    wg1 = Waveguide.make_at_port(port=left_grating1.port)
    wg1.add_straight_segment_until_y(DC.left_ports[1].origin[1] - BEND_RADIUS)
    wg1.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg1.add_straight_segment_until_x(DC.left_ports[1].origin[0])

    # Route the DC to the lower spiral
    wg3 = Waveguide.make_at_port(port=DC.right_ports[0])
    wg3.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg3.add_bend(angle=-pi/2, radius=BEND_RADIUS)
    wg3.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg3.add_bend(angle=pi/2, radius=BEND_RADIUS)
    wg3.add_bend(angle=pi/2, radius=BEND_RADIUS)

    # Route the DC to the upper spiral
    wg4 = Waveguide.make_at_port(port=DC.right_ports[1])
    wg4.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg4.add_bend(angle=pi/2, radius=BEND_RADIUS)
    wg4.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg4.add_bend(angle=-pi/2, radius=BEND_RADIUS)
    wg4.add_bend(angle=pi/2, radius=BEND_RADIUS)

    # Add the lower spiral
    low_spiral = Spiral.make_at_port(port=wg3.current_port.rotated(0), num=lower_spiral_no, gap=spiral_gap, inner_gap=spiral_inner_gap)
    spiral_obj = low_spiral.get_shapely_object()
    spiral_size = abs(spiral_obj.bounds[1] - spiral_obj.bounds[3])

    # Add the upper spiral
    high_spiral = Spiral.make_at_port(port=wg4.current_port.rotated(0), num=upper_spiral_no, gap=spiral_gap, inner_gap=spiral_inner_gap)
    spiral_obj = high_spiral.get_shapely_object()
    spiral_size = abs(spiral_obj.bounds[1] - spiral_obj.bounds[3])

    # Add waveguide at upper spiral output
    wg6 = Waveguide.make_at_port(port=high_spiral.out_port)
    wg6.add_bend(angle=-pi, radius=BEND_RADIUS)
    wg6.add_straight_segment(length=GRATING_TAPER_ROUTE*3)
    wg6.add_bend(angle=pi / 2, radius=BEND_RADIUS)

    # Add waveguide at lower spiral output before DC2
    wg5 = Waveguide.make_at_port(port=low_spiral.out_port)
    wg5.add_straight_segment(length=GRATING_TAPER_ROUTE)
    wg5.add_bend(angle=-pi / 2, radius=BEND_RADIUS)
    wg5.add_straight_segment_until_x(wg6.current_port.origin[0])

    # Create DC at the waveguide attached to lower spiral output
    DC2 = DirectionalCoupler.make_at_port(port=wg5.current_port, length=coupling_length, gap=coupling_gap,
                                          bend_radius=BEND_RADIUS)

    # Route the DC to first right-hand grating coupler
    wg7 = Waveguide.make_at_port(port=DC2.right_ports[0])
    wg7.add_straight_segment_until_x(3*GRATING_PITCH-BEND_RADIUS)
    wg7.add_bend(angle=-pi/2, radius=BEND_RADIUS)
    wg7.add_straight_segment(length=GRATING_TAPER_ROUTE)

    # Route the DC to the second right-hand grating coupler
    wg8 = Waveguide.make_at_port(port=DC2.right_ports[1])
    wg8.add_straight_segment_until_x(4*GRATING_PITCH-BEND_RADIUS)
    wg8.add_bend(angle=-pi/2, radius=BEND_RADIUS)
    wg8.add_straight_segment_until_y(wg7.current_port.origin[1])

    # Create the first right-hand grating coupler
    right_grating1 = CornerstoneGratingCoupler().create_coupler(origin=((3*GRATING_PITCH), position[1]),
                                                              coupler_params=coupler_parameters)

    # Create the second right-hand grating coupler
    right_grating2 = CornerstoneGratingCoupler().create_cornerstone_coupler_at_port(port=wg8.current_port,
                                                                                    **coupler_parameters, angle=wg8.angle)

    # Add sub-components to respective cell and layers
    asymmetric_spiral_mzi_cell.add_cell(left_grating1.cell)
    asymmetric_spiral_mzi_cell.add_cell(left_grating2.cell)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg1)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg2)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, DC)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg3)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg4)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, low_spiral)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, high_spiral)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg5)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, DC2)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg6)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg7)
    asymmetric_spiral_mzi_cell.add_to_layer(WAVEGUIDE_LAYER, wg8)
    asymmetric_spiral_mzi_cell.add_cell(right_grating1.cell)
    asymmetric_spiral_mzi_cell.add_cell(right_grating2.cell)

    # Grating checker
    grating_checker([left_grating1, left_grating2])
    grating_checker([left_grating1, right_grating1])
    grating_checker([left_grating1, right_grating2])

    return asymmetric_spiral_mzi_cell