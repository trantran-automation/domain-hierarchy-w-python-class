# domain-hierarchy-w-python-class
A short script to demonstrate a convince way to define domain name hierarchy with python class.
This project is for people who work with a lot of domain syntax like /root/amr/action/.. like in ROS and MQTT.
If you tired of have to remember every domain, sub domain, here is a way to help you define it easy, robust, friendly with Pylance, code hint

## Feature:
- Create a domain class to handle domain name hierarchy instead of pure string
- Help you define a hierarchy tree of domain name with python nested class.
- Allow custom, dynamic local domain name when define the tree
- Has a "is_parent_of" method to match sub domain, peer domain with a domain in str form

# Usage
- just define your tree like example in script
- import the tree anywhere with syntax "from domain_hierachy import DomainTree"
- This project use "string orientation" for the domain define so you should init it first at the start of the script where you use it.
- To define your tree, nested subdomain to parent domain like i did.
- Look at the tree example i made in the file domain_hierachy.py

