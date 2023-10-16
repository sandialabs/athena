cmake_minimum_required(VERSION 3.16)
project(timeloop)

set(CMAKE_CXX_STANDARD 14)
SET(BOOST_ROOT "/usr/lib/x86_64-linux-gnu/")
find_package(Boost 1.67.0 COMPONENTS iostreams serialization)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
add_subdirectory(${CMAKE_SOURCE_DIR}/yaml-cpp-master)

find_package(yaml-cpp REQUIRED)
find_library(libconfig libconfig)
find_package(Curses REQUIRED)
include_directories(${CURSES_INCLUDE_DIR})
include_directories(${Boost_INCLUDE_DIRS})

include_directories(include)
include_directories(include/applications)
include_directories(include/applications/design-space)
include_directories(include/applications/mapper)
include_directories(include/applications/metrics)
include_directories(include/applications/model)
include_directories(include/applications/simple-mapper)
include_directories(include/compound-config)
include_directories(include/data)
include_directories(include/data/cnn)
include_directories(include/loop-analysis)
include_directories(include/mapping)
include_directories(include/mapspaces)
include_directories(include/model)
include_directories(include/pat)
include_directories(include/search)
include_directories(include/util)
include_directories(include/workload)
include_directories(include/workload/density-models)
include_directories(include/workload/format-models)
include_directories(include/workload/shape-models)
include_directories(include/workload/util)
include_directories(pat-public/src/pat)
include_directories(src/pat)

add_library(timeloop

        include/compound-config/compound-config.hpp
        include/data/cnn/cnn-densities.hpp
        include/data/cnn/cnn-layers.hpp
        include/loop-analysis/coordinate-space-tile-info.hpp
        include/loop-analysis/loop-state.hpp
        include/loop-analysis/nest-analysis-tile-info.hpp
        include/loop-analysis/nest-analysis.hpp
        include/loop-analysis/operation-type.hpp
        include/loop-analysis/point-set-aahr.hpp
        include/loop-analysis/point-set.hpp
        include/loop-analysis/point.hpp
        include/loop-analysis/sparse-analysis.hpp
        include/loop-analysis/tiling-tile-info.hpp
        include/loop-analysis/tiling.hpp
        include/mapping/arch-properties.hpp
        include/mapping/constraints.hpp
        include/mapping/loop.hpp
        include/mapping/mapping.hpp
        include/mapping/nest.hpp
        include/mapping/parser.hpp
        include/mapping/spacetime.hpp
        include/mapspaces/mapspace-base.hpp
        include/mapspaces/mapspace-factory.hpp
        include/mapspaces/subspaces.hpp
        include/mapspaces/uber.hpp
        include/model/arithmetic.hpp
        include/model/attribute.hpp
        include/model/buffer.hpp
        include/model/engine.hpp
        include/model/level.hpp
        include/model/model-base.hpp
        include/model/network-factory.hpp
        include/model/network-legacy.hpp
        include/model/network-reduction-tree.hpp
        include/model/network-simple-multicast.hpp
        include/model/network.hpp
        include/model/sparse-optimization-info.hpp
        include/model/sparse-optimization-parser.hpp
        include/model/topology.hpp
        include/model/util.hpp
        include/pat/pat.cpp
        include/pat/pat.hpp
        include/search/exhaustive.hpp
        include/search/hybrid.hpp
        include/search/linear-pruned.hpp
        include/search/random-pruned.hpp
        include/search/random.hpp
        include/search/search-factory.hpp
        include/search/search.hpp
        include/util/accelergy_interface.hpp
        include/util/args.hpp
        include/util/banner.hpp
        include/util/dynamic-array.hpp
        include/util/map2d.hpp
        include/util/misc.hpp
        include/util/numeric.hpp
        include/workload/density-models/density-distribution-factory.hpp
        include/workload/density-models/density-distribution.hpp
        include/workload/density-models/fixed-structured-distribution.hpp
        include/workload/density-models/hypergeometric-distribution.hpp
        include/workload/format-models/coordinate-payload.hpp
        include/workload/format-models/metadata-format-factory.hpp
        include/workload/format-models/metadata-format.hpp
        include/workload/format-models/run-length-encoding.hpp
        include/workload/format-models/uncompressed-bitmask.hpp
        include/workload/format-models/uncompressed-offset-pair.hpp
        include/workload/shape-models/data-space.hpp
        include/workload/shape-models/operation-space.hpp
        include/workload/shape-models/problem-shape.hpp
        include/workload/util/per-data-space.hpp
        include/workload/util/per-problem-dimension.hpp
        include/workload/workload.hpp
        pat-public/src/pat/pat.cpp
        pat-public/src/pat/pat.hpp

        src/compound-config/compound-config.cpp
        src/data/cnn/cnn-densities.cpp
        src/data/cnn/cnn-layers.cpp
        src/loop-analysis/coordinate-space-tile-info.cpp
        src/loop-analysis/loop-state.cpp
        src/loop-analysis/nest-analysis-tile-info.cpp
        src/loop-analysis/nest-analysis.cpp
        src/loop-analysis/operation-type.cpp
        src/loop-analysis/point-set-aahr.cpp
        src/loop-analysis/point.cpp
        src/loop-analysis/sparse-analysis.cpp
        src/loop-analysis/tiling-tile-info.cpp
        src/loop-analysis/tiling.cpp
        src/mapping/arch-properties.cpp
        src/mapping/constraints.cpp
        src/mapping/loop.cpp
        src/mapping/mapping.cpp
        src/mapping/nest.cpp
        src/mapping/parser.cpp
        src/mapspaces/mapspace-base.cpp
        src/mapspaces/mapspace-factory.cpp
        src/mapspaces/subspaces.cpp
        src/mapspaces/uber.cpp
        src/model/arithmetic.cpp
        src/model/buffer.cpp
        src/model/engine.cpp
        src/model/level.cpp
        src/model/model-base.cpp
        src/model/network-factory.cpp
        src/model/network-legacy.cpp
        src/model/network-reduction-tree.cpp
        src/model/network-simple-multicast.cpp
        src/model/network.cpp
        src/model/sparse-optimization-info.cpp
        src/model/sparse-optimization-parser.cpp
        src/model/topology.cpp
        src/pat/pat.cpp
        src/pat/pat.hpp
        src/search/exhaustive.cpp
        src/search/hybrid.cpp
        src/search/linear-pruned.cpp
        src/search/random-pruned.cpp
        src/search/random.cpp
        src/search/search-factory.cpp
        src/util/accelergy_interface.cpp
        src/util/args.cpp
        src/util/banner.cpp
        src/util/map2d.cpp
        src/util/numeric.cpp
        src/workload/density-models/density-distribution-factory.cpp
        src/workload/density-models/density-distribution.cpp
        src/workload/density-models/fixed-structured-distribution.cpp
        src/workload/density-models/hypergeometric-distribution.cpp
        src/workload/format-models/coordinate-payload.cpp
        src/workload/format-models/metadata-format-factory.cpp
        src/workload/format-models/metadata-format.cpp
        src/workload/format-models/run-length-encoding.cpp
        src/workload/format-models/uncompressed-bitmask.cpp
        src/workload/format-models/uncompressed-offset-pair.cpp
        src/workload/shape-models/operation-space.cpp
        src/workload/shape-models/problem-shape.cpp
        src/workload/workload.cpp)


