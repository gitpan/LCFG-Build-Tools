Name:           perl-LCFG-Build-Tools
Version:        0.0.58
Release:        1
Summary:        LCFG build system tools
License:        gpl
Group:          Development/Libraries
Source0:        LCFG-Build-Tools-0.0.58.tar.gz
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
BuildRequires:  perl(MooseX::App::Cmd) >= 0.06
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl(Test::Differences)
BuildRequires:  perl(DateTime)
Requires:       perl(LCFG::Build::PkgSpec) >= 0.0.22
Requires:       perl(LCFG::Build::VCS) >= 0.0.19
Requires:       perl(YAML::Syck) >= 0.98
Requires:       perl(File::Find::Rule)
Requires:       perl(Template) >= 2.14
Requires:       perl(Archive::Tar), perl(IO::Zlib)
Requires:       perl(RPM4)
Requires:       perl(MooseX::App::Cmd) >= 0.06
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
* Mon Jan 18 2010 SVN: new release

* Mon Jan 18 2010 18:09 squinney@INF.ED.AC.UK
- lib/LCFG/Build/Tools.pm.in: Use the new
  'allow_any_unambiguous_abbrev' option in App::Cmd rather than our
  hacky approach of overriding an internal method

* Mon Jan 18 2010 18:08 squinney@INF.ED.AC.UK
- lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MicroVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/SRPM.pm.in:
  The run() method is now named execute()

* Mon Jan 18 2010 18:07 squinney@INF.ED.AC.UK
- Build.PL.in, LCFG-Build-Tools.spec, META.yml.in, Makefile.PL,
  README: Upgrade to version 0.06 of MooseX::App::Cmd

* Fri Jul 03 2009 14:19 squinney@INF.ED.AC.UK
- Changes, lcfg.yml: LCFG-Build-Tools release: 0.0.57

* Fri Jul 03 2009 14:17 squinney@INF.ED.AC.UK
- lib/LCFG/Build/Tool.pm.in: quiet attribute was missing the
  relevant metaclass specification

* Thu Apr 09 2009 07:53 squinney@INF.ED.AC.UK
- Changes, lcfg.yml: LCFG-Build-Tools release: 0.0.56

* Thu Apr 09 2009 07:53 squinney@INF.ED.AC.UK
- lcfg.yml, lib/LCFG/Build/Utils.pm.in: Fixed a problem with not
  copying the mode when translating files prior to packing. Only
  affects packages using the translate_before_pack option which is
  not standard

* Fri Mar 13 2009 15:50 squinney@INF.ED.AC.UK
- Changes, lcfg.yml: LCFG-Build-Tools release: 0.0.55

* Fri Mar 13 2009 15:49 squinney@INF.ED.AC.UK
- Build.PL.in, LCFG-Build-Tools.spec, META.yml.in, Makefile.PL,
  README, lib/LCFG/Build/Tools.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: switched from Date::Format to
  DateTime

* Wed Mar 11 2009 13:26 squinney@INF.ED.AC.UK
- bin/lcfg-reltool.in, lib/LCFG/Build/Tool.pm.in,
  lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MicroVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/SRPM.pm.in,
  lib/LCFG/Build/Tools.pm.in, lib/LCFG/Build/Utils.pm.in,
  lib/LCFG/Build/Utils/MacOSX.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Set svn:keywords on the
  LCFG::Build::Tools Perl modules and scripts

* Mon Mar 09 2009 16:43 squinney
- lcfg.yml: Removed hardwired version-control type from lcfg.yml to
  allow future transfer to subversion

* Wed Feb 18 2009 14:53 squinney
- Changes, lcfg.yml: Release: 0.0.54

* Wed Feb 18 2009 14:53 squinney
- templates/build.cmake.tt: fixed small error in lcfg_pod2man

* Wed Feb 18 2009 12:36 squinney
- Changes, lcfg.yml: Release: 0.0.53

