// motion_tracker_pybind.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cstdlib>

namespace py = pybind11;

// declare C functions
extern "C" {
    char* mt_capture_landmarks(int cam_index);
}

std::vector<float> capture_landmarks(int cam_index) {
    char* s = mt_capture_landmarks(cam_index);
    std::string str(s);
    free(s);
    if (str == "NONE" || str.rfind("ERR", 0) == 0) {
        throw std::runtime_error(str);
    }
    std::vector<float> out;
    size_t start = 0;
    while (start < str.size()) {
        size_t pos = str.find(',', start);
        if (pos == std::string::npos) pos = str.size();
        std::string token = str.substr(start, pos - start);
        out.push_back(std::stof(token));
        start = pos + 1;
    }
    return out;
}

PYBIND11_MODULE(motion_tracker_bindings, m) {
    m.doc() = "Motion tracker bindings for DEX";
    m.def("capture_landmarks", &capture_landmarks, "Capture normalized hand landmarks from camera (cam index)");
}