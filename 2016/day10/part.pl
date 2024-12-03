#!/usr/bin/perl
package main;
use strict;
use warnings;

sub main {
    my $filename = shift;

    open(my $file, $filename) or die ":(";
    my @lines = <$file>;
    close($file);

    my $rules = {};
    my @transactions;
    for my $line (@lines) {
        chomp $line;

        if ($line =~ m{bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)}) {
            $rules->{$1} = {
                low => [ $2, $3 ],
                high => [ $4, $5]
            };
            next;
        }


        if ($line =~ m{value (\d+) goes to (\w+) (\d+)}) {
            push @transactions, {
                value => $1,
                to => $2,
                idx => $3,
            };
        }
    }

    my $bot_input = {};
    my $output = {};
    my $part1_bot = undef;
    while (@transactions) {
        my $t = shift @transactions;

        if ($t->{to} eq "output") {
            $output->{ $t->{idx} } = $t->{value};
        } elsif ($t->{to} eq "bot") {
            my $input = $bot_input->{ $t->{idx} } || [];
            push @$input, $t->{value};

            if (scalar @$input == 2) {
                # check part 1 rule
                @$input = sort { $a <=> $b } @$input;
                
                if ($input->[0] == 17 && $input->[1] == 61 && !$part1_bot) {
                    $part1_bot = $t->{idx};
                }
                
                if ($rules->{ $t->{idx} }) {
                    unshift @transactions, +{
                        value => $input->[0],
                        to => $rules->{ $t->{idx} }->{low}->[0],
                        idx => $rules->{ $t->{idx} }->{low}->[1],
                    };
                    unshift @transactions, +{
                        value => $input->[1],
                        to => $rules->{ $t->{idx} }->{high}->[0],
                        idx => $rules->{ $t->{idx} }->{high}->[1],
                    };
                }
            } elsif (scalar @$input > 2) {
                die "this should not happen";
            }

            $bot_input->{ $t->{idx} } = $input;
        } else {
            die "uknown";
        }
    }

    print "part1 >> bot $part1_bot\n";

    my $part2 = $output->{0} * $output->{1} * $output->{2};
    print "part2 >> product $part2\n";
}

main(@ARGV);
