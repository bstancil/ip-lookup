ip-lookup
=================

A not-fast, not-perfect way to get geo information about your IPs. In particular, it returns county codes, which means you can make lovely US maps like this: https://modeanalytics.com/benn/reports/edfacef30130/results. 

##How it works

Make a CSV with one column that's a list of IP addresses. It doesn't clean out duplicates, so a deduped list is best.

Then, download all three files in this repo and put them in the same directory as the IP CSV. Navigate to that directory on your command line, and run this command:
    
    python ipLookup.py [source csv with IPs] [name of desired destination csv]

Boom, you now have a new file that includes geo information about all of the IPs. If no match for that IP was found (this occurs frequently), the row with that IP will be blank.

To make a map like the one above, add the output the CSV to your database such that it's joinable against an event stream or other dataset that has IP info. Join that table against your event stream table like the example found here: https://modeanalytics.com/benn/reports/f45cef4190e2/query

Copy the presentation code from that same query into your Mode presentation (this code: https://modeanalytics.com/benn/reports/f45cef4190e2/presentation)

Your new Mode report should now be an awesome map! https://modeanalytics.com/benn/reports/f45cef4190e2/results

IP lookup info from GeoLite by MaxMind: http://dev.maxmind.com/geoip/legacy/geolite/
