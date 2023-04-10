if {[llength $argv] != 3} {
  puts "Usage: tclsh script_name.tcl <TCP Option> <TCP Option> <Queue Option>"
  exit
}
	set tcp_option_1 [lindex $argv 0]
	set tcp_option_2 [lindex $argv 1]
	set cbr_rate [lindex $argv 2]

	# Create output file name based on TCP option and CBR rate input
	set output_file "exp_2_${tcp_option_1}_${tcp_option_2}_${cbr_rate}.tr"

	#Making a NS Simulator
	global nf ns
	set ns [new Simulator]

	#Writing Trace data to file
	set nf [open $output_file w]
	$ns trace-all $nf

	#Creating the nodes
	set node1 [$ns node]
	set node2 [$ns node]
	set node3 [$ns node]
	set node4 [$ns node]
	set node5 [$ns node]
	set node6 [$ns node]

	#Creating the links between the nodes
	$ns duplex-link $node1 $node2 10Mb 10ms DropTail
	$ns duplex-link $node2 $node3 10Mb 10ms DropTail
	$ns duplex-link $node4 $node3 10Mb 10ms DropTail
	$ns duplex-link $node3 $node6 10Mb 10ms DropTail
	$ns duplex-link $node5 $node2 10Mb 10ms DropTail

	#Setting up the queue limit 
	$ns queue-limit $node2 $node3 10

	#Setting up a UDP connection from node node2 to node node3
	set udp [new Agent/UDP]
	$ns attach-agent $node2 $udp
	
	set udpsink [new Agent/Null]
	$ns attach-agent $node3 $udpsink
	$ns connect $udp $udpsink
	
	#Setting up CBR over UDP connection
	set cbr [new Application/Traffic/CBR]
	$cbr attach-agent $udp
	$cbr set type_ CBR
	$cbr set packet_size_ 1000
	$cbr set rate_ ${cbr_rate}mb
	$cbr set random_ false

	#Setting N1-N4 TCP
	set tcp_n1 [new Agent/TCP/$tcp_option_1]
	$ns attach-agent $node1 $tcp_n1
	set sink_n4 [new Agent/TCPSink]
	$ns attach-agent $node4 $sink_n4
	$ns connect $tcp_n1 $sink_n4
	#added below
	$tcp_n5 set fid_ 1
	
	#Setting N5-N6 TCP
	set tcp_n5 [new Agent/TCP/$tcp_option_2]
	$ns attach-agent $node5 $tcp_n5
	set sink_n6 [new Agent/TCPSink]
	$ns attach-agent $node6 $sink_n6
	$ns connect $tcp_n5 $sink_n6
	#added below 
	$tcp_n5 set fid_ 2
	
	#Setting up FTP ftp_option_1 over TCP Connectionode1 tcp_n1
	set ftp_option_1 [new Application/FTP]
	$ftp_option_1 attach-agent $tcp_n1
	$ftp_option_1 set type_ FTP

	#Setting up FTP ftp_option_2 over TCP Connection2 tcp_n5
	set ftp_option_2 [new Application/FTP]
	$ftp_option_2 attach-agent $tcp_n5
	$ftp_option_2 set type_ FTP

	#Start Times
	$ns at 0.1 "$cbr start"
	$ns at 0.2 "$ftp_option_1 start"
	$ns at 0.3 "$ftp_option_2 start"
	
	#End Times
	$ns at 10.2 "$ftp_option_1 stop"
	$ns at 10.3 "$ftp_option_2 stop"
	$ns at 10.4 "$cbr stop"
	$ns at 10.5 "$ns halt"

	$ns run


