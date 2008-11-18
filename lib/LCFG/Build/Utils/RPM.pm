package LCFG::Build::Utils::RPM;    # -*-cperl-*-
use strict;
use warnings;

# $Id: RPM.pm.in,v 1.8 2008/09/12 14:05:30 squinney Exp $
# $Source: /disk/cvs/dice/LCFG-Build-Tools/lib/LCFG/Build/Utils/RPM.pm.in,v $
# $Revision: 1.8 $
# $HeadURL$
# $Date: 2008/09/12 14:05:30 $

our $VERSION = '0.0.47';

use Date::Format ();
use Date::Parse  ();
use File::Copy   ();
use File::Path   ();
use File::Spec   ();

use LCFG::Build::Utils;

sub generate_metadata {
    my ( $self, $pkgspec, $dir, $outdir ) = @_;

    $outdir ||= q{.};
    $dir    ||= q{.};

    my $specfile = join q{.}, $pkgspec->fullname, 'spec';
    $specfile = File::Spec->catfile( $dir, $specfile );

    if ( !-f $specfile ) {
        $specfile = File::Spec->catfile( $dir, 'specfile' );
        if ( !-f $specfile ) {
            die "You need to generate a specfile\n";
        }
    }

    # Do our best to find a changelog file of some description.

    my $logfile = $pkgspec->get_vcsinfo('logname');
    if ( !defined $logfile ) {
        for my $file (qw/ChangeLog Changes/) {
            my $path = File::Spec->catfile( $dir, $file );
            if ( -f $path ) {
                $logfile = $file;
                last;
            }
        }
    }

    my $extra = {};
    if ( defined $logfile ) {
        $logfile = File::Spec->catfile( $dir, $logfile );
        if ( -f $logfile ) {

            my $changelog = format_changelog($logfile);
            $extra->{LCFG_CHANGELOG} = $changelog;
        }
    }

    my $packname = join q{-}, $pkgspec->fullname, $pkgspec->version;
    my $specname = $packname . '.spec';
    my $output   = File::Spec->catfile( $outdir, $specname );

    LCFG::Build::Utils::translate_file( $pkgspec, $specfile,
                                        $output,
                                        $extra );

    # Do this so the generated tar-file contains a usable specfile

    File::Copy::copy( $output, $specfile );

    return;
}

sub _format_entry {
    my ( $date, $release, $rest, @body ) = @_;

    my $t = Date::Parse::str2time($date);
    my $formatted_date = Date::Format::time2str( '%a %b %d %Y', $t );

    if ( $rest =~ /\s*cvs:\s*new release/i && defined $release ) {
        $rest = "<<<< Release: $release >>>>";
    }
    $rest =~ s/ +/ /g;

    my $output = "* $formatted_date $rest\n";
    for my $item (@body) {
        $item =~ s/\n+(  )?/\n  /g;
        $output .= "- $item\n";
    }
    $output .= "\n";

    return $output;
}

sub format_changelog {
    my ($logfile) = @_;

    my $fh = IO::File->new( $logfile, 'r' )
        or die "Could not open $logfile: $!\n";

    # Big assumption here that the changelog is in the correct
    # format for cl2rpm to understand.

    my $changelog;
    my ( $date, $tab, $release, $rest, @body );

    while ( defined( my $line = <$fh> ) ) {
        chomp $line;

        if ( $line =~ m/^(\d+-\d+-\d+)\s*(.*)$/ ) {

            if ( defined $date ) {
                $changelog .= _format_entry( $date, $release, $rest, @body );

                undef $release;
                $tab  = "\t";
                @body = ();
            }

            ( $date, $rest ) = ( $1, $2 );

        }
        elsif ( $line =~ m/^\s+\*\s*release:\s*(.*)$/i ) {
            $release = $1;
        }
        elsif ( $line =~ m/^(\s+)\*\s*(.*)$/ ) {
            $tab = $1;
            push @body, $2;
        }
        elsif ( $line =~ /^\s+.*$/ ) {
            $line =~ s/^\Q$tab\E//;
            if ( $tab eq "\t" ) {
                $line =~ s/^        //;
            }

            if ( length $line > 0 ) {
                if ( scalar @body > 0 ) {
                    $body[-1] = join "\n", $body[-1], $line;
                }
                else {
                    push @body, $line;
                }
            }
        }
    }

    $changelog .= _format_entry( $date, $release, $rest, @body );

    return $changelog;
}

