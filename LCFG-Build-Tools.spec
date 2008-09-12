Name:           perl-LCFG-Build-Tools
Version:        0.0.38
Release:        1
Summary:        LCFG build system tools
License:        gpl
Group:          Development/Libraries
Source0:        LCFG-Build-Tools-0.0.38.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:5.6.1
BuildRequires:  perl(LCFG::Build::PkgSpec) >= 0.0.22
BuildRequires:  perl(LCFG::Build::VCS) >= 0.0.19
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(File::HomeDir) >= 0.58
BuildRequires:  perl(YAML::Syck) >= 0.98
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Template) >= 2.14
BuildRequires:  perl(Archive::Tar), perl(IO::Zlib)
BuildRequires:  perl(RPM4)
BuildRequires:  perl(MooseX::App::Cmd)
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl(Text::Abbreviate)
BuildRequires:  perl(Test::Differences)
Requires:       perl(LCFG::Build::PkgSpec) >= 0.0.22
Requires:       perl(LCFG::Build::VCS) >= 0.0.19
Requires:       perl(YAML::Syck) >= 0.98
Requires:       perl(File::Find::Rule)
Requires:       perl(Template) >= 2.14
Requires:       perl(Archive::Tar), perl(IO::Zlib)
Requires:       perl(RPM4)
Requires:       perl(MooseX::App::Cmd)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
LCFG::Build::Tools is a suite of tools designed to handle the
releasing of LCFG software projects and the creation of
packages. Support is available for developing projects within a
version-control systems (currently either CVS or None). By default a
source tar file is generated along with a specfile for building binary
RPMs. Support is provided for building binary RPMs directly. Work is
under way to also fully support the generation of MacOSX packages.

Although this software is designed for managing LCFG projects there is
nothing that requires the software be for LCFG. All the tools included
are designed to more widely applicable.

This suite has been intentionally designed to be easy to extend to
support new version-control systems (e.g. subversion, git, etc) and
new package formats (e.g. for Debian). It has also been designed to
ensure that it is easy to extend with additional command modules. For
further details see the online documentation at
http://www.lcfg.org/doc/buildtools/