* Wed Feb 18 2009 12:36 squinney
- lcfg.yml, templates/build.cmake.tt, templates/lcfg.cmake.tt:
  Split the pod2man stuff into its own lcfg_pod2man() macro so it
  can be called separately without installing the pod file into the
  @LCFGPOD@ directory

* Mon Feb 02 2009 14:38 squinney
- lib/LCFG/Build/Utils/RPM.pm.in: added check that the specfile was
  successfully parsed

* Fri Jan 30 2009 14:11 squinney
- Changes, lcfg.yml: Release: 0.0.52

* Fri Jan 30 2009 14:10 squinney
- lcfg.yml, templates/lcfg.cmake.tt: Use CPack for MacOSX package
  building

* Fri Jan 30 2009 14:10 squinney
- lib/LCFG/Build/Utils/MacOSX.pm.in: We do not need to generate
  plist files for MacOSX, CPack will handle it all

* Thu Dec 11 2008 14:43 squinney
- Changes, lcfg.yml: Release: 0.0.51

* Thu Dec 11 2008 14:42 squinney
- lib/LCFG/Build/Tool.pm.in: Added basic auto-detection of the
  version control system

* Wed Dec 10 2008 16:22 squinney
- templates/build.cmake.tt: Automatically create CONFIGDIR for
  components

* Fri Dec 05 2008 12:48 squinney
- Changes, lcfg.yml: Release: 0.0.50

* Fri Dec 05 2008 12:47 squinney
- lcfg.yml, templates/build.cmake.tt: Second attempt to handle
  automatically installing templates

* Fri Dec 05 2008 12:05 squinney
- Changes, lcfg.yml: Release: 0.0.49

* Fri Dec 05 2008 12:05 squinney
- templates/build.cmake.tt: Added support for automatically
  installing templates found in a templates directory

* Thu Nov 27 2008 19:45 squinney
- Changes, lcfg.yml: Release: 0.0.48

* Thu Nov 27 2008 19:45 squinney
- templates/build.cmake.tt: Fixed nagios module path

* Tue Nov 18 2008 14:30 squinney
- Changes, lcfg.yml: Release: 0.0.47

* Tue Nov 18 2008 14:30 squinney
- templates/build.cmake.tt: Added cmake macros
  lcfg_add_nagios_module() to do-the-right-thing with LCFG nagios
  configuration modules and lcfg_add_nagios_support() to call that
  for every module it finds in the nagios directory for a project.
  lcfg_add_nagios_support() is called for every component project,
  if there is not a nagios directory then it achieves nothing.

* Tue Nov 18 2008 14:12 squinney
- Changes, lcfg.yml: Release: 0.0.46

* Tue Nov 18 2008 14:12 squinney
- templates/lcfg.cmake.tt: Improved the fix for the OS_VERSION
  detection. It now behaves the same as the old buildtools. There
  is a new variable naemd OS_ID which gives the complete
  (arch-specific) name of the platform

* Tue Nov 11 2008 10:14 squinney
- Changes, lcfg.yml: Release: 0.0.45

* Tue Nov 11 2008 10:14 squinney
- templates/lcfg.cmake.tt: Fixed OS_VERSION macro for 64bit linux
  platforms

* Wed Oct 29 2008 15:22 squinney
- Changes, lcfg.yml: Release: 0.0.44

* Wed Oct 29 2008 15:21 squinney
- lib/LCFG/Build/Tool/RPM.pm.in: Fixed abstract for
  LCFG::Build::Tool::RPM

* Wed Oct 29 2008 15:20 squinney
- lib/LCFG/Build/Tool/SRPM.pm.in: Fixed abstract for
  LCFG::Build::Tool::SRPM

* Tue Oct 28 2008 10:42 squinney
- Changes, lcfg.yml: Release: 0.0.43

* Tue Oct 28 2008 10:42 squinney
- templates/cmake.tt: Slightly altered cmake.tt template so that it
  is more generic

