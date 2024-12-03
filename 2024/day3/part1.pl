#!/usr/bin/perl
package main;
use strict;
use warnings;

sub main {
    my $filename = shift;

    open(my $file, $filename) or die ":(";
    my $content = do { local $/ = undef; <$file> };
    close($filename);

    my @operations = $content =~ m{mul\(\d+,\d+\)}g;

    my $total = 0;
    for my $op (@operations) {
        my ($x, $y) = $op =~ m{mul\((\d+),(\d+)\)};
        $total += $x * $y;
    }

    print "part1 >> $total\n";
}

main(@ARGV)