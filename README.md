# XML-to-Router-CFG
Convert an XML file to a text file. 

As an IT field engineer or an engineer working for a VAR, customers tend to want a lot of equipment configured in a short amount of time. This script helps elevate some of the hassle on accomplishing this. If you provide a PDF form to the customer for site information, each field will (should) have a unique name for the field. 

A little known feature with PDF files is the ablity to export the form into a XML format. By using the exported XML file the script will use the input names to look up the site specific information provided by the customer then create a config file to please into the router/switch/NetApp FAS, etc