* Mon Oct 27 2008 09:04 squinney
- Changes, lcfg.yml: Release: 0.0.42

* Mon Oct 27 2008 09:04 squinney
- MANIFEST: Fixed MANIFEST

* Mon Oct 27 2008 09:03 squinney
- Changes, lcfg.yml: Release: 0.0.41

* Mon Oct 27 2008 09:02 squinney
- META.yml.in, bin/lcfg-reltool.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MicroVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/Release.pm.in, lib/LCFG/Build/Tools.pm.in,
  t/01_load.t: Renamed LCFG::Build::Tool::Release as
  LCFG::Build::Tool::MicroVersion

* Wed Oct 08 2008 13:41 squinney
- Changes, lcfg.yml: Release: 0.0.40

* Wed Oct 08 2008 13:40 squinney
- lib/LCFG/Build/Tool/CheckMacros.pm.in: Added a new
  --fix_deprecated option to the CheckMacros tool to replace any
  usage of deprecated macros in the scanned files with the modern
  equivalent

* Fri Oct 03 2008 12:55 squinney
- Changes, lcfg.yml: Release: 0.0.39

* Fri Oct 03 2008 12:54 squinney
- lib/LCFG/Build/Tool/CheckMacros.pm.in, templates/build.cmake.tt:
  Added a new CMake variable - LCFG_TMPLDIR which is the
  component-specific template location. Also added a new CMake
  macro - lcfg_add_template() to install template files into that
  location

* Fri Oct 03 2008 12:53 squinney
- templates/lcfg.cmake.tt: Fixed the setting of the OS_VERSION
  CMake variable on Scientific Linux machines

* Fri Sep 12 2008 14:07 squinney
- Changes, lcfg.yml: Release: 0.0.38

* Fri Sep 12 2008 14:05 squinney
- Build.PL.in, LCFG-Build-Tools.spec, META.yml, META.yml.in,
  Makefile.PL, lcfg.yml, lib/LCFG/Build/Tool.pm.in,
  lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in,
  lib/LCFG/Build/Tool/SRPM.pm.in, lib/LCFG/Build/Tools.pm.in,
  lib/LCFG/Build/Utils.pm.in, lib/LCFG/Build/Utils/MacOSX.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Lots of documentation
  improvements. Various work on making the file and directory path
  handling more platform-independent

* Tue Sep 09 2008 10:38 squinney
- Changes, lcfg.yml: Release: 0.0.37

* Tue Sep 09 2008 10:38 squinney
- lcfg.yml, lib/LCFG/Build/Tool.pm.in,
  lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in,
  lib/LCFG/Build/Tool/SRPM.pm.in, lib/LCFG/Build/Tools.pm.in: Use
  make_immutable for each Moose class. According to the docs this
  should provide a good speed-up in code loading

* Tue Sep 09 2008 09:59 squinney
- Changes, lcfg.yml: Release: 0.0.36

* Tue Sep 09 2008 09:59 squinney
- lcfg.yml, lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/SRPM.pm.in,
  lib/LCFG/Build/Utils.pm.in, lib/LCFG/Build/Utils/MacOSX.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Removed the genmeta options from
  the package building tools. Used Module::Pluggable to add a new
  LCFG::Build::Utils plugins() method which lists all available
  Utils sub-classes. Switched generate_metadata() and build() to be
  methods to make it easier to test for existence and call without
  a string eval

* Mon Sep 08 2008 13:24 squinney
- Changes, lcfg.yml: Release: 0.0.35

* Mon Sep 08 2008 13:22 squinney
- bin/lcfg-reltool.in, lib/LCFG/Build/Tool.pm.in,
  lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in,
  lib/LCFG/Build/Tool/SRPM.pm.in, lib/LCFG/Build/Tools.pm.in,
  lib/LCFG/Build/Utils.pm.in, lib/LCFG/Build/Utils/MacOSX.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Lots of documentation
  improvements

