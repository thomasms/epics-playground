TOP=..

include $(TOP)/configure/CONFIG

EPICS_BASE_PVA_CORE_LIBS = pvDatabase pvaClient pvAccess nt pvData Com

INC += pv/simpleIntRecord.hpp

exampleoneSRC = $(TOP)/exampleone
PROD_HOST += one
one_SRCS += main.cpp
one_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)

include $(TOP)/configure/RULES

CXXFLAGS = -std=c++11 -Wall -Wpedantic -O2 -g 