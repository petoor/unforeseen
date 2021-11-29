from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.database import InfluxDB
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.onprem.client import Client, User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Ansible
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom

# Custom icons  are made by the users 
# 714, 3, 8908, 714 and 3277 @ freeicons.io
# Some icons have slight modifications

name = "Unforseen"
analysis_icon = "./icons/analysis-128.png"
machine_icon = "./icons/conveyor-128.png"
cloud_icon = "./icons/cloud-128.png"
camera_icon = "./icons/camera-128.png"
cvat_icon = "./icons/cvat-128.png"

graph_attr = {
    "fontsize": "25",
    "bgcolor": "transparent",
    "fontname": "bold"
}

for outputformat in ["png"]:
    with Diagram(f"{name} Infrastructure", outformat=outputformat, show=False, graph_attr=graph_attr):
        output_machine = Custom("Industry machine", machine_icon)
        
        with Cluster("Unforeseen Server"):
            with Cluster("Server and monitoring"):
                grafana = Grafana("Grafana")
                influxdb = InfluxDB("InfluxDB")
                prometheus = Prometheus("Prometheus")	
                cvat = Custom("CVAT", cvat_icon)

        with Cluster("Unforeseen Client"):
            with Cluster("Image Analysis"):
                device = Custom("Camera \n SBC", camera_icon)
                events = Custom("Image Analysis", analysis_icon)         
                camerafeed = Server("Camera feed \n server")

            with Cluster("Storage"):
                cloud = Custom("Cloud Storage", cloud_icon)
                local = Storage("Local Storage")
         
        user = User("User")               
        #with Cluster("Remote"):
        #    github = Github(f"{name} Reposotory \n Costumer Fork")
        #    ansible = Ansible("Ansible")
 

          
        output_machine << Edge(color="red",style="dotted",label="Machine output signal") << device
        influxdb >> grafana << user
        device >> camerafeed >>  grafana
        events >> Edge(label="Metrics") >> influxdb
        device >> events
        device >> events
        device >> prometheus
        prometheus >> grafana
        user >> cvat
        #grafana << ansible
        #ansible << github
        
        device >> local
        local - Edge(label="If Cloud sync/backup enabled") >> cloud

