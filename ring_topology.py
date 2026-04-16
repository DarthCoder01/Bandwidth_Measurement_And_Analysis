from mininet.topo import Topo

class RingTopo(Topo):
    def build(self):
        # 1. Add the 3 Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # 2. Add the 6 Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        # 3. Connect the Switches together (Forming the Ring)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

        # 4. Connect the Hosts to their respective Switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        
        self.addLink(h5, s3)
        self.addLink(h6, s3)

# This line lets Mininet recognize the topology name via the command line
topos = { 'ringtopo': (lambda: RingTopo()) }
