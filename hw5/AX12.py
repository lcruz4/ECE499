def checksum(pktbytes):
  sum = 0
  newbytes=pktbytes[2:len(pktbytes)-1]
  for i in newbytes:
    sum +=  i
  pktbytes[len(pktbytes)-1]=~sum&255
  return pktbytes
def speedcmd(ID,speed):
  pktbytes=list()
  pktbytes.append(0xFF)
  pktbytes.append(0xFF)
  pktbytes.append(ID)
  pktbytes.append(0x05)
  pktbytes.append(0x20)
  if(speed<0):
    pktbytes.append((~speed+1)&0xFF)
    pktbytes.append(((~speed+1)>>8)&0x3)
  else:
    pktbytes.append(speed&0xFF)
    t = ((speed>>8)&0x3)
    t |= 0x4
    pktbytes.append(t)
  pktbytes.append(0)
  return checksum(pktbytes)
