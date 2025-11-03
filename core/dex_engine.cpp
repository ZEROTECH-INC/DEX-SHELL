// core/dex_engine.cpp
// Minimal DEX Engine skeleton (C++)
// Build: g++ -std=c++17 -O2 -o dex_engine dex_engine.cpp

#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <csignal>

std::atomic<bool> running(true);

void signal_handler(int signum) {
    running = false;
}

void engine_loop() {
    int tick = 0;
    while (running) {
        std::cout << "[dex_engine] tick=" << tick++ << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    std::cout << "[dex_engine] graceful shutdown." << std::endl;
}

int main(int argc, char** argv) {
    std::cout << "DEX Engine (C++) starting..." << std::endl;
    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);
    engine_loop();
    return 0;
}
