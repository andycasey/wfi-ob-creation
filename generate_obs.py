#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate Observation Blocks for the 'Awakening the Giants' program on the
Wide Field Imager at the 2.2 m MPG telescope at La Silla Observatory.
"""

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__author__ = "Andy Casey <arc@ast.cam.ac.uk>"

import numpy as np
import os

import astropy.units as u
import astropy.coordinates as coord

import ob_templates

# 10 Sky flats
# 10 Dome flats
# Focus sequence

clobber = True
ins_filter_name = "MB#516/16_ESO871"
output_folder = "OBs"


# Focus Sequence.
bulge = coord.Galactic(0, 0, unit=u.degree).transform_to(coord.ICRS)
focus_ob = ob_templates.FocusSequenceObservationBlock(
    "cal.focus", ins_filter_name, target_ra=bulge.ra, target_dec=bulge.dec)
focus_ob.write(os.path.join(output_folder, "atg.cal.focus.obx"), clobber)


# Sky flats.
sky_flat_ob = ob_templates.SkyFlatObservationBlock("cal.skyflats", ins_filter_name)
sky_flat_ob.update(det_explevel=20000, seq_nexpo=3)
sky_flat_ob.write(os.path.join(output_folder, "atg.cal.skyflat.obx"), clobber)


# Dome flats.
dome_flat_ob = ob_templates.DomeFlatObservationBlock("cal.domeflats", ins_filter_name)
dome_flat_ob.update(det_explevel=20000, seq_nexpo=3)
dome_flat_ob.write(os.path.join(output_folder, "atg.cal.domeflat.obx"), clobber)


# Science exposures.
# (From -10 to +10 in l, -2.5 to +2.5 in b)
# All in 0.4 degree increments.

repr_gal_deg = lambda x: "{0}{1:0>2d}".format("mp"[x > 0], abs(int(x * 10)))
generate_ob_name = lambda N, l, b: "atg.sci.{N:0>4.0f}.{l_str}{b_str}".format(N=N,
    l_str=repr_gal_deg(l), b_str=repr_gal_deg(b))

N, step = (0, 0.4)
for l in np.arange(-10, 10 + step, step):
    for b in np.arange(-2.5, 2.5 + step, step):

        coordinate = coord.Galactic(l, b, unit=u.degree).transform_to(coord.ICRS)

        # Create the observation block.
        observation_block = ob_templates.ScienceObservationBlock(
            ob_name=generate_ob_name(N, l, b),
            ins_filter_name=ins_filter_name,
            target_ra=coordinate.ra,
            target_dec=coordinate.dec,
            exposure_time=100, 
            num_exposures=5,
        )

        observation_block.write(os.path.join(output_folder, 
            "{}.obx".format(observation_block.ob_name)),
        clobber=clobber)

        print("Generated OB {0}: {1}".format(N, observation_block.ob_name))
        N += 1
