package LCFG::Build::Tool::Pack;    # -*-cperl-*-
use strict;
use warnings;

# $Id: Pack.pm.in,v 1.13 2008/09/12 14:05:30 squinney Exp $
# $Source: /disk/cvs/dice/LCFG-Build-Tools/lib/LCFG/Build/Tool/Pack.pm.in,v $
# $Revision: 1.13 $
# $HeadURL$
# $Date: 2008/09/12 14:05:30 $

our $VERSION = '0.0.49';

use File::Path ();
use File::Spec ();
use File::Temp ();
use LCFG::Build::PkgSpec;
use LCFG::Build::Utils;
use UNIVERSAL::require;

use Moose;

extends 'LCFG::Build::Tool';

has 'gencmake' => (
    is            => 'rw',
    isa           => 'Bool',
    lazy          => 1,
    default       => sub { $_[0]->spec->get_buildinfo('gencmake') },
    documentation => 'Generate CMake files',
);

has 'translate' => (
    is            => 'rw',
    isa           => 'Bool',
    lazy          => 1,
    default       => sub { $_[0]->spec->get_buildinfo('translate_before_pack') },
    documentation => 'Translate files before packing source',
);

has 'remove_after_translate' => (
    is            => 'rw',
    isa           => 'Bool',
    lazy          => 1,
    default       => sub { $_[0]->spec->get_buildinfo('remove_input_after_translate') },
    documentation => 'Remove input files after translation',
);

__PACKAGE__->meta->make_immutable;

sub abstract {
    return q{Package the tagged source tree};
}

sub run {
    my ($self) = @_;

    my ( $spec, $vcs ) = ( $self->spec, $self->vcs );

    my $version = $spec->version;

    my $module = $spec->fullname;

    my $dirname = join q{-}, $module, $version;
    my $outdir = File::Spec->catdir( $self->resultsdir, $dirname );

    if ( -d $outdir ) {
        File::Path::rmtree $outdir;
    }
    eval { File::Path::mkpath $outdir };
    if ($@) {
        $self->fail("Could not create $outdir: $@");
    }

    my $tempdir = File::Temp::tempdir( TMPDIR => 1, CLEANUP => 1 );

    my $srcdir = $vcs->export( $version, $tempdir );
    $self->log('Successfully exported the source tree.');

    # We want to work with the specfile of the exported version not
    # the local version to avoid any recent development-related
    # changes.

    my $new_metafile = File::Spec->catfile( $srcdir, 'lcfg.yml' );
    my $new_spec = LCFG::Build::PkgSpec->new_from_metafile($new_metafile);
    $self->spec($new_spec);

    # Might be nice to be more fine-grained about what we do here in a
    # dry-run but it is hard to do much more when the export has not
    # done anything.

    if ( !$self->dryrun ) {

        if ( $self->translate ) {
            LCFG::Build::Utils::find_and_translate( $new_spec, $srcdir,
                $self->remove_after_translate );
            $self->log('Successfully translated template files.');
        }

        if ( $self->gencmake ) {
            LCFG::Build::Utils::generate_cmake( $new_spec, $srcdir );
            $self->log('Successfully generated cmake files.');
        }

        for my $util ( LCFG::Build::Utils->plugins() ) {
            $util->require or $self->fail($@);
            my $type = ( split /::/, $util )[-1];

            if ( $util->can('generate_metadata') ) {
                eval {
                    $util->generate_metadata( $new_spec, $srcdir, $outdir )
                };
                if ($@) {
                    $self->fail("Failed to generate package metadata files for $type: $@");
                }

                $self->log("Successfully generated metadata files for $type");
            }
        }

        # We MUST pack *AFTER* generating the metadata in case the
        # metadata files need to be inserted into the generated tar
        # file.

        my $tarname = $new_spec->tarname;
        LCFG::Build::Utils::generate_srctar( $tarname, $srcdir, $outdir );
        $self->log('Successfully generated source tar file.');

    }

    return;
}

no Moose;
1;
__END__

=head1 NAME

    LCFG::Build::Tool::Pack - LCFG software packaging tool

=head1 VERSION

    This documentation refers to LCFG::Build::Tool::Pack version 0.0.49

=head1 SYNOPSIS

    my $tool = LCFG::Build::Tool::Pack->new( dir => '.' );

    $tool->run;

    my $tool2 = LCFG::Build::Tool::Pack->new_with_options();

    $tool2->run;

