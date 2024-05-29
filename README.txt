File mptcp2.py là topology của SD-VANET nhưng chưa enable MPTCP
Để enable MPTCP, chạy file "1.v0.95.2_mptcp_configuration.bash" để boot multipath TCP vào trong kernel của linux
./pox.py forwarding.l2_learning openflow.spanning_tree --hold-down log.level --DEBUG samples.pretty_log openflow.discovery host_tracker info.packet_dump