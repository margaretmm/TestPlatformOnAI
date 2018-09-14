from enum import IntEnum, unique


@unique
class TransferType_Enum(IntEnum):
    http=1,
    mq=2


if __name__ == "__main__":
   print(TransferType_Enum['http'].name)
   print(TransferType_Enum['http'].value)
   print(type(TransferType_Enum.http.name))
