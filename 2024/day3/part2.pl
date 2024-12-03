#!/usr/bin/perl
package main;
use strict;
use warnings;

sub main {
    my $filename = shift;

    open(my $file, $filename) or die ":(";
    my $content = do { local $/ = undef; <$file> };
    close($filename);

    my @operations = $content =~ m{(?:mul\(\d+,\d+\))|(?:(?:do\(\))|(?:don't\(\)))}g;

    my $total = 0;
    my $enabled = 1;
    for my $op (@operations) {
        if ($op eq "do()") {
            $enabled = 1;
            next;
        }
        if ($op eq "don't()") {
            $enabled = 0;
            next;
        }

        if ($enabled) {
            my ($x, $y) = $op =~ m{mul\((\d+),(\d+)\)};
            $total += $x * $y;
        }
    }

    print "part2 >> $total\n";
}

main(@ARGV)