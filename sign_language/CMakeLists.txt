cmake_minimum_required(VERSION 3.14)
project(dex_motion_tracker)

find_package(OpenCV REQUIRED)
find_package(Python COMPONENTS Interpreter Development REQUIRED)
# optionally find pybind11
find_package(pybind11 QUIET)

add_library(motion_tracker SHARED motion_tracker.cpp)
target_include_directories(motion_tracker PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(motion_tracker PRIVATE ${OpenCV_LIBS})

if(pybind11_FOUND)
  pybind11_add_module(motion_tracker_bindings motion_tracker_pybind.cpp)
  target_link_libraries(motion_tracker_bindings PRIVATE motion_tracker)
endif()