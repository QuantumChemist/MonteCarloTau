#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <random>

namespace py = pybind11;

std::tuple<std::vector<std::array<double,2>>, int, int> generate_batch(int batch_size=100) {
    std::vector<std::array<double,2>> pts;
    pts.reserve(batch_size);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    int c = 0;
    for (int i = 0; i < batch_size; ++i) {
        double x = dis(gen);
        double y = dis(gen);
        pts.push_back({x, y});
        if (x*x + y*y <= 1.0) ++c;
    }
    return std::make_tuple(pts, c, batch_size);
}

PYBIND11_MODULE(montecpp, m) {
    m.doc() = "Monte Carlo helpers";
    m.def("generate_batch", &generate_batch, py::arg("batch_size")=100);
}
