### Desc: This script retrieve details from excel files and use the information to generate xml config file for mtputty.
### This script is useful if you have many VMs to be onboarded to mtputty.


#Defining libraries to be used
import pandas as pd

#Step 1: Defining Excel file to get data from.
rawdata = pd.read_excel (r'C:\Users\foldername\excelfilename.xlsx')

#Defining column to be used in Pandas DataFrame
df = pd.DataFrame(rawdata, columns= ['S/N','Environment','MachineType','OS Version','IP Address','Layer','ShortDesc'])

###############################TAGS##############################
##########Creating tags to be used in code generation############
#Opening tags
header_open = '<?xml version="1.0" encoding="UTF-8"?>'
header_server_open = '<Servers>'
header_putty_open = '<Putty>'
header_node_master_open = '<Node Type="0">'
header_node_child_open = '<Node Type="1">'
header_displayname_open='<DisplayName>'
body_savedsession_open='<SavedSession>'
#For UID, incremental counter, using mod 16, and close with }
body_uid_open='<UID>'
body_uid='{00000000-0000-0000-0000-'
body_servername_open='<ServerName>'
body_puttycontype_open='<PuttyConType>'
body_port_open='<Port>'
body_username_open='<UserName>'
body_password_open='<Password>'
body_passworddelay_open='<PasswordDelay>'
body_clparams_open='<CLParams>'
body_scriptdelay_open='<ScriptDelay>'
tab="\t"

#Closing tags
header_server_close = '</Servers>'
header_putty_close = '</Putty>'
header_node_master_close = '</Node>'
header_displayname_close='</DisplayName>'
body_savedsession_close='</SavedSession>'
body_uid_close='</UID>'
body_servername_close='</ServerName>'
body_puttycontype_close='</PuttyConType>'
body_port_close='</Port>'
body_username_close='</UserName>'
body_password_close='</Password>'
body_passworddelay_close='</PasswordDelay>'
body_clparams_close='</CLParams>'
body_scriptdelay_close='</ScriptDelay>'

#################################################################
f = open(r"C:\Users\foldername\mtputtyfilename.xml", "w")
###Header creation###
f.write(header_open + '\n')
f.write(header_server_open + '\n')
f.write(tab + header_putty_open + '\n')

####UAT App Tier####
#Excel Filter condition
df_uat_rhel=(df.loc[(df['Environment'] == "UAT") & (df['MachineType'] == "Virtual VM") & (df['OS Version'] == "RHEL 8.x") & (df['Layer'] == "App")])
#iloc length calculation
df_uat_rhel_len=len(df_uat_rhel.index)

# Start of Folder #
var_curenv=(df_uat_rhel.iloc[0,1])
var_curosversion=(df_uat_rhel.iloc[0,3])
f.write(tab + tab + header_node_master_open + '\n')
f.write(tab + tab + tab + header_displayname_open + var_curenv + "_App_" + var_curosversion + header_displayname_close + '\n')

# Assigning value to current dataframe variable to generate the value for the current entry
for counter in range(df_uat_rhel_len):
    var_sn=(df_uat_rhel.iloc[counter,0])
    var_env=(df_uat_rhel.iloc[counter,1])
    var_machinetype=(df_uat_rhel.iloc[counter,2])
    var_osversion=(df_uat_rhel.iloc[counter,3])
    var_ipaddress=(df_uat_rhel.iloc[counter,4])
    var_layer=(df_uat_rhel.iloc[counter,5])
    var_shortdesc=(df_uat_rhel.iloc[counter,6])

    ## Start of Sub-Folder (Begin looping based on number of VMs.##
    f.write(tab + tab + tab + header_node_child_open + '\n')
    f.write(tab + tab + tab + tab + body_savedsession_open + 'Default Settings' + body_savedsession_close + '\n')
    f.write(tab + tab + tab + tab + header_displayname_open + str(var_sn).zfill(4) + '_' + var_layer + '_' + var_shortdesc + '_' + var_ipaddress + header_displayname_close + '\n')
    final_sn= "{00000000-0000-0000-0000-00000000" + str(var_sn).zfill(4) + "}"
    f.write(tab + tab + tab + tab + body_uid_open + final_sn + body_uid_close + '\n')
    f.write(tab + tab + tab + tab + body_servername_open + var_ipaddress + body_servername_close + '\n')
    f.write(tab + tab + tab + tab + body_puttycontype_open + '4' + body_puttycontype_close + '\n')
    f.write(tab + tab + tab + tab + body_port_open + '22' + body_port_close + '\n')
    f.write(tab + tab + tab + tab + body_username_open + body_username_close + '\n')
    f.write(tab + tab + tab + tab + body_password_open + body_password_close + '\n')
    f.write(tab + tab + tab + tab + body_passworddelay_open + '0' + body_passworddelay_close + '\n')
    f.write(tab + tab + tab + tab + body_clparams_open + var_ipaddress + ' -ssh -P 22' + body_clparams_close + '\n')
    f.write(tab + tab + tab + tab + body_scriptdelay_open + '0' + body_scriptdelay_close + '\n')
    f.write(tab + tab + tab + header_node_master_close + '\n')

f.write(tab + tab + header_node_master_close + '\n')

######################################################################################################################

## Close header
f.write(tab + header_putty_close + '\n')
f.write(header_server_close + '\n')


## Close file after completion##
f.close()

print("Script completed running...")

