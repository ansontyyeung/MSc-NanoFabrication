import numpy as np

#################
# GENERAL PARAMS
################
WAVEGUIDE_LAYER = (3, 0)
GRATING_LAYER = (4, 0)
WAVEGUIDE_WIDTH = 0.45
BEND_RADIUS = 10
VGA_NUM_CHANNELS = 127
CELL_OUTLINE_LAYER = (99, 0)
LABEL_LAYER = (100, 0)
CELL_VERTICAL_SPACING = 20
CELL_HORIZONTAL_SPACING = 10

###########################
# GRATING COUPLER PARAMETERS
###########################
GRATING_COUPLER_WIDTH = 0.45
GRATING_FAN_ANGLE = 1.5
GRATING_PERIOD = 0.67
GRATING_FILL_FACTOR = 0.5
GRATING_NO_PERIODS = 60
GRATING_TAPER_LENGTH = 350
GRATING_PITCH = 127.0
GRATING_TAPER_ROUTE = 10.0
coupler_parameters = {
    'width': GRATING_COUPLER_WIDTH,
    'full_opening_angle': np.deg2rad(GRATING_FAN_ANGLE),
    'grating_period': GRATING_PERIOD,
    'grating_ff': GRATING_FILL_FACTOR,
    'n_gratings': GRATING_NO_PERIODS,
    'taper_length': GRATING_TAPER_LENGTH
}

teeth_coupler_parameters = {
    'width': GRATING_COUPLER_WIDTH,
    'full_opening_angle': np.deg2rad(GRATING_FAN_ANGLE)*1.1,
    'grating_period': GRATING_PERIOD,
    'grating_ff': GRATING_FILL_FACTOR,
    'n_gratings': GRATING_NO_PERIODS,
    'taper_length': GRATING_TAPER_LENGTH
}

###########################
# TEXT PARAMETERS
###########################
LABEL_ORIGIN = [80, -385]
LABEL_ORIGIN_HORIZONTAL = [-280, -110]
LABEL_HEIGHT = 10
LABEL_ANGLE_VERTICAL = np.pi / 2
LABEL_ANGLE_HORIZONTAL = 0
