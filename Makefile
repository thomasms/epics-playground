TOP = .
include $(TOP)/configure/CONFIG

EMBEDDED_TOPS += $(TOP)/exampleone
# more here....


DIRS := configure
DIRS += $(EMBEDDED_TOPS)
include $(TOP)/configure/RULES_TOP
