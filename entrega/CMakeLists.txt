cmake_minimum_required(VERSION 3.3)
project(entrega)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp CsvReader.cpp CsvReader.h)
add_executable(entrega ${SOURCE_FILES})