* Mon Sep 08 2008 12:33 squinney
- Changes, lcfg.yml: Release: 0.0.34

* Mon Sep 08 2008 12:32 squinney
- LCFG-Build-Tools.spec, MANIFEST, lcfg.yml: Now using the new
  support for removing input files after substitution. Also
  corrected a couple of bits in the specfile.

* Mon Sep 08 2008 12:26 squinney
- lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/Pack.pm.in, lib/LCFG/Build/Utils.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Added support for removing input
  files after macro substitution has been completed. Also switched
  the source tar file generation sequence so that the packing
  happens last which allows the inclusion of generated metadata
  files

* Mon Sep 08 2008 12:24 squinney
- lib/LCFG/Build/Tools.pm.in: Added some high-level documentation
  to LCFG::Build::Tools

* Mon Sep 08 2008 12:23 squinney
- LCFG-Build-Tools.spec: Improved specfile

* Mon Sep 08 2008 12:23 squinney
- Build.PL.in, Makefile.PL, README: Updated perl build files

* Mon Sep 08 2008 12:22 squinney
- MANIFEST: Updated package MANIFEST

* Tue Sep 02 2008 11:35 squinney
- Changes, lcfg.yml: Release: 0.0.33

* Tue Sep 02 2008 11:34 squinney
- lcfg.yml, lib/LCFG/Build/Utils/MacOSX.pm.in,
  templates/build.cmake.tt: Fixed a problem with pod2man not
  working if the group argument, which gets passed into the
  --center option, was not specified

* Thu Aug 07 2008 12:05 squinney
- Changes, lcfg.yml: Release: 0.0.32

* Thu Aug 07 2008 12:05 squinney
- Build.PL.in, LCFG-Build-Tools.spec, MANIFEST, lcfg.yml,
  lib/LCFG/Build/Tool.pm.in, lib/LCFG/Build/Tool/CheckMacros.pm.in,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in,
  lib/LCFG/Build/Tool/SRPM.pm.in, lib/LCFG/Build/Tools.pm.in,
  lib/LCFG/Build/Utils.pm.in, lib/LCFG/Build/Utils/MacOSX.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in, t/02_macros.t, t/macros.tmpl,
  t/macros.txt: Lots of small changes to satisfy perltidy and
  perlcritic

* Wed Aug 06 2008 15:49 squinney
- Changes, lcfg.yml: Release: 0.0.31

* Wed Aug 06 2008 15:49 squinney
- LCFG-Build-Tools.spec, t, t/01_load.t: Added a basic test to
  check that all Perl modules are loadable. Also added all the
  necessary build dependencies so this check can be carried out in
  a chroot

* Wed Aug 06 2008 14:25 squinney
- Changes, lcfg.yml: Release: 0.0.30

* Wed Aug 06 2008 14:24 squinney
- Build.PL.in, LCFG-Build-Tools.spec, MANIFEST, lcfg.yml,
  lib/LCFG/Build/Tool/DevOSXPkg.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/OSXPkg.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Utils.pm.in, lib/LCFG/Build/Utils/MacOSX.pm.in,
  templates/Description.plist.tmpl, templates/Info.plist.tmpl:
  Added basic MacOSX support, stubs for the ospkg and devospkg
  command modules are now supplied

* Tue Aug 05 2008 14:29 squinney
- Changes, lcfg.yml: Release: 0.0.29

* Tue Aug 05 2008 14:29 squinney
- lib/LCFG/Build/Tool/CheckMacros.pm.in: Added a new checkmacros
  command

* Wed Jul 30 2008 20:17 squinney
- Changes, lcfg.yml: Release: 0.0.28

* Wed Jul 30 2008 20:16 squinney
- lib/LCFG/Build/Tool/SRPM.pm.in: overrode sourceonly and deps
  attributes from LCFG::Build::Tool::SRPM so they don't show up as
  options for the srpm command

