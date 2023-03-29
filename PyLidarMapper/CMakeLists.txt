cmake_minimum_required(VERSION 3.24)
project(PyLidarMapper)

add_compile_definitions(MAIN_DIR=\"${CMAKE_SOURCE_DIR}\")

add_subdirectory(Projector)
add_subdirectory(PyMapper)