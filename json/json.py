import json

netConfig = {

    "node0": {  
        "id": "0",  
        "Power Type": "External",  
        "Energy": "2000",  
        "positionx": "150",
        "positiony":"100",
        "CH":"",
        "TDMA":"0",
        "sensor": "1"
    },  
    "node1": {  
        "id": "1",  
        "Power Type": "Battery",  
        "Energy": "2000",  
        "positionx": "10",
        "positiony":"10",
        "CH":"",
        "TDMA":"0",
        "sensor": "1"
    },
}

#json.dump(netConfig,open('data.txt', 'w'))

#out_file = open("myfile.json", "w") 
#json.dump(netConfig,)
#with open("netConfig.json", "w") as outfile: 
    #json.dump(netConfig, outfile) 

clusterConfig = {

    "cluster0":{
        "id" : "0",
        "nodes" :"",
        "CH" :"node0"
    }
    
}

#with open("clusterConfig.json", "w") as outfile: 
#    json.dump(clusterConfig, outfile) 



#0  with energy : <Power Type=External, Energy=2000 mJ>  with position 150.0 100.0 ; CH is [] is alive: True with TDMA 0 4
#1  with energy : <Power Type=Battery, Energy=1998 mJ>  with position 10 10 ; CH is [] is alive: True with TDMA 5 1998.26853125


# Opening JSON file 
#with open('clusterConfig.json', 'r') as openfile: 
  
    # Reading from json file 
    #json_object = json.load(openfile) 
  
#print(json_object) 
#print(type(json_object)) 



json_data = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
loaded_json = json.loads(json_data)


print("%s: %d" % (x, loaded_json[x]))