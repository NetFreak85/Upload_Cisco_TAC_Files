#!/usr/local/bin/python3.9

#***********************************#
#                                   #
#   --usage:                        #
#             ./Upload.py           #
#         or  python Upload.py      #
#                                   #
# date:  28/06/2022 Created         #
#***********************************#

##################
# Import Section #
##################

import argparse
import requests
from requests.auth import HTTPBasicAuth

#############
# Variables #
#############

#Variable that allow verbose mode
Verbose_Mode = False

#########################
# Functions Declaration #
#########################

#Defining the Argument function that allow the verbose mode
def get_args():
    parser = argparse.ArgumentParser()

    #Method that enable verbose mode
    parser.add_argument('-v',
                        help='Verbose mode',
                        action='store_true',
                        required=False)

    #Method that capture the Cisco Case Number
    parser.add_argument('-c', '--case',
                        help='Cisco Case Number',
                        action='store_true',
                        required=True)

    #Method that capture the Cisco Case Token
    parser.add_argument('-t', '--token',
                        help='Cisco Case Token Number',
                        action='store_true',
                        required=True)

    #Method that capture the Cisco Case Token
    parser.add_argument('-f', '--filepath',
                        help='File Path',
                        action='store_true',
                        required=True)

    return parser.parse_args()

#Function that upload the file in the Cisco Cloud
def upload_Tac_File(SR_Ticket,Token, Filename):

    #Return the result of the upload file
    Upload_Result = True

    #Cisco TAC URL
    URL = "https://cxd.cisco.com/home/"

    #Get authentication with the SR Ticket Number and Case Token
    auth = HTTPBasicAuth(SR_Ticket, Token)

    #We open the file with the commands results
    f = open(Filename, 'rb')

    #Upload the file to Cisco Cloud
    r = requests.put(URL + Filename, f, auth=auth, verify=False)
    
    #Close the request & file
    r.close()
    f.close()

    #Check the request status code
    if r.status_code == 201:
        Upload_Result = True
    else:
        Upload_Result = False

    return Upload_Result, r.status_code

#Main program Function
def main():

    #Boolean variable that check if the uploading was Successfully or not
    Upload_Result = True

    #Variable that will store the results of the Query HTTP Response code
    HTTP_Response_Code = 0

    #Variable that enable or not the verbose mode
    global Verbose_Mode

    #Class that evaluate arguments in the script
    args = get_args()

    #Check if verbose mode is enable 
    if args.v:
        Verbose_Mode = True

    #Print into the console the uploading start process
    if Verbose_Mode:
        print("Uploading File into the Cisco Case")

    #Upload the file storage in argument F into the Cisco Case
    Upload_Result, HTTP_Response_Code = upload_Tac_File(args.c, args.t, args.f)

    #If we enable verbose mode we print into the console the result of the uploading and the http error (if the upload fail)
    if Verbose_Mode:

        #Print over console if the upload was Successfully
        if Upload_Result:
            print("File " + args.f + " Uploaded Successfully")
        
        #Print the error msg received
        else:
            print ("HTTP Response code: " + HTTP_Response_Code)

################
# Main Program #
################

if __name__ == '__main__':
    exit(main())