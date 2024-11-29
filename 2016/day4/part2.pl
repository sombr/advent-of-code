#!/usr/bin/perl
package main;
use strict;
use warnings;

sub main {
    my $filename = shift;
    open(my $file, $filename) or die "cannot open $filename";

    while (my $line = <$file>) {
        chomp $line;
        my ($room, $id, $check) = $line =~ m{^([a-z-]+)-(\d+)\[(\w+)\]$};
        my $name = $room;

        $room =~ s{-}{}g;
        my $counts = {};
        for my $r (split(//, $room)) {
            $counts->{$r}++;
        }

        my @pairs;
        for my $r (keys %$counts) {
            push @pairs, [$counts->{$r}, $r];
        }
        @pairs = sort { $a->[0] == $b->[0] ? $a->[1] cmp $b->[1] : $b->[0] <=> $a->[0] } @pairs;

        my $computed_checksum = [];
        for my $p (@pairs) {
            last if scalar @$computed_checksum == 5;
            push @$computed_checksum, $p->[1];
        }
        $computed_checksum = join("", @$computed_checksum);

        if ($computed_checksum eq $check) {
            # real room, let's decode
            my @letters = split(//, $name);
            my @decoded = ();

            for my $l (@letters) {
                if ($l eq "-") {
                    push @decoded, " ";
                } else {
                    my $letter_index = ord($l) - ord('a');
                    my $new_index = ($letter_index + $id) % 26;
                    push @decoded, chr($new_index + ord('a'));
                }
            }

            print(">>> sector: $id decoded: ", join("", @decoded), "\n");
        }
    }

    close($file);
}

main(@ARGV)
