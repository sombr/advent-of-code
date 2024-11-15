#!/usr/bin/perl
use strict;
use warnings;

open(my $file, "input.txt") or die ":(";

my $txt = do { local $/ = undef; <$file> };

my $acc = 0;
my $first_below = -1;

my $i = 1;
for my $sym (split(//, $txt)) {
    $acc++ if $sym eq "(";
    $acc-- if $sym eq ")";

    $first_below = $i if $first_below < 0 and $acc < 0;

    $i++;
}

close($file);

print(">> part1: $acc\n");
print(">> part2: $first_below\n");