* Wed Jul 30 2008 20:14 squinney
- lib/LCFG/Build/Tool/RPM.pm.in: Removed srpm method from
  LCFG::Build::Tool::RPM as it is no longer needed

* Wed Jul 30 2008 20:00 squinney
- bin/lcfg-reltool.in: switch lcfg-reltool to using
  LCFG::Build::Tools and updated the docs a bit

* Wed Jul 30 2008 19:59 squinney
- lib/LCFG/Build/Tool/SRPM.pm.in: Added the srpm command for
  convenience

* Wed Jul 30 2008 19:58 squinney
- lib/LCFG/Build/Tools.pm.in: Documented override of the App::Cmd
  _prepare_command method in LCFG::Build::Tools

* Wed Jul 30 2008 19:34 squinney
- lib/LCFG/Build/Tools.pm.in: attempt to handle abbreviated command
  names

* Wed Jul 30 2008 18:53 squinney
- lib/LCFG/Build/Tool/Release.pm.in: Fixed
  LCFG::Build::Tool::Release run method

* Wed Jul 30 2008 18:48 squinney
- lib/LCFG/Build/Tool/Release.pm.in: Document why the resultsdir is
  overridden in LCFG::Build::Tool::Release

* Wed Jul 30 2008 18:19 squinney
- lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in: Fixed overrides

* Wed Jul 30 2008 18:17 squinney
- lib/LCFG/Build/Tool.pm.in, lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/Pack.pm.in: Moved resultsdir option to the
  top-level LCFG::Build::Tool class

* Wed Jul 30 2008 18:08 squinney
- lib/LCFG/Build/Tool/MajorVersion.pm.in,
  lib/LCFG/Build/Tool/MinorVersion.pm.in,
  lib/LCFG/Build/Tool/Release.pm.in: Added majorversion and
  minorversion tools

* Wed Jul 30 2008 16:31 squinney
- templates/build.cmake.tt: Removed lcfg_add_doc CMake macro as it
  is unnecessary

* Wed Jul 30 2008 16:30 squinney
- lib/LCFG/Build/Tool.pm.in, lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in:
  Added documentation for the commands and the options

* Wed Jul 30 2008 16:28 squinney
- LCFG-Build-Tools.spec: Added requirement for
  perl(MooseX::App::Cmd) to the specfile

* Wed Jul 30 2008 15:24 squinney
- lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in:
  Converted to MooseX::App::Cmd

* Wed Jul 30 2008 14:47 squinney
- lib/LCFG/Build/Tool.pm.in, lib/LCFG/Build/Tools.pm.in: Switched
  to using App::Cmd

* Fri Jul 25 2008 12:49 squinney
- Changes, lcfg.yml: Release: 0.0.27

* Fri Jul 25 2008 12:48 squinney
- lcfg.yml, templates/build.cmake.tt, templates/lcfg.cmake.tt:
  Added handling of logrotate files. Improved handling of bin and
  sbin files

* Fri Jul 25 2008 12:44 squinney
- lcfg_config.yml: Added INITDIR macro

* Tue Jul 22 2008 15:44 squinney
- Changes, lcfg.yml: Release: 0.0.26

* Tue Jul 22 2008 15:43 squinney
- templates/lcfg.cmake.tt: Set MSG variable

* Tue Jul 22 2008 10:40 squinney
- Changes, lcfg.yml: Release: 0.0.25

* Tue Jul 22 2008 10:39 squinney
- templates/lcfg.cmake.tt: Added ICONDIR, SCRIPTDIR, HAS_PROC and
  BOOTCOMP cmake variables. Also added bash detection

* Tue Jul 22 2008 10:34 squinney
- templates/build.cmake.tt: Fixed cmake lcfg_add_schema macro so it
  works for all values

* Fri Jul 18 2008 13:19 squinney
- Changes, lcfg.yml: Release: 0.0.24

* Fri Jul 18 2008 13:18 squinney
- templates/build.cmake.tt: Split out from lcfg_add_pod() an
  lcfg_add_man() macro

