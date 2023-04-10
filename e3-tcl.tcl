if {[llength $argv] != 3} {
  puts "Usage: tclsh script_name.tcl <TCP Option> <Queue Option> <Queue Limit Option>"
  exit
}

set tcp_option [lindex $argv 0]
set queue_option [lindex $argv 1]
set queue_limit_option [lindex $argv 2]

# Create output file name based on TCP option and CBR rate input
set output_file "exp_3_${tcp_option}_${queue_option}_${queue_limit_option}.tr"

global nf ns
set ns [new Simulator]

#Writing Trace data to file
set nf [open $output_file w]             
$ns trace-all $nf

set node1 [$ns node] 
set node2 [$ns node]
set node3 [$ns node]
set node4 [$ns node]
set node5 [$ns node]
set node6 [$ns node]

$ns duplex-link $node1 $node2 10Mb 10ms $queue_option
$ns duplex-link $node5 $node2 10Mb 10ms $queue_option
$ns duplex-link $node2 $node3 10Mb 10ms $queue_option
$ns duplex-link $node3 $node4 10Mb 10ms $queue_option
$ns duplex-link $node3 $node6 10Mb 10ms $queue_option

#setting queue limit 
$ns queue-limit $node2 $node3 $queue_limit_option

#setting topology 
$ns duplex-link-op $node1 $node2 orient right-down
$ns duplex-link-op $node5 $node2 orient right-up
$ns duplex-link-op $node2 $node3 orient right
$ns duplex-link-op $node4 $node3 orient left-down
$ns duplex-link-op $node6 $node3 orient left-up

#UDP connection (n5-n6)
set udp [new Agent/UDP]
$ns attach-agent $node5 $udp
set udpsink [new Agent/Null]
$ns attach-agent $node6 $udpsink
$ns connect $udp $udpsink

$udp set fid_ 2

#Setting the CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set rate_ 5mb 
#7mb? ^

#TCP connection (n1-n4)
set tcp [new Agent/TCP/$tcp_option]
if {$tcp_option == "Reno"} {
		 set sink [new Agent/TCPSink]
	}
if {$tcp_option == "Sack1"} {
		 set sink [new Agent/TCPSink/Sack1]
	}
$ns attach-agent $node1 $tcp
$ns attach-agent $node4 $sink
$ns connect $tcp $sink	

#Setting up a FTP over TCP connection to generate traffic
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP



#start time
#$ns at 0.1 "$cbr start"
#$ns at 0.2 "$ftp start"


#end times 
#$ns at 10.1 "$cbr stop"
#$ns at 10.2 "$ftp stop"
#$ns at 10.3 "$ns halt"

#start time
$ns at 0.1 "$ftp start"
$ns at 4.0 "$cbr start"



#end times 
$ns at 10.1 "$cbr stop"
$ns at 10.2 "$ftp stop"
$ns at 10.3 "$ns halt"


$ns run