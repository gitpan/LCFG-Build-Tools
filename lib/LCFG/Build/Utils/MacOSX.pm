package LCFG::Build::Utils::MacOSX;    # -*-cperl-*-
use strict;
use warnings;

# $Id: MacOSX.pm.in,v 1.6 2008/09/12 14:05:30 squinney Exp $
# $Source: /disk/cvs/dice/LCFG-Build-Tools/lib/LCFG/Build/Utils/MacOSX.pm.in,v $
# $Revision: 1.6 $
# $HeadURL$
# $Date: 2008/09/12 14:05:30 $

our $VERSION = '0.0.45';

use File::Spec ();
use LCFG::Build::Utils;
use Sys::Hostname ();

sub generate_metadata {
    my ( $self, $spec, $dir, $outdir ) = @_;

    $outdir ||= q{.};
    $dir    ||= q{.};

    my $hostname = Sys::Hostname::hostname;

    my @parts = split /\./, $hostname;
    shift @parts;
    @parts = reverse @parts;

    my $bundleid = join q{.}, @parts, $spec->fullname;

    my $extra = { OSXPKG_BUNDLEID => $bundleid };

    my $tmpldir
        = File::Spec->catdir( LCFG::Build::Utils::datadir(), 'templates' );

    for my $file (qw/Description.plist Info.plist/) {
        my $infile = File::Spec->catfile( $dir, $file );

        if ( !-f $infile ) {
            $infile = File::Spec->catfile( $tmpldir, "$file.tmpl" );
        }

        my $output = File::Spec->catfile( $outdir, $file );
        LCFG::Build::Utils::translate_file( $spec, $infile, $output, $extra );
    }

    return;
}

sub build {
    my ( $self, $tarfile ) = @_;

    return;
}

1;
__END__

=head1 NAME

    LCFG::Build::Utils::MacOSX - LCFG software building utilities

=head1 VERSION

    This documentation refers to LCFG::Build::Utils::MacOSX version 0.0.45

=head1 SYNOPSIS

    my $dir = q{.};

    my $spec = LCFG::Build::PkgSpec->new_from_metafile("$dir/lcfg.yml");

    my $resultsdir = '/tmp/foo';
    LCFG::Build::Utils::MacOSX->generate_metadata( $spec, $dir, $resultsdir )

=head1 DESCRIPTION

This module provides a suite of utilities to help in building MacOSX
packages from LCFG projects, particularly LCFG components. The methods
are mostly used by tools which implement the LCFG::Build::Tool base
class (e.g. LCFG::Build::Tool::OSXPkg) but typically they are designed to
be generic enough to be used elsewhere.

=head1 SUBROUTINES/METHODS

There are two public methods you can call on this class.

=over 4

=item generate_metadata( $pkgspec, $dir, $outdir )

This generates the Description.plist and Info.plist metadata files for
building MacOSX packages with PackageMaker. It first looks in the
directory specified in $dir and if templates for the metadata files
are not found it uses those stored in
/usr/share/lcfgbuild/templates. The generated files are placed into
the output directory named in $outdir.

=item build( $tarfile )

=back

=head1 DEPENDENCIES

For building packages you will need PackageMaker.

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
