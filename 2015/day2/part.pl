#!/usr/bin/perl
use strict;
use warnings;

open(my $file, "input.txt") or die ":(";

my $acc = 0;
my $ribbon_acc = 0;
while (my $line = <$file>) {
    chomp $line;
    my ($ta, $tb, $tc) = split(/x/, $line);

    my ($ab, $bc, $ac) = ($ta*$tb, $tb*$tc, $ta*$tc);
    
    my $min_side = $ab < $bc ? $ab : $bc;
    $min_side = $ac if $ac < $min_side;

    my $paper = $min_side + 2*($ab+$bc+$ac);
    $acc += $paper;

    my ($m1, $m2) = sort { $a <=> $b } ($ta, $tb, $tc);
    my $ribbon = ($m1+$m2)*2 + $ta*$tb*$tc;
    $ribbon_acc += $ribbon;
}

close($file);

print("part1: $acc\n");
print("part2: $ribbon_acc\n");
