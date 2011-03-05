def help(dataN):
    sendMsg("""Send the the line preceeding ^^ to @Buttsworth_ on 
            twitter. Most recent update with ^last. View channels
            with ^chans. http://twitter.com/#!/Buttsworth_"""
            ,dataN['chan'])
triggers = { '^help':help,'^about':help}
