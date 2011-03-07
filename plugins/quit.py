
def exit(conn):
    conn.close()
    
triggers = {'^quit':exit,'^exit':exit}
