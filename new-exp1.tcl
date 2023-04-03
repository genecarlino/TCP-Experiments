if {[llength $argv] != 2} {
  puts "Usage: tclsh script_name.tcl <TCP Option> <CBR Rate>"
  exit
}

set tcp_option [lindex $argv 0]
set cbr_rate [lindex $argv 1]

# Create output file name based on TCP option and CBR rate input
set output_file "exp_1_${tcp_option}_${cbr_rate}.tr"

#can we get rid of global ns?
global nf ns
set ns [new Simulator]
set nf [open $output_file w]             
$ns trace-all $nf

set node1 [$ns node] 
set node2 [$ns node]
set node3 [$ns node]
set node4 [$ns node]
set node5 [$ns node]
set node6 [$ns node]

$ns duplex-link $node1 $node2 10Mb 10ms DropTail
$ns duplex-link $node5 $node2 10Mb 10ms DropTail
$ns duplex-link $node2 $node3 10Mb 10ms DropTail
$ns duplex-link $node3 $node4 10Mb 10ms DropTail
$ns duplex-link $node3 $node6 10Mb 10ms DropTail

$ns queue-limit $node2 $node3 10

#setting topology 
$ns duplex-link-op $node1 $node2 orient right-down
$ns duplex-link-op $node5 $node2 orient right-up
$ns duplex-link-op $node2 $node3 orient right
$ns duplex-link-op $node4 $node3 orient left-down
$ns duplex-link-op $node6 $node3 orient left-up




if {$tcp_option == "Tahoe"} {
        set tcp [new Agent/TCP]
    } else {
        set tcp [new Agent/TCP/$tcp_option]
    }

$ns attach-agent $node1 $tcp


set sink [new Agent/TCPSink]
$ns attach-agent $node4 $sink

$ns connect $tcp $sink
$tcp set fid_ 1

set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

   
set udp [new Agent/UDP] 
$ns attach-agent $node2 $udp
set udpsink [new Agent/Null]
$ns attach-agent $node3 $udpsink
$ns connect $udp $udpsink
$udp set fid_ 2

set cbr [new Application/Traffic/CBR] 
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packetSize_ 1000
$cbr set rate_ ${cbr_rate}mb  
$cbr set random_ false 


$ns at 0.1 "$cbr start"
#$ns at 0.5 "$ftp start" 
$ns at 0.2 "$ftp start" 
#adjust times as needed 
# $ns at 9.0  "$ftp stop"
# $ns at 9.5 "$cbr stop"
$ns at 20.2  "$ftp stop"
$ns at 20.3 "$cbr stop"

proc clear_cash {} {
        global nf ns
        $ns flush-trace
        close $nf
        exit 0
    }
$ns at 10.0 "clear_cash"

$ns run