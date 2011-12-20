help = "Rehab is for quitters"
def exit(conn):
    conn.conn.quitting = True
    conn.close()
    
triggers = {'^quit':exit,'^exit':exit}
