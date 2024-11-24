#!/usr/bin/perl
package main;
use strict;
use warnings;

my $PART1_LOOKUP = {
    children => 3,
    cats => 7,
    samoyeds => 2,
    pomeranians => 3,
    akitas => 0,
    vizslas => 0,
    goldfish => 5,
    trees => 3,
    cars => 2,
    perfumes => 1,
};

sub main {
    my $filename = shift;

    my $chosen = [];
    open(my $file, $filename) or die ":(";
    while (my $line = <$file>) {
        chomp $line;
        # Sue 4: goldfish: 5, children: 8, perfumes: 3

        my ($sue, $parts) = $line =~ m{^Sue\s+(\d+):\s+(.*)$};
        $parts = +{ map { split(/:\s+/, $_) } split(/,\s+/, $parts) };

        my $good = 1;
        for my $k (keys %$parts) {
            $good = $good && ($PART1_LOOKUP->{$k} == $parts->{$k});
        }
        next unless $good;

        push(@$chosen, [$sue, $parts]);
    }
    close($file);

    use Data::Dumper;
    print Dumper $chosen;
}

main(@ARGV)