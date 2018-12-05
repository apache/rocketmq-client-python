add_executable(runUnitTests
		PythonWrapperTest.cpp
		)

target_link_libraries(runUnitTests
		dl
		gtest)

if (UNIX AND NOT APPLE)
	target_link_libraries(runUnitTests rt)
endif ()

set_target_properties(runUnitTests PROPERTIES
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