* Fri Jul 18 2008 10:59 squinney
- Changes, lcfg.yml: Release: 0.0.23

* Fri Jul 18 2008 10:59 squinney
- templates/lcfg.cmake.tt: Added LIBDIR and LIBSECURITYDIR
  variables. Also now handle the correct setting of PERL_LIBDIR and
  PERL_ARCHDIR based on whether the builder wants site or vendor
  locations.

* Fri Jul 18 2008 10:57 squinney
- templates/build.cmake.tt: Added support for installing perl
  modules with lcfg_add_perl_module() and lcfg_add_perl_tree().

* Thu Jul 17 2008 15:16 squinney
- Changes, lcfg.yml: Release: 0.0.22

* Thu Jul 17 2008 15:16 squinney
- lcfg.yml, templates/build.cmake.tt: Improved handling of POD
  files

* Tue Jul 15 2008 10:51 squinney
- Changes, lcfg.yml: Release: 0.0.21

* Tue Jul 15 2008 10:50 squinney
- lib/LCFG/Build/Utils/RPM.pm.in: Rewrote the build method in
  Utils::RPM to avoid using RPM4::Spec::rpmbuild which appears to
  be weirdly broken

* Fri Jul 11 2008 14:22 squinney
- Changes, lcfg.yml: Release: 0.0.20

* Fri Jul 11 2008 14:20 squinney
- templates/build.cmake.tt, templates/lcfg.cmake.tt: Added
  detection of the perl executable and fixed usage of lsb detection
  for linux

* Fri Jul 11 2008 14:19 squinney
- lib/LCFG/Build/Utils.pm.in: Fixed find_trans_files to return
  relative paths

* Thu Jul 10 2008 09:15 squinney
- Changes, lcfg.yml: Release: 0.0.19

* Thu Jul 10 2008 09:14 squinney
- bin/lcfg-reltool.in, lib/LCFG/Build/Tool/RPM.pm.in,
  lib/LCFG/Build/Utils/RPM.pm.in: Added a shortcut command for
  building an srpm. Added some error handling for when rpmbuild
  fails

* Thu Jul 10 2008 09:06 squinney
- Changes, lcfg.yml: Release: 0.0.18

* Thu Jul 10 2008 09:05 squinney
- lcfg.yml, lib/LCFG/Build/Utils.pm.in: Rewrote
  LCFG::Build::Utils::translate_string() so that it only
  substitutes known macros. It is also now much easier to extend
  with new macro styles. Changed the behaviour of
  LCFG::Build::Utils::translate_macro() so it returns undef for an
  unknown macro

* Wed Jul 09 2008 15:56 squinney
- Changes, lcfg.yml: Release: 0.0.17

* Wed Jul 09 2008 15:56 squinney
- lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/RPM.pm.in:
  Fixed mistake with printing out the binary RPM filenames in
  Tool::RPM and Tool::DevRPM

* Wed Jul 09 2008 14:21 squinney
- Changes, lcfg.yml: Release: 0.0.16

* Wed Jul 09 2008 14:20 squinney
- lcfg.yml, lib/LCFG/Build/Tool/DevRPM.pm.in,
  lib/LCFG/Build/Tool/Pack.pm.in: Fixed bug where Tool::Pack used
  the devel-tree metadata file instead of that from the tagged-tree

* Tue Jul 08 2008 09:57 squinney
- Changes, lcfg.yml: Release: 0.0.15

* Tue Jul 08 2008 09:54 squinney
- lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/RPM.pm.in:
  This time the logging of results from Tool::RPM and Tool::DevRPM
  might actually be correct...

* Tue Jul 08 2008 09:45 squinney
- Changes, lcfg.yml: Release: 0.0.14

* Tue Jul 08 2008 09:44 squinney
- lib/LCFG/Build/Tool/DevPack.pm.in,
  lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/Pack.pm.in,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm.in,
  lib/LCFG/Build/Tools.pm.in: Various documentation improvements

