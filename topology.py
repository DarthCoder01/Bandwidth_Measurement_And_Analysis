from mininet.topo import Topo

class CustomTopo(Topo):
    "Custom Topology: 2 Switches, 4 Hosts"

    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Link hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)

        # Link switches to each other
        self.addLink(s1, s2)

# This dictionary allows Mininet to find your topology via the command line
topos = {'customtopo': (lambda: CustomTopo())}
