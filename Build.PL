use Module::Build; # -*-cperl-*-

my %yml_files = map { $_ => "lcfgbuild/$_" }
    qw(lcfg_config.yml mapping_config.yml);

my %tmpl_files = map { $_ => "lcfgbuild/$_" }
    ( glob('templates/*.tt'), glob('templates/*.tmpl') );

my $build = Module::Build->new(
    module_name   => 'LCFG::Build::Tools',
    dist_abstract => 'LCFG build system tools',
    dist_author   => 'Stephen Quinney <squinney@inf.ed.ac.uk>',
    dist_version  => '0.0.38',
    license => 'gpl',
    requires => {
        'perl'                 => '5.6.1',
        'Archive::Tar'         => '0',
        'Date::Format'         => '1.16',
        'Date::Parse'          => '0',
        'File::HomeDir'        => '0.58',
        'File::Find::Rule'     => '0',
        'IO::Zlib'             => '0',
        'LCFG::Build::PkgSpec' => '0.0.22',
        'LCFG::Build::VCS'     => '0.0.19',
        'Module::Pluggable'    => '3.10',
        'Moose'                => '0.57',
        'MooseX::App::Cmd'     => '0.04',
        'Template'             => '2.14',
        'Text::Abbreviate'     => '0.01',
        'UNIVERSAL::require'   => '0',
        'YAML::Syck'           => '0.98',
    },
    build_requires => {
        'Test::More'        => 0,
        'Test::Differences' => 0,
        'Test::Exception'   => 0,
    },
    add_to_cleanup => [ 'LCFG-Build-Tools-*', 'MANIFEST.bak', 'Changes.bak' ],
    create_makefile_pl => 'traditional',
    yml_files    => \%yml_files,
    tmpl_files   => \%tmpl_files,
    install_path => { lcfgbuild => '/usr/share/lcfgbuild' },
);
$build->add_build_element('yml');
$build->add_build_element('tmpl');
$build->create_build_script;
