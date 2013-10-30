"""
This is a script designed to run on a Profitbricks image.

Profitbricks does no have the capability of having its new Node's metadata
tags set up by the instantiator of the Node.  This means that it is
necessary for the new Profitbricks instance to proactively fetch its
configuration data using its uniquely configured Hostname as the
identifying tag.

This script fetches the configuration data and stores the results
into the output file specified (or to stdout by default).

This script is invoked as follows:

python pbGetConfig.py dbaasAddress dbaasPort# [outputFilename]
"""
import os, sys
import socket
import urllib2

def main(baseUrl, filename):
    """
    Fetch the contents at the base URL specified,
    adding the current hostname as a parameter tag,
    and preserve the fetched contents into the output
    file named: filename.
    """
    hostname = socket.gethostname()
    print("hostname=%s" % hostname)
    response = urllib2.urlopen(baseUrl + hostname + '/')
    #print response.info()
    html = response.read()
    if filename:
        open(filename, 'wb').write(html)
    else:
        print html
    response.close()  # best practice to close the file

if __name__ == '__main__':
    #baseUrl = 'http://localhost:8000/api/cloud_config_by_hostname/'
    url_hdr = 'http://'
    #url_port= '8000'
    url_dir = '/api/cloud_config_by_hostname/'
    outputFilename = None
    if len(sys.argv) > 2:
        url_host = sys.argv[1]
        url_port = sys.argv[2]
        if len(sys.argv) > 3:
            outputFilename = sys.argv[3]
    else:
        print("Usage: %s dbaasHost dbaasPort# [outputFilename]" % sys.argv[0])
        sys.exit(1)
    baseUrl = url_hdr + url_host + ":" + url_port + url_dir
    main(baseUrl, outputFilename)

