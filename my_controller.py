from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LearningSwitch(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed: return

        # Learn the MAC address of the sender
        self.mac_to_port[packet.src] = event.port

        # If we know the destination port, install a flow rule
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            
            # Create a flow modification message (Match-Action rule)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match(dl_dst=packet.dst, dl_src=packet.src)
            msg.actions.append(of.ofp_action_output(port=out_port))
            
            self.connection.send(msg)
            
            # Forward this specific packet out of the switch
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg)
            
        # If we don't know the destination, flood the packet
        else:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)

def launch():
    def start_switch(event):
        log.info("Controlling switch %s" % (event.connection,))
        LearningSwitch(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
