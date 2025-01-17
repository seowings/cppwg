// This file is auto-generated by cppwg; manual changes will be overwritten.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <memory>
#include "PottsMesh.hpp"

#include "PottsMesh_3.cppwg.hpp"

namespace py = pybind11;
typedef PottsMesh<3> PottsMesh_3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class PottsMesh_3_Overrides : public PottsMesh_3
{
public:
    using PottsMesh_3::PottsMesh;
    void Scale(double const factor) override
    {
        PYBIND11_OVERRIDE(
            void,
            PottsMesh_3,
            Scale,
            factor);
    }
};

void register_PottsMesh_3_class(py::module &m)
{
    py::class_<PottsMesh_3, PottsMesh_3_Overrides, std::shared_ptr<PottsMesh_3>, AbstractMesh<3, 3>>(m, "PottsMesh_3")
        .def(py::init<>())
        .def("Scale",
            (void(PottsMesh_3::*)(double const)) &PottsMesh_3::Scale,
            " ", py::arg("factor"))
    ;
}
