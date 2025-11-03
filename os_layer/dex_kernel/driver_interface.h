#ifndef DEX_DRIVER_INTERFACE_H
#define DEX_DRIVER_INTERFACE_H

#include <string>
#include <iostream>

class DEXDriverInterface {
public:
    void init_driver(const std::string& driver_name) {
        std::cout << "[Driver] Initializing: " << driver_name << std::endl;
    }

    void send_signal(const std::string& signal) {
        std::cout << "[Driver] Signal sent: " << signal << std::endl;
    }

    void shutdown() {
        std::cout << "[Driver] Shutdown sequence complete." << std::endl;
    }
};

#endif