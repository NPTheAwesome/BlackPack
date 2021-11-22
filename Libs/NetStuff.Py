from dataclasses import dataclass
import sys
import types
import struct

@dataclass
class PreHeader:
    ByteOrder: bool
    Size:      int
    def __sizeof__(self):
        return (sys.getsizeof(self.ByteOrder) + sys.getsizeof(self.Size))
    def __str__(self):
        byte = 'little'
        if self.ByteOrder == 1:
            byte = 'big'
        return (str(sys.getsizeof(self)) + ' Bytes: PreHeader Size. (according to sys)\n' + 
                byte + ': Byte Order.\n' + 
                str(int.from_bytes(self.Size, byte)) + ' Bytes: Header Size. (according to PreHeader)\n')
    def GEN(header):
        ByteOrder = int(sys.byteorder == 'little') + 1
        Size      = struct.pack("I", sys.getsizeof(header))
        return PreHeader(ByteOrder, Size)

@dataclass
class PackageHeader:
    ContentLength: int
    ContentType:   type
    def __sizeof__(self):
        return (sys.getsizeof(self.ContentLength) + sys.getsizeof(self.ContentType))
    def __str__(self):
        return (str(sys.getsizeof(self)) + ' Bytes: Header Size. (according to sys)\n' + 
                str(self.ContentLength) + ' Bytes: Content Length. (according to Header)\n' + 
                self.ContentType + ': Content Type.\n')
                
    def GEN(content):
        ContentLength = sys.getsizeof(content)
        ContentType   = type(content)
        return PackageHeader(ContentLength, ContentType)

@dataclass
class Message:
    Pre:     PreHeader
    Header:  PackageHeader
    Content: object
    def __sizeof__(self):
        return (sys.getsizeof(self.Pre) + sys.getsizeof(self.Header) + sys.getsizeof(self.Content))
    def __str__(self):
        return (str(self.Pre) +
                str(self.Header) + 
                str(sys.getsizeof(self.Content)) + ' Bytes: Content Length. (according to sys)\n' + 
                str(self.Content) + ': Content.\n' + 
                str(sys.getsizeof(self)) + ' Bytes: Total Message Size. (according to sys)\n' +
                str(sys.getsizeof(self) - 16) + ' Bytes: Total Message Size. (minus 16 byte message class overhead)')
    def GEN(content):
        Header  = PackageHeader.GEN(content)
        Pre     = PreHeader.GEN(Header)
        Content = content
        return Message(Pre, Header, Content)

#mes = 'hello world'

#message = Message.GEN(mes)

#print (message)

#rs = input("Exited Error Code 0.")
