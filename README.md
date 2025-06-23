# Genetis RHINO

Uses Genetic Algorithms to find optimum beam patterns for the RHINO horn. See [https://arxiv.org/abs/2410.00076](https://arxiv.org/abs/2410.00076) for information about RHINO.

For information about the software see the repository this was forked from: [https://github.com/osu-particle-astrophysics/GENETIS_PUEO](https://github.com/osu-particle-astrophysics/GENETIS_PUEO).

The algorithm for RHINO is simpler than that for PUEO. The algorithm is:
```
generate initial genes
loop
	generate horn antennas from genes, using xfdtd
		generate multiple "individuals", each from a different set of genes
	simulate the horn beam patterns, using xfdtd
		this runs multiple GPU jobs on the cluster
	calculate the fitness of the beam patterns
	update the genes for each individual based on the fitness values
```

The Parts of the original GENETIS_PUEO algorithm have been modified or not used. A summary:

* Part_A. Generate genes. Unmodified except for the specific genes representing parameters of a horn antenna, and their constraints. Genetic specific code unmodified.
* Part_B.sh. Generate horns using xfdtd and send simulation to the cluster to get beam patterns. Unmodified.
* Part_B2_Parallel.sh. Wait for the simulations to finish and extract the beam patterns (UAN files). This is substantially modified because in the original GENETIS_PUEO there were further simulations to do with firing neutrinos at the beam patterns. These are removed.
* Part_C.sh. Process UAN files to DAT files for further analysis using existing RHINO tools. Modified from processing neutrino output.
* Part_D1.sh. Not used.
* Part_D2.sh. Not used.
* Part_E.sh.  Analyse beams in DAT files and create fitness scores. Modified to remove neutrino processing.
* Part_F.sh. Make some plots of beams. Modified.

The JavaScript code in XMacros has been substantially modified since it builds RHINO horns rather than PUEO antennas. There are also extra scripts for plotting and making movies of the outputs. Some examples are in genetis_example.pdf.





