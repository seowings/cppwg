// This file is auto-generated by cppwg; manual changes will be overwritten.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <memory>
#include "AbstractMesh.hpp"

#include "AbstractMesh_3_3.cppwg.hpp"

namespace py = pybind11;
typedef AbstractMesh<3, 3> AbstractMesh_3_3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class AbstractMesh_3_3_Overrides : public AbstractMesh_3_3
{
public:
    using AbstractMesh_3_3::AbstractMesh;
    void Scale(double const factor) override
    {
        PYBIND11_OVERRIDE_PURE(
            void,
            AbstractMesh_3_3,
            Scale,
            factor);
    }
};

void register_AbstractMesh_3_3_class(py::module &m)
{
    py::class_<AbstractMesh_3_3, AbstractMesh_3_3_Overrides, std::shared_ptr<AbstractMesh_3_3>>(m, "AbstractMesh_3_3")
        .def(py::init<>())
        .def("GetIndex",
            (unsigned int(AbstractMesh_3_3::*)() const) &AbstractMesh_3_3::GetIndex,
            " ")
        .def("SetIndex",
            (void(AbstractMesh_3_3::*)(unsigned int)) &AbstractMesh_3_3::SetIndex,
            " ", py::arg("index"))
        .def("AddNode",
            (void(AbstractMesh_3_3::*)(::Node<3>)) &AbstractMesh_3_3::AddNode,
            " ", py::arg("node"))
        .def("Scale",
            (void(AbstractMesh_3_3::*)(double const)) &AbstractMesh_3_3::Scale,
            " ", py::arg("factor"))
    ;
}
