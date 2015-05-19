Network eXperiment Tool (NeXT)

=== Introduction ===

This is a tool that implements an architecture proposed by Abel Souza in his final thesis entitled "Uma Arquitetura para Experimentos em Larga Escala de Redes P2P" and published on the 33rd Brazilian Symposium on Computer Networks and Distributed Systems.

Download the paper clicking on the following URL:

http://sbrc2015.ufes.br/wp-content/uploads/b-140485_1.pdf

=== REQUIREMENTS ===

This toold is based on GTK 3.10 (Gnome ToolKit). Other than that, you must have Python 2.7 and a Library called Paramiko (http://www.paramiko.org/installing.html).

The PlanetLab Analisys Tool is supposed to be supported by every major Unix environments although it was only tested on Linux's Operating Systems such as Ubuntu 14.04 .

= WARNING FOR THIS DOCUMENT =

IT MUST BE STATED THAT ALTHOUGH WE WILL USE THE SopCast APPLICATION TO ILLUSTRATE THE USE OF OUR TOOL, THIS TYPE OF APPLICATION MUST BE PROVIDED BY THE USER.

=== Using ===

In order to properly use this tool you must have a PlanetLab account configured with a password. Other than that, you should have one executable file for Nodes and another one for Monitors.

== Nodes ==

Nodes are the hosts which form a given network following a Torrent topology. These hosts usually connect to a server that will serve them with a set of nodes which they can then use to connect and consume a service of interest (an streaming media, for example). 

It must be stated that Nodes can do whatever they want, but they will all execute the same set of commands specified in an executable file.

== Monitors ==

Monitors are hosts which will act passively in the network formmed by the nodes. They are used in order to collect some packages and usually affects the network for a short time.

== The Tool ==

To open the tool, you only need to double click on the a 'panv.py' and execute it. You will need to login with you PlanetLab account.

Once you are logged, you will be presented with an interface in which you can use to configure everything. Perhaps the first thing you want to do is to select the private key provided by PlanetLab so you can retrieve all the node configured on you PlanetLab Slice.
You do that clicking on the 'PlanetLab' notetab (below the Stop Button) and then clicking on the chooser "Private-key file". Simple as that.

Once you configure the private-key, you can click on "Refresh List" to get the nodes from your Slice. Within this list, you must select
at least one Nodes and/or one Monitors. Select as many as you can. Notice that when a node is offline, a red icon is shown on its 'Status' column. Otherwise, an connected cable icon will be shown. This way you can select your monitors and nodes accordingly.


== Quick Setup ==

Refer to HOWTO file in order to execute an illustrative experiment.

== Options not working, yet ==

- Add Node;
- Delete Node;

They will be working as soon as possible. Meanwhile, you can execute these actions on the PlanetLab Website.