sub build {
    my ( $self, $tarfile, $specfile, $sourceonly, $options ) = @_;

    if ( !defined $options ) {
        $options = {};
    }

    require RPM4;

    my %dirs = (
        builddir  => RPM4::expand('%_builddir'),     # BUILD
        specdir   => RPM4::expand('%_specdir'),      # SPECS
        sourcedir => RPM4::expand('%_sourcedir'),    # SOURCES
        srcrpmdir => RPM4::expand('%_srcrpmdir'),    # SRPMS
        rpmdir    => RPM4::expand('%_rpmdir'),       # RPMS
    );

    for my $dir ( values %dirs ) {
        if ( !-d $dir ) {
            eval { File::Path::mkpath $dir };
            if ($@) {
                die "Could not create $dir: $@\n";
            }
        }
    }

    if ( defined $tarfile ) {
        File::Copy::copy( $tarfile, $dirs{sourcedir} );
    }

    my @buildflags;
    if ($sourceonly) {
        @buildflags = qw(PACKAGESOURCE);
    }
    else {
        @buildflags = qw(PREP
                         BUILD
                         FILECHECK
                         INSTALL
                         CHECK
                         PACKAGESOURCE
                         PACKAGEBINARY);
    }

    my $rpmspec = RPM4::Spec->new($specfile);

    my $db = RPM4::newdb();

    if ( !$options->{nodeps} ) {

        my $sh = $rpmspec->srcheader()
            or die "Can't get source header from spec object\n";

        $db->transadd( $sh, q{}, 0 );
        $db->transcheck;

        my $pbs = RPM4::Transaction::Problems->new($db);
        $db->transreset();

        if ($pbs) {
            $pbs->print_all( \*STDERR );
            die "rpmbuild failed\n";
        }

    }

    my $result = eval { $db->specbuild( $rpmspec, [@buildflags] ) };
    if ($@) {
        die "rpmbuild failed: $@\n";
    }
    elsif ( $result != 0 ) {
        die "rpmbuild failed\n";
    }

    my $source = $rpmspec->srcrpm;

    my @packages;
    if ( !$sourceonly ) {
        @packages = $rpmspec->binrpm;
    }

    return {
        packages => \@packages,
        source   => $source,
    };
}

1;
__END__

=head1 NAME

    LCFG::Build::Utils::RPM - LCFG software building utilities

=head1 VERSION

    This documentation refers to LCFG::Build::Utils::RPM version 0.0.47

=head1 SYNOPSIS

    my $dir = q{.};

    my $spec = LCFG::Build::PkgSpec->new_from_metafile("$dir/lcfg.yml");

    my $resultsdir = '/tmp/foo';
    LCFG::Build::Utils::RPM->generate_metadata( $spec, $dir, $resultsdir )

=head1 DESCRIPTION

This module provides a suite of utilities to help in building RPM
packages from LCFG projects, particularly LCFG components. The methods
are mostly used by tools which implement the LCFG::Build::Tool base
class (e.g. LCFG::Build::Tool::RPM) but typically they are designed to
be generic enough to be used elsewhere.

=head1 SUBROUTINES/METHODS

There are two public methods you can call on this class.

=over 4

=item generate_metadata( $pkgspec, $dir, $outdir )

This generates the necessary metadata file (i.e. the specfile) for
building RPM packages from this project.  It takes an LCFG build
package metadata object, an input directory where the template RPM
specfile and change log files are stored and an output directory where
the generate file should be placed.

=item build( $tarfile, $specfile, $sourceonly, $options )

This actually builds the RPM packages using the RPM4 wrapper around
C<rpmbuild>. It requires the name of the source tar file and the RPM
specfile. Optionally it can do a source-only build, and a reference to
a hash of options can be passed in, this allows one to specify things
like making rpmbuild ignore dependencies with "nodeps". See the
RPM4::Spec Perl documentation for full details of the supported
options.

=back

=head1 DEPENDENCIES

For building packages you will need RPM4(3), for formatting the change
log file you will need Date::Parse(3) and Date::Format(3) which are
part of the TimeDate suite.

=head1 PLATFORMS

This is the list of platforms on which we have tested this
software. We expect this software to work on any Unix-like platform
which is supported by Perl.

FedoraCore5, FedoraCore6, ScientificLinux5

=head1 BUGS AND LIMITATIONS

There are no known bugs in this application. Please report any
problems to bugs@lcfg.org, feedback and patches are also always very
welcome.

=head1 AUTHOR

    Stephen Quinney <squinney@inf.ed.ac.uk>

=head1 LICENSE AND COPYRIGHT

    Copyright (C) 2008 University of Edinburgh. All rights reserved.

This library is free software; you can redistribute it and/or modify
it under the terms of the GPL, version 2 or later.

=cut
