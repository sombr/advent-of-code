#!/usr/bin/perl
use strict;
use warnings;
use Digest::MD5 qw/md5_hex/;
use File::Slurp;

my $input = read_file("input.txt");
chomp $input;

for (my $i = 0; $i < 1_000_000; $i++) {
    my $hex = md5_hex("$input$i");
    if ($hex =~ m{^0{5}}) {
        print ">> part1: $i\n";
        last;
    }
}

for (my $i = 0; $i < 1_000_000_000; $i++) {
    my $hex = md5_hex("$input$i");
    if ($hex =~ m{^0{6}}) {
        print ">> part2: $i\n";
        last;
    }
}
