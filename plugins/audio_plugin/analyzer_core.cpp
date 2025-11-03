// plugins/audio_plugin/analyzer_core.cpp
// Minimal analyzer core for demonstration. Compile with:
//   g++ -std=c++17 -O2 analyzer_core.cpp -o analyzer_core
#include <iostream>
#include <vector>
#include <cmath>

double rms(const std::vector<double>& buf) {
    double s = 0.0;
    for (double v : buf) s += v*v;
    return std::sqrt(s / buf.size());
}

int main() {
    std::vector<double> test = {0.1, 0.2, -0.3, 0.4, -0.1};
    std::cout << "[analyzer_core] rms=" << rms(test) << std::endl;
    return 0;
}