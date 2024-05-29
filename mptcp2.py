"""MPTCP Demo"""

import sys
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from time import sleep
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.wmediumdConnector import interference

def topology():

    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation(
        'sta1', wlans=2, ip='10.0.0.10/8', position='51,10,0' )
    ap2 = net.addAccessPoint(
        'ap2', mac='00:00:00:00:00:02', equipmentModel='TLWR740N',
        protocols='OpenFlow10', ssid= 'ssid_ap2', mode= 'n2',
        channel= '1', position='55,17,0' )
    ap3 = net.addAccessPoint(
        'ap3', mac='00:00:00:00:00:03', equipmentModel='TLWR740N',
        protocols='OpenFlow10', ssid= 'ssid_ap3', mode= 'g',
        channel= '6', position='50,11,0' )
    h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.254/8' )
    h5 = net.addHost( 'h5', mac='00:00:00:00:00:05', ip='192.168.0.254/24' )
    s6 = net.addSwitch( 's6', mac='00:00:00:00:00:06', protocols='OpenFlow10' )
    s7 = net.addSwitch( 's7', mac='00:00:00:00:00:07', protocols='OpenFlow10' )
    s8 = net.addSwitch( 's8', mac='00:00:00:00:00:08', protocols='OpenFlow10' )
    s9 = net.addSwitch( 's9', mac='00:00:00:00:00:09', protocols='OpenFlow10' )
    h10 = net.addHost( 'h10', mac='00:00:00:00:00:10', ip='192.168.1.254/24' )
    c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1' )

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap2, sta1, 0, 0)
    net.addLink(ap3, sta1, 0, 1)
    net.addLink(ap2, h4)
    net.addLink(ap3, h5)
    net.addLink(s6, h4)
    net.addLink(s6, h5)
    net.addLink(s6, s7)
    net.addLink(s6, s8)
    net.addLink(s7, s9)
    net.addLink(s8, s9)
    net.addLink(s9, h10)

    h4.cmd('ifconfig h4-eth1 192.168.1.1/24')
    h5.cmd('ifconfig h5-eth1 192.168.1.2/24')

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10/8')
    sta1.cmd('ifconfig sta1-wlan1 192.168.0.10/24')

    sta1.cmd('ip route add default 10.0.0.254/8 via sta1-wlan0')
    sta1.cmd('ip route add default 192.168.0.254/24 via sta1-wlan1')

    sta1.cmd('ip rule add from 10.0.0.10 table 1')
    sta1.cmd('ip rule add from 192.168.0.10 table 2')

    sta1.cmd('ip route add 10.0.0.0 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 192.168.0.0 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-wlan1 table 2')

    sta1.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta1-wlan0')

    info("*** Starting network\n")
 #   net.plotGraph(max_x=100, max_y=100)
 #   net.startMobility(time=1)
    net.build()
    c1.start()
    s6.start( [c1] )
    s7.start( [c1] )
    s8.start( [c1] )
    s9.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )

    h10.cmd('ip route add 10.0.0.0/8 via 192.168.1.1')
    h10.cmd('ip route add 192.168.0.0/24 via 192.168.1.2')

    h4.cmd('sysctl -w net.ipv4.ip_forward=1')
    h5.cmd('sysctl -w net.ipv4.ip_forward=1')
    

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