=head1 DESCRIPTION

This module provides software release tools for the LCFG build
suite.

This is a tool to take a tagged copy of the source for a project
managed with the LCFG build tools and package it into a gzipped source
tar file. Build metadata files for supported platforms (e.g. a
specfile for building binary RPMs) are also generated at the same
time. It is also possible to do limited autoconf-style macro
substitution prior to the source being packaged. This allows the
generation of 'pristine' tar files where downstream users will be
unaware of the additional source-file processing that has been carried
out prior to distribution.

More information on the LCFG build tools is available from the website
http://www.lcfg.org/doc/buildtools/

=head1 ATTRIBUTES

The following attributes are modifiable via the command-line (i.e. via
@ARGV) as well as the normal way when the Tool object is
created. Unless stated the options take strings as arguments and can
be used like C<--foo=bar>. Boolean options can be expressed as either
C<--foo> or C<--no-foo> to signify true and false values.

=over 4

=item dryrun

A boolean value which indicates whether actions which permanently
alter the contents of files should be carried out. The default value
is false (0). When running in dry-run mode various you will typically
get extra output to the screen showing what would have been done.

=item quiet

A boolean value which indicates whether the actions should attempt to
be quieter. The default value is false (0).

=item dir

The path of the project directory which contains the software for
which you want to create a release. If this is not specified then a
default value of the current directory (.) will be used. This
directory must already contain the LCFG build metadata file (lcfg.yml)
for the software.

=item resultsdir

When a project is packaged for release the generated products (the
gzipped source tar file, various build metadata files and possibly
binary RPMS, etc) are stored into a directory named after the
combination of the full name of the project and the version
number. For example, a project named 'foo' with version '1.2.3' would
have an output directory of 'foo-1.2.3'. You should note that if the
C<base> attribute is specified in the metadata file (this is the case
for LCFG components) then that is also used. If the previous example
was an LCFG component it would have a directory named
'lcfg-foo-1.2.3'.

This attribute controls the parent directory into which that generated
directory will be placed. The default on a Unix system is
C<$HOME/lcfgbuild/> which will be created if it does not already
exist.

=item gencmake

This is a boolean value which controls whether CMake build files will
be created when the source code for the project is packaged. The
default is to take the setting from C<gencmake> option in the
C<buildinfo> section of the LCFG build metadata file.

=item translate

This is a boolean value which controls whether source files will be
translated BEFORE they are packaged. The default is to take the
setting from C<translate_before_pack> option in the C<buildinfo>
section of the LCFG build metadata file.

=item remove_after_translate

This is a boolean value which controls whether input files will be
removed after they have been translated. They are only removed if the
input and output filenames do not match (e.g. foo.cin becomes
foo). The default is to take the setting from
C<remove_input_after_translate> option in the C<buildinfo> section of
the LCFG build metadata file.

=back

The following methods are not modifiable by the command-line, they are
however directly modifiable via the Tool object if
necessary. Typically you will only need to query these attributes,
they are automatically created when you need them using values for
some of the other command-line attributes.

=over 4

=item spec

This is a reference to the current project metadata object, see
L<LCFG::Build::PkgSpec> for full details.

=item vcs

This is a reference to the current version-control object, see
L<LCFG::Build::VCS> for full details.

=back

=head1 SUBROUTINES/METHODS

=over 4

=item run

This uses the relevant L<LCFG::Build::VCS> module to export the tagged
version of the project and packages it into a gzipped source tar
file. The version to export is selected by looking at the version
field in LCFG build metadata file within the directory
specified. After that it builds metadata files for each supported
platform (e.g. a specfile for building binary RPMs).

=item fail($message)

Immediately fails (i.e. dies) and displays the message.

=item log($message)

Logs the message to the screen if the C<quiet> attribute has not been
specified. A message string is prefixed with 'LCFG: ' to help visually
separate it from other output.

=back

=head1 DEPENDENCIES

This module is L<Moose> powered and uses L<MooseX::App::Cmd> to handle
command-line options.

The following modules from the LCFG build tools suite are also
required: L<LCFG::Build::Tool>, L<LCFG::Build::PkgSpec>,
L<LCFG::Build::VCS> and VCS helper module for your preferred
version-control system.

=head1 SEE ALSO

L<LCFG::Build::Tools>, L<LCFG::Build::Skeleton>, lcfg-reltool(1)

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
