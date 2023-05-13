# TCP-Experiments
Performance Analysis of Various TCP Variants 

This repository presents a comprehensive analysis of different TCP variants and queuing algorithms under varied network conditions. The performance metrics considered in the study include throughput, packet drop rate, and latency. The TCP variants analyzed include Tahoe, Reno, NewReno, and Vegas, and the queuing algorithms investigated are RED and DropTail.
Repository Structure

The repository consists of the following:

   Source Code: This includes the network simulation scripts used for the experiments. The simulations are conducted using Network Simulator 2 (NS-2), a popular network simulation software.

   Data Analysis Scripts: Python scripts to parse and analyze the simulation data. The scripts use the Matplotlib library to generate insightful plots illustrating the performance of TCP variants and queuing algorithms under different conditions.

   Research Paper: A comprehensive research paper detailing the design of the experiments, the methodology followed, the results obtained, and the analysis of these results.

Key Findings

   1.TCP Vegas displayed superior performance in terms of throughput and latency under various load conditions.

   2.In terms of fairness, the same-protocol combinations (Reno-Reno, Vegas-Vegas) showed a high degree of fairness, while combinations of different protocols (e.g., Vegas-NewReno) demonstrated considerable unfairness due to their distinct congestion control mechanisms.

   3.The influence of queueing algorithms on network performance was considerable, with RED and DropTail showing differing performance under various conditions. The choice between RED and DropTail, and their combination with SACK, depends on the specific network requirements.

Usage

To run the simulations, use the Network Simulator 2 (NS-2) software. The results can be parsed and analyzed using the provided Python scripts.

This repository provides valuable insights into the performance of different TCP variants and queuing algorithms under varying network conditions. It demonstrates a strong understanding of networking concepts, proficiency in network simulation using NS-2, and data analysis skills using Python.
