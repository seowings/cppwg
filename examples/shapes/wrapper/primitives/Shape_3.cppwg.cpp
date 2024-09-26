// This file is automatically generated by cppwg.
// Do not modify this file directly.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.cppwg.hpp"

#include "Shape_3.cppwg.hpp"

namespace py = pybind11;
typedef Shape<3> Shape_3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

void register_Shape_3_class(py::module &m)
{
    py::class_<Shape_3, std::shared_ptr<Shape_3>>(m, "Shape_3")
        .def(py::init<>())
        .def("GetIndex",
            (unsigned int(Shape_3::*)() const) &Shape_3::GetIndex,
            " ")
        .def("rGetVertices",
            (::std::vector<std::shared_ptr<Point<3>>> const &(Shape_3::*)() const) &Shape_3::rGetVertices,
            " ", py::return_value_policy::reference_internal)
        .def("SetIndex",
            (void(Shape_3::*)(unsigned int)) &Shape_3::SetIndex,
            " ", py::arg("index"))
        .def("SetVertices",
            (void(Shape_3::*)(::std::vector<std::shared_ptr<Point<3>>> const &)) &Shape_3::SetVertices,
            " ", py::arg("rVertices"))
        .def("AddVertex",
            (void(Shape_3::*)(::std::shared_ptr<Point<3>>)) &Shape_3::AddVertex,
            " ", py::arg("point") = std::make_shared<Point<3>>())
    ;
}
