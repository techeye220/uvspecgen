# Generate UV-Vis spectra from electronic structure TDHF/TDDFT output files. 
# Copyright (C) 2014 Li Research Group (University of Washington) 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Electronic structure program output file parsing using ``cclib``.

This module provides the abstract ``Logfile`` class for parsing excited
state energies and oscillator strengths from CIS, TD-HF, and TD-DFT
calculations.  It uses the ``cclib`` library for parsing the output of
various computational chemistry packages.  The following packages are
currently supported:
    * ADF
    * GAMESS
    * Gaussian03
    * Gaussian09
    * Jaguar

"""
import logging
import os.path
import sys

from uvspec.config.settings import error

try:
    import numpy
except ImportError:
    error('The ``numpy`` package is required\n'
          '         ``numpy`` is free to download at http://www.numpy.org')

try:
    from cclib.parser import ccopen
except ImportError:
    error('The ``cclib`` package is required\n'
          '         ``cclib`` is free to download at http://cclib.sf.net')


class Logfile(object):
    """Abstract logfile class for extracting excited state data.
    
    The ``cclib`` parsing library is used to return a generic 1D-array of
    excited state energies (in units of cm^-1) and a 1D-array of oscillator
    strengths for all excited states in a logfile generated by one of the
    supported computational chemistry packages: ADF, GAMESS, Gaussian03,
    Gaussian09, or Jaguar.
    
    """
    def __init__(self, filename=None):
        """Extract the excited state energies and oscillator strengths.

        When an instance of the ``Logfile`` class is created, the
        ``excited_state_energy`` and ``oscillator_strength`` arrays are
        initialized as empty lists.  This lists are populated once the
        ``parse()`` method is called.

        If ``filename`` is not provided, an empty instance of the ``Logfile``
        object is returned.

        """
        self.name = filename
        self.excited_state_energy = [] 
        self.oscillator_strength = [] 

    def __repr__(self):
        return 'Logfile: %s' % self.name

    def parse(self):
        """Parse the logfile and assign the discrete spectrum values."""
        try:
            if os.path.exists(self.name):
                logfile = ccopen(self.name)
                logfile.logger.setLevel(logging.ERROR)
                data = logfile.parse()
                setattr(self, 'excited_state_energy', data.etenergies)
                setattr(self, 'oscillator_strength', data.etoscs)
            else:
                error('The logfile `%s` could not be found' % self.name)
        except TypeError:
            error('The `parse()` method requires the `filename` argument '
                  'in `Logfile`')
