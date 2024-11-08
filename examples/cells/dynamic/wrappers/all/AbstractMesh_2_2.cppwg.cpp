// This file is auto-generated by cppwg; manual changes will be overwritten.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <memory>
#include "AbstractMesh.hpp"

#include "AbstractMesh_2_2.cppwg.hpp"

namespace py = pybind11;
typedef AbstractMesh<2, 2> AbstractMesh_2_2;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class AbstractMesh_2_2_Overrides : public AbstractMesh_2_2
{
public:
    using AbstractMesh_2_2::AbstractMesh;
    void Scale(double const factor) override
    {
        PYBIND11_OVERRIDE_PURE(
            void,
            AbstractMesh_2_2,
            Scale,
            factor);
    }
};

void register_AbstractMesh_2_2_class(py::module &m)
{
    py::class_<AbstractMesh_2_2, AbstractMesh_2_2_Overrides, std::shared_ptr<AbstractMesh_2_2>>(m, "AbstractMesh_2_2")
        .def(py::init<>())
        .def("GetIndex",
            (unsigned int(AbstractMesh_2_2::*)() const) &AbstractMesh_2_2::GetIndex,
            " ")
        .def("SetIndex",
            (void(AbstractMesh_2_2::*)(unsigned int)) &AbstractMesh_2_2::SetIndex,
            " ", py::arg("index"))
        .def("AddNode",
            (void(AbstractMesh_2_2::*)(::Node<2>)) &AbstractMesh_2_2::AddNode,
            " ", py::arg("node"))
        .def("Scale",
            (void(AbstractMesh_2_2::*)(double const)) &AbstractMesh_2_2::Scale,
            " ", py::arg("factor"))
    ;
}