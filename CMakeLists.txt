cmake_minimum_required(VERSION 3.14)
project(trading_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Fetch pybind11 directly if not installed system-wide
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.12.0   # pick a stable release
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(trading_cpp bindings.cpp)

# 👇 Add this so the compiler can find headers in your source dir
target_include_directories(trading_cpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
