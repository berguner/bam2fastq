# bam2fastq
A simple script for converting pair-end bam files to fastq files. Unlike other bam2fastq scripts this script can handle the discordant pairs(pairs mapped to different chromosomes) without sorting the reads by name. Discordant reads will accumulate in memory until their mates are found. So there should be enough memory for such pairs. For regular Illumina WGS/WXS memory should not be an issue. If the mate of a read could not be found it will be written in single_ends.fq file.

The script creates 3 files:
R1.fq
R2.fq
single_ends.fq

Usage:
samtools view sample.bam | python bam2fastq.py
