# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Fran�ois Bissey, francois.bissey@canterbury.ac.nz, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.compiler import *

class Xl(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['xlc','xlc_r']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['xlC','xlC_r','xlc++','xlc++_r']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['xlf','xlf_r']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['xlf90','xlf90_r','xlf95','xlf95_r','xlf2003','xlf2003_r','xlf2008','xlf2008_r']

    @property
    def cxx11_flag(self):
        if self.version < ver('13.1'):
            tty.die("Only xlC 13.1 and above have some c++11 support.")
        else:
            return "-qlanglvl=extended0x"

    @classmethod
    def default_version(self, comp):
        """The '-qversion' is the standard option fo XL compilers.
           Output looks like this::

              IBM XL C/C++ for Linux, V11.1 (5724-X14)
              Version: 11.01.0000.0000

           or::

              IBM XL Fortran for Linux, V13.1 (5724-X16)
              Version: 13.01.0000.0000

           or::

              IBM XL C/C++ for AIX, V11.1 (5724-X13)
              Version: 11.01.0000.0009

           or::

              IBM XL C/C++ Advanced Edition for Blue Gene/P, V9.0
              Version: 09.00.0000.0017
        """

        return get_compiler_version(
            comp, '-qversion',r'([0-9]?[0-9]\.[0-9])')

    @classmethod
    def fc_version(cls, fc):
        """The fortran and C/C++ versions of the XL compiler are always two units apart.
           By this we mean that the fortran release that goes with XL C/C++ 11.1 is 13.1.
           Having such a difference in version number is confusing spack quite a lot.
           Most notably if you keep the versions as is the default xl compiler will only
           have fortran and no C/C++.
           So we associate the Fortran compiler with the version associated to the C/C++
           compiler.
           One last stumble. Version numbers over 10 have at least a .1 those under 10
           a .0. There is no xlf 9.x or under currently available. BG/P and BG/L can
           such a compiler mix and possibly older version of AIX and linux on power.
        """
        fver = get_compiler_version(fc, '-qversion',r'([0-9]?[0-9]\.[0-9])')
        cver = float(fver) - 2
        if cver < 10 :
          cver = cver - 0.1
        return str(cver)


    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
