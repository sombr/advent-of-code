#!/usr/bin/perl
use strict;
use warnings;

open(my $file, "input.txt") or die ":(";

my $moves = do { local $/ = undef; <$file> };
chomp $moves;

close($file);

sub deliver {
    my $moves = shift;
    my $visited = shift;

    my ($r, $c) = (0,0);

    $visited->{"$r,$c"} = 1;
    for my $s (split(//, $moves)) {
        $r++ if $s eq "v";
        $r-- if $s eq "^";
        $c++ if $s eq ">";
        $c-- if $s eq "<";
        $visited->{"$r,$c"} = 1;
    }

    return scalar(keys %$visited);
}

print "part 1: " . deliver($moves, {}) . "\n";

my $santa = [];
my $robot = [];
my $i = 0;
for my $s (split(//, $moves)) {
    push @{ $i % 2 == 0 ? $santa : $robot }, $s;
    $i++;
}

my $visited = {};
deliver(join("", @$santa), $visited);
deliver(join("", @$robot), $visited);
print "part 2: " . scalar(keys %$visited) . "\n";
