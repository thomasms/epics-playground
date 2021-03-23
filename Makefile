TOP = .
include $(TOP)/configure/CONFIG

EMBEDDED_TOPS += $(TOP)/servers/simple
# more here....


DIRS := configure
DIRS += $(EMBEDDED_TOPS)
include $(TOP)/configure/RULES_TOP
