#!/usr/bin/env python

import pygeoip
import csv
import re
import string
import sys
import os

# Function for writing output to csv
def write_to_csv(csv_name,array):
    columns = len(array[0])
    rows = len(array)
    
    with open(csv_name, "wb") as test_file:
        file_writer = csv.writer(test_file)
        for i in range(rows):
            file_writer.writerow([array[i][j] for j in range(columns)])

# Function to read list
def read_list(csv_name):
    table = []
    
    with open(csv_name, 'Ub') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        print f
        
        for row in f:
            table.append(row[0])
    return table

# Function to read hometown table and 
# output array and array key
def read_table(csv_name):
    table = []
    keys = []
    
    with open(csv_name, 'Ub') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        
        for row in f:
            table.append(row)
            keys.append(row[0]+row[1])
            
    return (table,keys)

# Strips special characters in hometowns
def strip_special(array,columns_with_string):
    new_table = []
    for i in array:
        new_row =[]
        for j in range(len(i)):
            if j in columns_with_string:
                if i[j] != None:
                    x = i[j].encode('utf-8').strip()
                else:
                    x = i[j]
            else:
                x = i[j]
            new_row.append(x)
            
        new_table.append(new_row)
    
    return new_table

# Looks up county and state codes
def county_lookup(city,state,key_list,hometown_table):
    key = city + state
    n = key_list.index(key)
    
    try:
        row = hometown_table[n]
    except:
        row = ['','']
    
    state_code = row[2]
    county_code = row[3]
    
    return (state_code,county_code)

## SCRIPT ##

# Get inputs
ip_list = sys.argv[1]

ips = read_list(ip_list)
total_ips = len(ips)

print 'Found %i IP addresses...' % (total_ips)

# Read lookup data
gips = pygeoip.GeoIP('GeoLiteCity.dat')

town_matching = read_table('city_matching.csv')
town_obj = town_matching[0]
town_key = town_matching[1]

# Create result array and add header
result = []
header = ('ip_address','city','region_code','area_code','metro_code','country_code',
    'postal_code','latitude','longitude','state_code','county_code')
result.append(header)

# Loop over and look up IPs
print 'Looking up IPs...'

for idx, val in enumerate(ips):    
    try:
        info = gips.record_by_addr(val)
        
        if info != None:
            
            city = info['city']
            region_code = info['region_code']
            area_code = info['area_code']
            metro_code = info['metro_code']
            country_code = info['country_code']
            postal_code = info['postal_code']
            latitude = info['latitude']
            longitude = info['longitude']
            
            county = county_lookup(city,region_code,town_key,town_obj)
            state_code = county[0]
            county_code = county[1]
            
            entry = (val,city,region_code,area_code,metro_code,country_code,
                postal_code,latitude,longitude,state_code,county_code)
            
        else:
            entry = (val,'','','','','','','','','','')
    
    except:
        entry = (val,'','','','','','','','','','')
    
    result.append(entry)
    
    if idx % 1000 == 0 and idx != 0:
        print '%i out of %i IP addresses have been looked up so far...' % (idx, total_ips)

# Clean output and write to csv
print 'Cleaning up...'

clean = strip_special(result,[1])

output_file = sys.argv[2]
write_to_csv(output_file,clean)

print 'Done!'

            