* Tue Jul 08 2008 09:28 squinney
- Changes, lcfg.yml: Release: 0.0.13

* Tue Jul 08 2008 09:28 squinney
- lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/RPM.pm.in:
  Fixed log messages in Tool::RPM and Tool::DevRPM

* Tue Jul 08 2008 09:21 squinney
- Changes, lcfg.yml: Release: 0.0.12

* Tue Jul 08 2008 09:21 squinney
- LCFG-Build-Tools.spec: Fixed specfile so that *.in files do not
  get included

* Tue Jul 08 2008 09:19 squinney
- LCFG-Build-Tools.spec: Added into the specfile a list of Perl
  module dependencies which get missed by the automatic Perl dep
  finder since they are loaded through 'require' rather than 'use'

* Mon Jul 07 2008 14:33 squinney
- Changes, lcfg.yml: Release: 0.0.11

* Mon Jul 07 2008 14:32 squinney
- lib/LCFG/Build/Utils, lib/LCFG/Build/Utils/RPM.pm.in: Forgot to
  add the Utils::RPM module into CVS

* Mon Jul 07 2008 14:30 squinney
- Changes, lcfg.yml: Release: 0.0.10

* Mon Jul 07 2008 14:29 squinney
- Build.PL, Build.PL.in, bin/lcfg-reltool, bin/lcfg-reltool.in,
  lib/LCFG/Build/Tool.pm, lib/LCFG/Build/Tool.pm.in,
  lib/LCFG/Build/Tool/DevPack.pm,
  lib/LCFG/Build/Tool/DevPack.pm.in, lib/LCFG/Build/Tool/DevRPM.pm,
  lib/LCFG/Build/Tool/DevRPM.pm.in, lib/LCFG/Build/Tool/Pack.pm,
  lib/LCFG/Build/Tool/Pack.pm.in, lib/LCFG/Build/Tool/RPM.pm,
  lib/LCFG/Build/Tool/RPM.pm.in, lib/LCFG/Build/Tool/Release.pm,
  lib/LCFG/Build/Tool/Release.pm.in, lib/LCFG/Build/Tools.pm,
  lib/LCFG/Build/Tools.pm.in, lib/LCFG/Build/Utils,
  lib/LCFG/Build/Utils.pm, lib/LCFG/Build/Utils.pm.in: Lots more
  documentation of modules. Moved various files to .in versions for
  macro substitution

* Mon Jul 07 2008 12:00 squinney
- Changes, lcfg.yml: Release: 0.0.9

* Mon Jul 07 2008 11:59 squinney
- Build.PL, lib/LCFG/Build/Utils.pm, lib/LCFG/Build/Utils/RPM.pm:
  Documented LCFG::Build::Utils and LCFG::Build::Utils::RPM, also
  tidied code to satisfy perllint and perlcritic

* Mon Jul 07 2008 08:49 squinney
- Changes, lcfg.yml: Release: 0.0.8

* Mon Jul 07 2008 08:49 squinney
- lcfg.yml, lib/LCFG/Build/Tool.pm, lib/LCFG/Build/Tool/Release.pm,
  lib/LCFG/Build/Utils.pm, lib/LCFG/Build/Utils/RPM.pm: Extracted
  metafile templating from Utils::RPM to Utils so it can be used
  anywhere. Added a couple of missing module dependencies and
  tidied up a couple of sections

* Mon Jun 30 2008 15:40 squinney
- lib/LCFG/Build/Tools: removed LCFG::Build::Tools::Release as it
  has been renamed to LCFG::Build::Tool::Release

* Wed Jun 25 2008 14:51 squinney
- Changes, lcfg.yml: Release: 0.0.7

* Wed Jun 25 2008 14:50 squinney
- LCFG-Build-Tools.spec: Fixed prep stage in specfile

* Wed Jun 25 2008 14:48 squinney
- Changes, lcfg.yml: Release: 0.0.6

