// This file is automatically generated by cppwg.
// Do not modify this file directly.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.cppwg.hpp"

#include "Rectangle.cppwg.hpp"

namespace py = pybind11;
typedef Rectangle Rectangle;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

void register_Rectangle_class(py::module &m)
{
    py::class_<Rectangle, std::shared_ptr<Rectangle>, Shape<2>>(m, "Rectangle")
        .def(py::init<double, double>(), py::arg("width") = 2.0, py::arg("height") = 1.0)
        .def(py::init<::std::vector<std::shared_ptr<Point<2>>> const>(), py::arg("points") = ::std::vector<std::shared_ptr<Point<2>>> {})
    ;
}
