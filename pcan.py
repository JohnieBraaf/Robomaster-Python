import PCANBasic


class CAN():
    def __init__(self,
                 usb_bus=PCANBasic.PCAN_USBBUS1,
                 isFD=False,
                 bitrate=PCANBasic.PCAN_BAUD_500K,
                 bitrateFD=b'f_clock_mhz=20, nom_brp=5, nom_tseg1=2, nom_tseg2=1, nom_sjw=1, data_brp=2, data_tseg1=3, data_tseg2=1, data_sjw=1'):
        self.usb_bus = usb_bus
        self.isFD = isFD
        self.bitrate = bitrate
        self.bitrateFD = bitrateFD

        # init CAN interface
        self.can = PCANBasic.PCANBasic()
        if self.isFD:
            result = self.can.InitializeFD(self.usb_bus,self.bitrateFD)
        else:
            result = self.can.Initialize(self.usb_bus,self.bitrate)
        if result != PCANBasic.PCAN_ERROR_OK:
            print("Failed to initialize CAN interface")
            print(self.get_error_text(result))
            return

        # main loop
        while True:
            result = PCANBasic.PCAN_ERROR_OK
            while (not (result & PCANBasic.PCAN_ERROR_QRCVEMPTY)):
                result = self.read()
                if result != PCANBasic.PCAN_ERROR_OK and result != PCANBasic.PCAN_ERROR_QRCVEMPTY:
                    print(self.get_error_text(result))
                    return

    def read(self):
        if self.isFD:
            result = self.can.ReadFD(self.usb_bus)
        else:
            result = self.can.Read(self.usb_bus)

        if result[0] == PCANBasic.PCAN_ERROR_OK:
            message = result[1]
            message_id = '%.3X' % message.ID
            if (message.MSGTYPE & PCANBasic.PCAN_MESSAGE_EXTENDED.value) == PCANBasic.PCAN_MESSAGE_EXTENDED.value:
                message_id = '%.8X' % message.ID
            message_hex = b''
            for message_byte in message.DATA:
                message_hex += b'%.2X ' % message_byte
            message_hex = str(message_hex).replace("'", "", 2).replace("b", "", 1)

            timestamp = result[2]
            if not self.isFD:
                timestamp = timestamp.micros + (1000 * timestamp.millis) + (0x100000000 * 1000 * timestamp.millis_overflow)

            print(timestamp, message_id, message_hex)

        return result[0]

    def get_error_text(self, error):
        result = self.can.GetErrorText(error, 0x09)
        if result[0] != PCANBasic.PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            message = str(result[1])
            return message.replace("'", "", 2).replace("b", "", 1)


can1 = CAN(bitrate=PCANBasic.PCAN_BAUD_1M)
