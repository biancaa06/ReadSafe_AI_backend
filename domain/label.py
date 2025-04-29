from enum import Enum


class AgeLabelEnum(Enum):
    AGE_5_8 = 1
    AGE_8_12 = 2
    AGE_12_PLUS = 3

LABEL_NAMES = {
    AgeLabelEnum.AGE_5_8: "Age 5–8",
    AgeLabelEnum.AGE_8_12: "Age 8–12",
    AgeLabelEnum.AGE_12_PLUS: "Age 12+"
}