add_executable(timeloop-mapper
        src/applications/mapper/main.cpp
        src/applications/mapper/mapper-thread.cpp
        src/applications/mapper/mapper.cpp
        include/applications/mapper/mapper-thread.hpp
        include/applications/mapper/mapper.hpp)

target_link_libraries(timeloop ${Boost_LIBRARIES} Threads::Threads yaml-cpp  config config++  ${CURSES_LIBRARIES})
target_link_libraries(timeloop-mapper timeloop Threads::Threads config  ${CURSES_LIBRARIES})

include_directories(${YAML_CPP_INCLUDE_DIRS})

message(STATUS ${Boost_LIBRARIES})
message(STATUS ${CMAKE_SOURCE_DIR})
target_compile_definitions(timeloop PUBLIC -DBUILD_BASE_DIR=\"${CMAKE_SOURCE_DIR}\" )
target_compile_definitions(timeloop-mapper PUBLIC -DUSE_ACCELERGY)
add_definitions(-DCMAKE_EXPORT_COMPILE_COMMANDS=ON)
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} "-flto -march=native -floop-parallelize-all -floop-nest-optimize -fgraphite-identity -ftree-loop-distribution -ftree-vectorize")
#include/applications/design-space/arch.hpp
#include/applications/design-space/design-space.hpp
#include/applications/design-space/problem.hpp
#
#include/applications/metrics/metrics.hpp
#include/applications/model/model.hpp
#include/applications/simple-mapper/simple-mapper.hpp
#
#src/applications/design-space/arch.cpp
#src/applications/design-space/design-space.cpp
#src/applications/design-space/main.cpp
#src/applications/design-space/problem.cpp
#
#src/applications/metrics/main.cpp
#src/applications/metrics/metrics.cpp
#src/applications/model/main.cpp
#src/applications/model/model.cpp
#src/applications/simple-mapper/main.cpp
#src/applications/simple-mapper/simple-mapper.cpp