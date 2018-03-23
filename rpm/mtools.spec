#specfile originally created for Fedora, modified for Moblin Linux
Summary: Programs for accessing MS-DOS disks without mounting the disks
Name: mtools
Version: 0
Release: 1
License: GPLv2+
Group: Applications/System
Source: %{name}-%{version}.tar.bz2
Url: http://mtools.linux.lu/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

BuildRequires: texinfo, autoconf

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 XDF disks, and 2m disks

Mtools should be installed if you need to use MS-DOS disks

%prep
%setup -q -n %{name}-%{version}

%build
# Hack - this project does not use automake nor libtool so config.{guess,sub}
# would not be updated and the packaged version is too old
rm config.{guess,sub}
automake --add-missing &>/dev/null ||:

autoreconf -fiv
%configure --disable-floppyd
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc $RPM_BUILD_ROOT/%{_infodir}
%makeinstall
install -m644 mtools.conf $RPM_BUILD_ROOT/etc
gzip -9f $RPM_BUILD_ROOT/%{_infodir}/*

# We aren't shipping this.
find $RPM_BUILD_ROOT -name "floppyd*" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -e %{_infodir}/%{name}.info ] && /sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :;

%preun
if [ "$1" -eq 0 ]; then
    [ -e %{_infodir}/%{name}.info ] && /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :;
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/mtools.conf
%doc COPYING README Release.notes
/usr/bin/*
%doc %{_mandir}/*/*
%doc %{_infodir}/*