%prep
%setup -q -n LCFG-Build-Tools-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%{perl_vendorlib}/LCFG/Build/Tool/*.pm
%{perl_vendorlib}/LCFG/Build/Tool.pm
%{perl_vendorlib}/LCFG/Build/Tools.pm
%{perl_vendorlib}/LCFG/Build/Utils.pm
%{perl_vendorlib}/LCFG/Build/Utils/MacOSX.pm
%{perl_vendorlib}/LCFG/Build/Utils/RPM.pm
/usr/share/lcfgbuild/lcfg_config.yml
/usr/share/lcfgbuild/mapping_config.yml
/usr/share/lcfgbuild/templates/*.tt
/usr/share/lcfgbuild/templates/Description.plist.tmpl
/usr/share/lcfgbuild/templates/Info.plist.tmpl
/usr/bin/lcfg-reltool

%changelog
* Fri Sep 12 2008 <<<< Release: 0.0.38 >>>>

* Fri Sep 12 2008 15:05 squinney
- Lots of documentation improvements. Various work on making the
  file and directory path handling more platform-independent

* Tue Sep 09 2008 11:38 squinney

* Tue Sep 09 2008 11:38 squinney
- Use make_immutable for each Moose class. According to the docs
  this should provide a good speed-up in code loading

* Tue Sep 09 2008 10:59 squinney

* Tue Sep 09 2008 10:59 squinney
- Removed the genmeta options from the package building tools. Used
  Module::Pluggable to add a new LCFG::Build::Utils plugins()
  method which lists all available Utils sub-classes. Switched
  generate_metadata() and build() to be methods to make it easier
  to test for existence and call without a string eval

* Mon Sep 08 2008 14:24 squinney

* Mon Sep 08 2008 14:22 squinney
- Lots of documentation improvements

* Mon Sep 08 2008 13:33 squinney

* Mon Sep 08 2008 13:32 squinney
- Now using the new support for removing input files after
  substitution. Also corrected a couple of bits in the specfile.

* Mon Sep 08 2008 13:26 squinney
- Added support for removing input files after macro substitution
  has been completed. Also switched the source tar file generation
  sequence so that the packing happens last which allows the
  inclusion of generated metadata files

* Mon Sep 08 2008 13:24 squinney
- Added some high-level documentation to LCFG::Build::Tools

* Mon Sep 08 2008 13:23 squinney
- Improved specfile

* Mon Sep 08 2008 13:23 squinney
- Updated perl build files

* Mon Sep 08 2008 13:22 squinney
- Updated package MANIFEST

* Tue Sep 02 2008 12:35 squinney

* Tue Sep 02 2008 12:34 squinney
- Fixed a problem with pod2man not working if the group argument,
  which gets passed into the --center option, was not specified

* Thu Aug 07 2008 13:05 squinney

* Thu Aug 07 2008 13:05 squinney
- Lots of small changes to satisfy perltidy and perlcritic

* Wed Aug 06 2008 16:49 squinney

* Wed Aug 06 2008 16:49 squinney
- Added a basic test to check that all Perl modules are loadable.
  Also added all the necessary build dependencies so this check can
  be carried out in a chroot

* Wed Aug 06 2008 15:25 squinney

* Wed Aug 06 2008 15:24 squinney
- Added basic MacOSX support, stubs for the ospkg and devospkg
  command modules are now supplied

* Tue Aug 05 2008 15:29 squinney

* Tue Aug 05 2008 15:29 squinney
- Added a new checkmacros command

* Wed Jul 30 2008 21:17 squinney

* Wed Jul 30 2008 21:16 squinney
- overrode sourceonly and deps attributes from
  LCFG::Build::Tool::SRPM  so they don't show up as options for the
  srpm command

* Wed Jul 30 2008 21:14 squinney
- Removed srpm method from LCFG::Build::Tool::RPM as it is no
  longer needed

* Wed Jul 30 2008 21:00 squinney
- switch lcfg-reltool to using LCFG::Build::Tools and updated the
  docs a bit

* Wed Jul 30 2008 20:59 squinney
- Added the srpm command for convenience

* Wed Jul 30 2008 20:58 squinney
- Documented override of the App::Cmd _prepare_command method in
  LCFG::Build::Tools

* Wed Jul 30 2008 20:34 squinney
- attempt to handle abbreviated command names

* Wed Jul 30 2008 19:53 squinney
- Fixed LCFG::Build::Tool::Release run method

* Wed Jul 30 2008 19:48 squinney
- Document why the resultsdir is overridden in
  LCFG::Build::Tool::Release

* Wed Jul 30 2008 19:19 squinney
- Fixed overrides

* Wed Jul 30 2008 19:17 squinney
- Moved resultsdir option to the top-level LCFG::Build::Tool class

* Wed Jul 30 2008 19:08 squinney
- Added majorversion and minorversion tools

* Wed Jul 30 2008 17:31 squinney
- Removed lcfg_add_doc CMake macro as it is unnecessary

* Wed Jul 30 2008 17:30 squinney
- Added documentation for the commands and the options

* Wed Jul 30 2008 17:28 squinney
- Added requirement for perl(MooseX::App::Cmd) to the specfile

* Wed Jul 30 2008 16:24 squinney
- Converted to MooseX::App::Cmd

* Wed Jul 30 2008 15:47 squinney
- Switched to using App::Cmd

* Fri Jul 25 2008 13:49 squinney

* Fri Jul 25 2008 13:48 squinney
- Added handling of logrotate files. Improved handling of bin and
  sbin files

* Fri Jul 25 2008 13:44 squinney
- Added INITDIR macro

* Tue Jul 22 2008 16:44 squinney

* Tue Jul 22 2008 16:43 squinney
- Set MSG variable

* Tue Jul 22 2008 11:40 squinney

* Tue Jul 22 2008 11:39 squinney
- Added ICONDIR, SCRIPTDIR, HAS_PROC and BOOTCOMP cmake variables.
  Also added bash detection

* Tue Jul 22 2008 11:34 squinney
- Fixed cmake lcfg_add_schema macro so it works for all values

* Fri Jul 18 2008 14:19 squinney

* Fri Jul 18 2008 14:18 squinney
- Split out from lcfg_add_pod() an lcfg_add_man() macro

* Fri Jul 18 2008 11:59 squinney

* Fri Jul 18 2008 11:59 squinney
- Added LIBDIR and LIBSECURITYDIR variables. Also now handle the
  correct setting of PERL_LIBDIR and PERL_ARCHDIR based on whether
  the builder wants site or vendor locations.

* Fri Jul 18 2008 11:57 squinney
- Added support for installing perl modules with
  lcfg_add_perl_module() and lcfg_add_perl_tree().

* Thu Jul 17 2008 16:16 squinney

* Thu Jul 17 2008 16:16 squinney
- Improved handling of POD files

* Tue Jul 15 2008 11:51 squinney

* Tue Jul 15 2008 11:50 squinney
- Rewrote the build method in Utils::RPM to avoid using
  RPM4::Spec::rpmbuild which appears to be weirdly broken

* Fri Jul 11 2008 15:22 squinney

* Fri Jul 11 2008 15:20 squinney
- Added detection of the perl executable and fixed usage of lsb
  detection for linux

* Fri Jul 11 2008 15:19 squinney
- Fixed find_trans_files to return relative paths

* Thu Jul 10 2008 10:15 squinney

* Thu Jul 10 2008 10:14 squinney
- Added a shortcut command for building an srpm. Added some error
  handling for when rpmbuild fails

* Thu Jul 10 2008 10:06 squinney

* Thu Jul 10 2008 10:05 squinney
- Rewrote LCFG::Build::Utils::translate_string() so that it only
  substitutes known macros. It is also now much easier to extend
  with new macro styles. Changed the behaviour of
  LCFG::Build::Utils::translate_macro() so it returns undef for an
  unknown macro

* Wed Jul 09 2008 16:56 squinney

* Wed Jul 09 2008 16:56 squinney
- Fixed mistake with printing out the binary RPM filenames in
  Tool::RPM and Tool::DevRPM

* Wed Jul 09 2008 15:21 squinney

* Wed Jul 09 2008 15:20 squinney
- Fixed bug where Tool::Pack used the devel-tree metadata file
  instead of that from the tagged-tree

* Tue Jul 08 2008 10:57 squinney

* Tue Jul 08 2008 10:54 squinney
- This time the logging of results from Tool::RPM and Tool::DevRPM
  might actually be correct...

* Tue Jul 08 2008 10:45 squinney

* Tue Jul 08 2008 10:44 squinney
- Various documentation improvements

* Tue Jul 08 2008 10:28 squinney

* Tue Jul 08 2008 10:28 squinney
- Fixed log messages in Tool::RPM and Tool::DevRPM

* Tue Jul 08 2008 10:21 squinney

* Tue Jul 08 2008 10:21 squinney
- Fixed specfile so that *.in files do not get included

* Tue Jul 08 2008 10:19 squinney
- Added into the specfile a list of Perl module dependencies which
  get missed by the automatic Perl dep finder since they are loaded
  through 'require' rather than 'use'

* Mon Jul 07 2008 15:33 squinney

* Mon Jul 07 2008 15:32 squinney
- Forgot to add the Utils::RPM module into CVS

* Mon Jul 07 2008 15:30 squinney

* Mon Jul 07 2008 15:29 squinney
- Lots more documentation of modules. Moved various files to .in
  versions for macro substitution

* Mon Jul 07 2008 13:00 squinney

* Mon Jul 07 2008 12:59 squinney
- Documented LCFG::Build::Utils and LCFG::Build::Utils::RPM, also
  tidied code to satisfy perllint and perlcritic

* Mon Jul 07 2008 09:49 squinney

* Mon Jul 07 2008 09:49 squinney
- Extracted metafile templating from Utils::RPM to Utils so it can
  be used anywhere. Added a couple of missing module dependencies
  and tidied up a couple of sections

* Mon Jun 30 2008 16:40 squinney
- removed LCFG::Build::Tools::Release as it has been renamed to
  LCFG::Build::Tool::Release

* Wed Jun 25 2008 15:51 squinney

* Wed Jun 25 2008 15:50 squinney
- Fixed prep stage in specfile

* Wed Jun 25 2008 15:48 squinney

* Wed Jun 25 2008 15:48 squinney
- Moved from static specfile to using macros

* Wed Jun 25 2008 15:41 squinney

* Wed Jun 25 2008 15:41 squinney
- Added various extra release tools modules

* Wed Jun 25 2008 15:40 squinney

* Wed Jun 04 2008 17:11 squinney
- Renamed LCFG::Build::Tools to LCFG::Build::Tool

* Wed Jun 04 2008 16:17 squinney
- removed file

* Wed May 28 2008 15:31 squinney

* Tue May 13 2008 12:00 squinney
- Moved lcfg-reltool to this package to simplify dependencies

* Thu May 08 2008 09:51 squinney
- Added more stuff

* Thu May 08 2008 09:29 squinney
- Added lots of stuff

* Tue May 06 2008 17:02 squinney

* Tue May 06 2008 17:02 squinney
- Added lots of files to CVS


