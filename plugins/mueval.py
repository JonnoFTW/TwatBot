import subprocess
help = "Execute a haskell function"

def mueval(conn):
    try:
        src = ' '.join(conn.dataN['words'][1:])
    except:
        conn.sendMsg("Please specify a valud haskell statement")
        return
    args = ["/home/jonno/.cabal/bin/mueval-core","-E", "-XBangPatterns", "-XNoMonomorphismRestriction", "-XViewPatterns",     "--expression=" + src]
    print "cmd was"+ (' '.join(args))
    try:
        out = subprocess.check_output(args,stderr=subprocess.STDOUT).splitlines()
    except subprocess.CalledProcessError, e:
        out = e.output.splitlines()
    for i in out:
        conn.sendMsg(i)

triggers = {'^>':mueval}
