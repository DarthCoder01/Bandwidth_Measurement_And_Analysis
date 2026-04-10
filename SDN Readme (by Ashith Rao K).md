Markdown

````
# SDN Mininet Simulation - Layer 2 Learning Switch

## Problem Statement
The objective of this project is to implement a Software-Defined Networking (SDN) solution using Mininet and the POX OpenFlow controller. The project demonstrates controller-switch interaction, OpenFlow match-action rule design, and network behavior observation. Additionally, the project includes bandwidth measurement and performance analysis across different network topologies using `iperf`.

## Project Structure
* `topology.py`: A Python script defining a custom Mininet topology consisting of 2 switches and 4 hosts.
* `my_controller.py`: A Python script for the POX controller that implements a Layer 2 learning switch logic, handling `PacketIn` events and installing `FlowMod` rules.

## Setup and Execution Steps

### Prerequisites
* Ubuntu Linux Environment
* Mininet (`sudo apt install mininet`)
* POX Controller (`git clone https://github.com/noxrepo/pox`)

### Execution

**1. Start the POX Controller**
Open a terminal, navigate to your POX directory, and run the custom controller script:
```bash
cd pox
python3 pox.py my_controller
````

**2. Start Mininet with Custom Topology**

Open a second terminal, navigate to the project directory containing `topology.py`, and launch Mininet connected to the remote POX controller:

Bash

```
sudo mn --custom topology.py --topo customtopo --controller remote,ip=127.0.0.1,port=6633 --switch ovsk
```

**3. Verify Connectivity**

Inside the Mininet CLI, run a ping test to verify the learning switch logic is actively routing traffic:

Bash

```
mininet> pingall
```

## Expected Output

- The POX controller terminal will log successful connections to `s1` and `s2`.
    
- The `pingall` command will return **0% dropped packets**, confirming functional correctness.
    
- Running `dpctl dump-flows` in the Mininet CLI immediately after the ping test will display the OpenFlow match-action rules dynamically installed by the controller.
    

## Performance Observation & Analysis

To analyze network performance, TCP throughput was measured using `iperf` across two different scenarios.

**Methodology:**

- Server started on `h1` (`h1 iperf -s &`)
    
- Client traffic sent to `h1` from different hosts in the topology.
    

**Results:**

1. **Intra-Switch Communication (`h2` to `h1`):** Both hosts are connected to switch `s1`.
    
    - **Observed Bandwidth:** ~74.1 Gbits/sec
        
2. **Inter-Switch Communication (`h3` to `h1`):** Traffic must cross the link connecting switch `s2` to switch `s1`.
    
    - **Observed Bandwidth:** ~70.7 Gbits/sec
        

**Analysis:**

The throughput is highest when hosts communicate on the same switch, as the traffic is processed by a single datapath. When communicating across switches (h3 to h1), the bandwidth decreases. This is because the traffic must be processed by `s2`, transmitted across the physical link connecting the two switches, and then processed again by `s1`. This extra network hop and shared switch-to-switch link act as a slight bottleneck, introducing processing overhead that reduces the overall TCP throughput.

## Proof of Execution

1. **Initial Mininet Setup & Validation** This screenshot demonstrates the successful launch of Mininet using the default topology to verify that the base emulator installation is functioning correctly. It confirms the creation of the fundamental network components—such as hosts, switches, and links—while successfully initializing the Mininet command-line interface for further testing.
![[Screenshot from 2026-04-09 19-48-07.png]]


2.  The Custom Topology Initialization
![[Screenshot from 2026-04-09 20-00-57.png]]
Execution of the custom Python topology script (`topology.py`). Demonstrates the successful creation of 2 OpenFlow switches and 4 hosts, verified by an initial baseline connectivity test.


3. Controller Connection
![[Screenshot from 2026-04-09 20-29-37.png]]
Initialization of the custom POX controller script (`my_controller.py`). The log confirms the control plane successfully listening and connecting to the Mininet data plane switches (00-00-00-00-00-01 and 00-00-00-00-00-02).

4. Functional Correctness via Remote Controller
![[Screenshot from 2026-04-09 20-30-03.png]]
Data plane routing verification. Mininet is launched with the remote POX controller. The `pingall` command results in 0% dropped packets, proving the Layer 2 learning switch logic is correctly handling and routing `PacketIn` events.

5. OpenFlow Match-Action Rules & Controller Interaction
![[Screenshot from 2026-04-09 22-20-52.png]]
Proof of explicit flow rule implementation. The top panel (Wireshark) captures the OpenFlow `OFPT_FLOW_MOD` messages sent by the controller. The bottom panel (`dpctl dump-flows`) confirms these match-action rules (source MAC, destination MAC, and output port) were successfully installed into the hardware flow tables of switches s1 and s2.

6. Performance & Bandwidth Analysis
![[Screenshot from 2026-04-09 22-37-06.png]]
Throughput testing using `iperf`. Demonstrates a bandwidth of 74.1 Gbits/sec for intra-switch communication (h2 to h1 on s1), compared to a reduced bandwidth of 70.7 Gbits/sec for inter-switch communication (h3 to h1), highlighting the performance impact of multi-hop network topologies.