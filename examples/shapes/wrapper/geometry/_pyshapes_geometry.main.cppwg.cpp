// This file is automatically generated by cppwg.
// Do not modify this file directly.

#include <pybind11/pybind11.h>
#include "wrapper_header_collection.cppwg.hpp"
#include "Point_2.cppwg.hpp"
#include "Point_3.cppwg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_geometry, m)
{
    register_Point_2_class(m);
    register_Point_3_class(m);
}