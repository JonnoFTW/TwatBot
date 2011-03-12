help = "Rehab is for quitters"
def exit(conn):
    conn.close()
    
triggers = {'^quit':exit,'^exit':exit}