* Wed Jun 25 2008 14:48 squinney
- LCFG-Build-Tools.spec: Moved from static specfile to using macros

* Wed Jun 25 2008 14:41 squinney
- Changes, lcfg.yml: Release: 0.0.5

* Wed Jun 25 2008 14:41 squinney
- lib/LCFG/Build/Tool/DevRPM.pm, lib/LCFG/Build/Tool/Pack.pm,
  lib/LCFG/Build/Tool/RPM.pm: Added various extra release tools
  modules

* Wed Jun 25 2008 14:40 squinney
- Changes, LCFG-Build-Tools.spec, MANIFEST, META.yml, Makefile.PL,
  bin/lcfg-buildrpm, bin/lcfg-buildtool, bin/lcfg-gencmake,
  bin/lcfg-reltool, lcfg.yml, lib/LCFG/Build/Tool.pm,
  lib/LCFG/Build/Tool/DevPack.pm, lib/LCFG/Build/Tool/Release.pm,
  lib/LCFG/Build/Tools.pm, lib/LCFG/Build/Utils.pm,
  lib/LCFG/Build/Utils/RPM.pm: Release: 0.0.4

* Wed Jun 04 2008 16:13 squinney
- Build.PL, MANIFEST, MANIFEST.SKIP, META.yml, Makefile.PL, README,
  bin/lcfg-reltool, lcfg.yml, lib/LCFG/Build/Tool,
  lib/LCFG/Build/Tool.pm, lib/LCFG/Build/Tool/DevPack.pm,
  lib/LCFG/Build/Tool/Release.pm, lib/LCFG/Build/Tools/Release.pm,
  lib/LCFG/Build/Utils, lib/LCFG/Build/Utils.pm,
  lib/LCFG/Build/Utils/RPM.pm: Added lots more code

* Wed Jun 04 2008 16:11 squinney
- lib/LCFG/Build/Tools.pm: Renamed LCFG::Build::Tools to
  LCFG::Build::Tool

* Wed Jun 04 2008 15:17 squinney
- lib/LCFG/Build/Tools/RPM.pm: removed file

* Wed May 28 2008 14:31 squinney
- Changes, bin/lcfg-reltool, lcfg.yml, lib/LCFG/Build/Tools.pm,
  lib/LCFG/Build/Tools/Release.pm: Release: 0.0.3

* Tue May 13 2008 11:00 squinney
- LCFG-Build-Tools.spec, bin/lcfg-buildtool, bin/lcfg-reltool,
  lib/LCFG/Build/Tools.pm, lib/LCFG/Build/Tools/RPM.pm,
  templates/build.cmake.tt, templates/lcfg.cmake.tt: Moved
  lcfg-reltool to this package to simplify dependencies

* Thu May 08 2008 08:51 squinney
- Changes, LCFG-Build-Tools.spec, bin/lcfg-buildrpm,
  lib/LCFG/Build/Tools, lib/LCFG/Build/Tools/RPM.pm: Added more
  stuff

* Thu May 08 2008 08:29 squinney
- bin/lcfg-gencmake, lcfg.yml, lib/LCFG/Build/Tools.pm,
  mapping_config.yml, templates/build.cmake.tt, templates/cmake.tt,
  templates/lcfg.cmake.tt: Added lots of stuff

* Tue May 06 2008 16:02 squinney
- lcfg.yml: Release: 0.0.2

* Tue May 06 2008 16:02 squinney
- bin, bin/lcfg-buildtool, bin/lcfg-gencmake, lcfg.yml,
  lcfg_config.yml, lib, lib/LCFG, lib/LCFG/Build,
  lib/LCFG/Build/Tools.pm, mapping_config.yml, templates,
  templates/build.cmake.tt, templates/cmake.tt,
  templates/lcfg.cmake.tt: Added lots of files to CVS

* Tue May 06 2008 16:02 
- .: Standard project directories initialized by cvs2svn.


