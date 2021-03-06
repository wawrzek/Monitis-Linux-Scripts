Summary: MonitisMonitorManager Perl module
Name: perl-MonitisMonitorManager
Version: 3.9
Release: 1
License: GPL or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/MonitisMonitorManager/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: perl
Requires: perl
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source: perl-MonitisMonitorManager.tar.gz

%description
%{summary}.

%prep
%setup -q -n perl-MonitisMonitorManager-%{version}

%build
# force installation to go to /usr and not /usr/local as the init.d service
# needs stuff in /usr/bin/monitis-m3
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL PREFIX=$RPM_BUILD_ROOT/usr
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

# this is the original line, but we've set the PREFIX previously
#make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
make pure_install

find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for brp in %{_prefix}/lib/rpm/%{_build_vendor}/brp-compress \
  %{_prefix}/lib/rpm/brp-compress
do
  [ -x $brp ] && $brp && break
done


find $RPM_BUILD_ROOT -type f \
| sed "s@^$RPM_BUILD_ROOT@@g" \
> %{name}-%{version}-%{release}-filelist

eval `%{__perl} -V:archname -V:installsitelib -V:installvendorlib -V:installprivlib`
for d in $installsitelib $installvendorlib $installprivlib; do
  [ -z "$d" -o "$d" = "UNKNOWN" -o ! -d "$RPM_BUILD_ROOT$d" ] && continue
  find $RPM_BUILD_ROOT$d/* -type d \
  | grep -v "/$archname\(/auto\)\?$" \
  | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
  >> %{name}-%{version}-%{release}-filelist
done

if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

cp -av etc $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/etc/init.d/rpm.m3 $RPM_BUILD_ROOT/etc/init.d/m3
rm -f $RPM_BUILD_ROOT/etc/init.d/deb.m3

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)
%doc Changes README eg
/etc/init.d/m3
%config(noreplace) /etc/m3.d
%config(noreplace) /etc/logrotate.d/m3
%config(noreplace) /etc/sysconfig/m3

%changelog
* Fri May 18 2012 Dan Fruehauf <malkodan@gmail.com> - 3.6-1
- Added raw command for listing and deleting monitors

* Tue May 1 2012 Dan Fruehauf <malkodan@gmail.com> - 3.4-1
- Initial release which actually works

* Mon Apr 30 2012 Dan Fruehauf <malkodan@gmail.com> - 3.3-8
- Specfile autogenerated with command '/usr/bin/cpanflute2 --just-spec /tmp/MonitisMonitorManager-3.3.tar.gz'

