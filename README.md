# bam2fastq
A simple script for converting pair-end bam files to fastq files. Unlike other bam2fastq scripts this script can handle discordant pairs(pairs mapped to different chromosomes) without sorting the reads by name. Discordant reads will accumulate in memory until their mates are found. For regular Illumina WGS/WXS data memory should not be an issue. If the mate of a read could not be found it will be written in single_ends.fq file.

IMPORTANT: Mates are matched by their names, so there shouldn't be any suffixes (i.e. "/1" or "/2") in read names

The script creates 3 files:
R1.fq
R2.fq
single_ends.fq

Usage:
samtools view sample.bam | python bam2fastq.py
