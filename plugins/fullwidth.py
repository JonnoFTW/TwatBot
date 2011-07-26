# coding=utf-8
help = u"Converts string to glorious Ｆ Ｕ Ｌ Ｌ ＀ Ｗ Ｉ Ｄ Ｔ Ｈ"

def convert(conn):
    try:
        fool = ''.join(conn.dataN['words'][1:])
        out = u''
        for i in fool:
            if i == ' ':
                out += unichr(0x3000)
            else:
                out += unichr(ord(i)+0xfee0)
        conn.sendMsg(out,conn.dataN['chan'])
    except IndexError, e:
        conn.sendMsg('Please provide a string',conn.dataN['chan'])
        return

triggers = { '^full':convert}
