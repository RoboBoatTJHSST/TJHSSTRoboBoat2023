cmake_minimum_required(VERSION 3.24)
project(PyMapper)

set(CMAKE_CXX_STANDARD 17)

# Required by livox sdk
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Include opencv
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})
add_definitions(${OpenCV_DEFINITIONS})

# Include livox sdk
link_directories(~/Livox-SDK/build/sdk_core/)

# Needed to load config stuff
find_package(yaml-cpp REQUIRED)
include_directories(${yaml-cpp_INCLUDE_DIRS})
link_directories(${yaml-cpp_LIBRARY_DIRS})
add_definitions(${yaml-cpp_DEFINITIONS})

# Needed to compile Projector
find_package(PCL REQUIRED COMPONENTS common io)
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

# Python binding library
add_subdirectory(pybind11)
pybind11_add_module(pymapper SHARED LidarCapture.cpp py-mapper.cpp)
set_target_properties(pymapper PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/")

# Linking stuff
target_link_libraries(pymapper PRIVATE Threads::Threads)
target_link_libraries(pymapper PRIVATE ${OpenCV_LIBRARIES})
target_link_libraries(pymapper PRIVATE ${PCL_LIBRARIES})
target_link_libraries(pymapper PRIVATE ${Pylon_LIBRARIES})
target_link_libraries(pymapper PRIVATE yaml-cpp)
target_link_libraries(pymapper PRIVATE liblivox_sdk_static.a)

# Actually compile python bindings
target_compile_definitions(pymapper PRIVATE VERSION_INFO=0.1)
