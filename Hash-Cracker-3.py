#!/usr/local/bin/python
# Change the above path to where Python is installed on your system
# Use the 'which python' command to find the path for you

import StringIO
import getopt
import hashlib
import sys
import os
import time

def help():
    print "ZEUS-CRACK - A command-line hash cracker"
    print " "
    print "Supported Hash Types: (-t option)"
    print "md5, sha1, sha224, sha256, sha384, sha512"
    print "Options: -h (Hash) -t (Hash Type) -w (Wordlist) -v (Verbose)"
    print " "
    print "Example usage: ./Zeus-Cracker.py -h <hash> -t md5 -w file.txt"

def example():
    print 'Example usage: ./Zeus-Cracker.py -h <hash> -t md5 -w file.txt'
    print 'Use -H for full help information'

def invalidhashtype():
    print "ERROR: Unsupported hash type specified."

def unsuccessful():
    print "UNSUCCESSFUL: Hash not found in Wordlist."

class hCrack:
    
    def hCrackWordlist(self, uHash, hType, wordlist, verbose):
        start = time.time()
        self.lineCount = 0
        if (hType == "md5"):
            h = hashlib.md5
        elif (hType == "sha1"):
            h = hashlib.sha1
        elif (hType == "sha224"):
            h = hashlib.sha224
        elif (hType == "sha256"):
            h = hashlib.sha256
        elif (hType == "sha384"):
            h = hashlib.sha384
        elif (hType == "sha512"):
            h = hashlib.sha512
        else:
            invalidhashtype()
            exit()
        with open(wordlist, "rU") as infile:
            for line in infile:
                line = line.strip()
                lineHash = h(line).hexdigest()
                if (verbose == True):
                    sys.stdout.write('\r' + str(line) + ' ' * 20)
                    sys.stdout.flush()

                if (str(lineHash) == str(uHash.lower())):

                    Result = open('ZeusCrack-result.txt', 'a+')
                    Result.write('%s : {}'.format(lineHash) % line)
                    Result.write('\n')
                    Result.close()

                    end = time.time()
                    print "Hash is: %s" % line
                    print "Words tried: %s" % self.lineCount
                    print "Time: %s seconds" % round((end - start), 2)
                    print "Hash saved in: ZeusCrack-result.txt"
                    exit()
                else:
                    self.lineCount = self.lineCount + 1
        end = time.time()
        print "Cracking Failed"
        print "Reached end of wordlist"
        print "Words tried: %s" % self.lineCount
        print "Time: %s seconds" % round((end - start), 2)
        exit()

    def hCrackNumberBruteforce(self, uHash, hType, verbose):
        start = time.time()
        self.lineCount = 0
        if (hType == "md5"):
            h = hashlib.md5
        elif (hType == "sha1"):
            h = hashlib.sha1
        elif (hType == "sha224"):
            h = hashlib.sha224
        elif (hType == "sha256"):
            h = hashlib.sha256
        elif (hType == "sha384"):
            h = hashlib.sha384
        elif (hType == "sha512"):
            h = hashlib.sha512
        else:
            invalidhashtype()
            exit()
        while True:
            line = "%s" % self.lineCount
            line.strip()
            numberHash = h(line).hexdigest().strip()
            if (verbose == True):
                sys.stdout.write('\r' + str(line) + ' ' * 20)
                sys.stdout.flush()
            if (numberHash.strip() == uHash.strip().lower()):
                end = time.time()
                print "Hash specified: %s" % lineCount
                print "Time: %s seconds" % round((end - start), 2)
                break
            else:
                self.lineCount = self.lineCount + 1

def main(argv):
    hType = uHash = wordlist = verbose = numbersBruteforce = None
    try:
        opts, args = getopt.getopt(argv, "Hh:t:w:nv", ["ifile=", "ofile="])
    except getopt.GetoptError:
        example()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-H':
            help()
            sys.exit()
        elif opt in ("-t", "--type"):
            hType = arg
        elif opt in ("-h", "--hash"):
            uHash = arg
        elif opt in ("-w", "--wordlist"):
            wordlist = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-n", "--numbers"):
            numbersBruteforce = True
    if not (hType and uHash):
        example()
        sys.exit()

    # Checks through saved hashfile instead of processing Wordlist 
    with open('ZeusCrack-result.txt', 'w+') as ResultsFile:
        for HASH in ResultsFile:
            HASH = HASH.strip().split(" : ")
            if uHash.lower() == HASH[1]:
                print "Cracked Hash is: %s" % HASH[0]
                sys.exit()
        else:
            print "Hash: %s" % uHash
            print "Hash type: %s" % hType
            print "Wordlist found: %s" % wordlist
            print "Processing Wordlist..."
            try:
                h = hCrack()
                if (numbersBruteforce == True):
                    h.hCrackNumberBruteforce(uHash, hType, verbose)
                else:
                    h.hCrackWordlist(uHash, hType, wordlist, verbose)

            except IndexError:
                unsuccessful()
                print "Words tried: %s" % h.lineCount

            except KeyboardInterrupt:
                print "Quitting"
                print "Words tried: %s" % h.lineCount

            except IOError:
                print "ERROR: Wordlist %s not found." % wordlist

if __name__ == "__main__":
    main(sys.argv[1:])