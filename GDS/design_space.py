"""
JieQing MO, Tung Yan YEUNG
2023-24 University of Bristol - MSc Optoelectronic and Quantum Technologies
EENGM0026 Nanofabrication for Quantum Engineering

This is the main file to compile the program
"""

from shapely.geometry import Polygon
from gdshelpers.layout import GridLayout

from components import *
from parameters import *

# Path where you want your GDS to be saved to
savepath = r"./"


def generate_blank_gds(d_height=3000,
                       d_width=6000):
    """
    Function which creates the appropriately sized blank design space.
    :return:
    """
    # Define a design bounding box as a guide for our eyes
    outer_corners = [(0, 0), (d_width, 0), (d_width, d_height), (0, d_height)]
    polygon = Polygon(outer_corners)

    layout = GridLayout(title='JMO_YTY_Nanofab_2024',
                        frame_layer=CELL_OUTLINE_LAYER,
                        text_layer=LABEL_LAYER,
                        region_layer_type=None,
                        tight=True,
                        vertical_spacing=10,
                        vertical_alignment=1,
                        horizontal_spacing=10,
                        horizontal_alignment=10,
                        text_size=LABEL_HEIGHT,
                        row_text_size=15
                        )

    return layout, polygon


def grating_sweep(layout_cell):
    """
    Function which takes a layout cell as an argument
    and adds a sweep of grating coupler loopbacks
    with different periods.
    """

    # ============================================================================================
    # for spiral gap sweep
    # initialize parameters
    dc_length = 13.8
    dc_gap = 0.3
    up_no = 1
    low_no = 1
    gap_size = 5
    inner_gap_size = 5

    # for each period create a grating loop back and add to the loopback row
    for i in range(11):
        device_name = 'JMO_YTY_Spiral_gap_sweep_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_length, dc_gap, up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)

        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nSpiral_Up_Loop_'
                                                          + str(up_no) + 'Low_Loop_'
                                                          + str(low_no)))

        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)
        up_no += 0.5

    # ============================================================================================
    # for spiral inner gap sweep
    # add a new row in the layout cell
    layout_cell.begin_new_row()

    up_no = 5
    inner_gap_size = 5
    # for each period create a grating loop back and add to the loopback row
    for i in range(11):
        device_name = 'JMO_YTY_Spiral_inner_gap_sweep_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_length, dc_gap, up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)

        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nSpiral_inner_gap_'
                                                          + str(round(inner_gap_size, 3)) + 'um'))

        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)
        inner_gap_size += 0.3

    # ============================================================================================
    # for DC sweep with silicon lay = 220nm ; etching depth 110nm
    layout_cell.begin_new_row()

    up_no = 3
    dc_lengths = [10.3, 10.4, 10.5, 10.6, 10.7, 10.9, 11.5, 11.6, 11.7, 11.9, 12.0]
    dc_gaps = [0.290, 0.292, 0.294, 0.296, 0.298, 0.300, 0.302, 0.304, 0.306, 0.308, 0.310]

    for i in range(len(dc_lengths)):
        device_name = 'JMO_YTY_DC_sweep_Si_220nm_etch_110nm_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_lengths[i], dc_gaps[i], up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)
        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nDC_Length_' + str(dc_lengths[i]) + 'um Gap_'
                                                          + str(dc_gaps[i]) + 'um'))
        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)

    # ============================================================================================
    # for DC sweep with silicon lay = 220nm ; etching depth 120nm
    layout_cell.begin_new_row()

    dc_lengths = [11.5, 11.6, 11.7, 11.8, 11.9, 12.2, 12.8, 13.0, 13.1, 13.3, 13.4]

    for i in range(len(dc_lengths)):
        device_name = 'JMO_YTY_DC_sweep_Si_220nm_etch_120nm_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_lengths[i], dc_gaps[i], up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)
        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nDC_Length_' + str(dc_lengths[i]) + 'um Gap_'
                                                          + str(dc_gaps[i]) + 'um'))
        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)

    # ============================================================================================
    # for DC sweep with silicon lay = 220nm ; etching depth 130nm
    layout_cell.begin_new_row()

    dc_lengths = [13.0, 13.1, 13.2, 13.3, 13.5, 13.8, 14.5, 14.7, 15.0, 15.2, 15.3]

    for i in range(len(dc_lengths)):
        device_name = 'JMO_YTY_DC_sweep_Si_220nm_etch_130nm_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_lengths[i], dc_gaps[i], up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)
        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nDC_Length_' + str(dc_lengths[i]) + 'um Gap_'
                                                          + str(dc_gaps[i]) + 'um'))
        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)

    # ============================================================================================
    # for DC sweep with silicon lay = 240nm ; etching depth 130nm
    layout_cell.begin_new_row()

    dc_lengths = [12.1, 12.2, 12.3, 12.4, 12.6, 12.9, 13.4, 13.6, 13.8, 14.0, 14.2]
    dc_gaps = [0.290, 0.292, 0.294, 0.296, 0.298, 0.300, 0.302, 0.304, 0.306, 0.308, 0.310]

    for i in range(len(dc_lengths)):
        device_name = 'JMO_YTY_DC_sweep_Si_240nm_etch_130nm_' + str(i)
        asymmetric_spiral_mzi_loopback = asymmetric_spiral_mzi(coupler_parameters, dc_lengths[i], dc_gaps[i], up_no, low_no,
                                                               gap_size, inner_gap_size, name=device_name)
        # Create Label
        asymmetric_spiral_mzi_loopback.add_to_layer(LABEL_LAYER, Text(origin=LABEL_ORIGIN, height=LABEL_HEIGHT,
                                                     angle=LABEL_ANGLE_VERTICAL,
                                                     text=device_name + '\nDC_Length_' + str(dc_lengths[i]) + 'um Gap_'
                                                          + str(dc_gaps[i]) + 'um'))
        layout_cell.add_to_row(asymmetric_spiral_mzi_loopback)

    return layout_cell


def populate_gds(layout_cell, polygon):
    """
    Function which takes in the blank design space and populates it

    :param polygon: Shape of bounding box
    :param layout_cell: The blank layout cell
    :return: Populated design space
    """

    # Add a new row to the layout cell and stamp out devices
    layout_cell.begin_new_row()
    layout_cell = grating_sweep(layout_cell)

    # Generate the design space populated with the devices
    design_space_cell, mapping = layout_cell.generate_layout(cell_name='Cell0_JMO_YTY_Nanofab_2024_UoB')

    # Add our bounding box
    design_space_cell.add_to_layer(CELL_OUTLINE_LAYER, polygon)

    # Save our GDS
    design_space_cell.save('{0}JMO_YTY_Nanofab_2024_UoB.gds'.format(savepath))
    # design_space_cell.show()

    return design_space_cell


# Call the function which generates a blank design space
blank_design_space, bounding_box = generate_blank_gds()

# Populate the blank gds with all of our devices
populate_gds(blank_design_space, bounding_box)
