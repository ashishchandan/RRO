Summary: The "Cran R" program from GNU
Name: :::RPM_NAME:::
Version: :::RPM_VERSION:::
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPLv3+
Group: Development/Tools

BuildRequires: ed, gcc, gcc-c++, gcc-objc
BuildRequires: perl, texinfo
BuildRequires: libpng-devel, libjpeg-devel, readline5-devel, libtiff-devel
BuildRequires: libSM-devel, libX11-devel, libICE-devel,
BuildRequires: libXt-devel, libXmu-devel, pango-devel
BuildRequires: cairo-devel, ncurses-devel
Requires: make, gcc, gcc-fortran,  libpng, readline, cairo-devel
Requires: libtiff, libjpeg8, ghostscript-fonts-std, curl
Requires(post): info
Requires(preun): info

%define libnn lib64
%define DIR_VERSION :::RPM_VERSION:::
%define r_version :::R_VERSION:::

%description
'GNU S' - A language and environment for statistical computing and
graphics. R is similar to the award-winning S system, which was
developed at Bell Laboratories by John Chambers et al. It provides a
wide variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%prep
%setup -q

%build
./configure --prefix=%{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version} --enable-R-shlib --with-tcltk --with-cairo --with-libpng --with-libtiff --with-x=no --with-lapack --enable-BLAS-shlib LIBR="-lpthread" --enable-memory-profiling

make -j8

%install
%make_install
# make install
# %find_lang %{name}
rm -f %{buildroot}/%{_infodir}/dir
rm -rf %{buildroot}/lib
cp %{_topdir}/Rprofile.site %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/lib64/R/etc
cp %{_topdir}/README.txt %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}
cp %{_topdir}/COPYING %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}
cp %{_topdir}/ThirdPartyNotices.pdf %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}

if [ -d "/tmp/rro_extra_pkgs" ]
then
    pushd /tmp/rro_extra_pkgs
    for filename in :::EXTRA_PKGS:::; do
        %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/lib64/R/bin/R --vanilla --install-tests CMD INSTALL ${filename}
    done
    popd
	pushd %{buildroot}%{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/lib64/R/library
	if [ -d "foreach" ]; then
	    rm -rf foreach
	fi
	if [ -d "iterators" ]; then
	    rm -rf iterators
	fi
	popd
fi

%post
if test "${RPM_INSTALL_PREFIX0}" = ""; then
    RPM_INSTALL_PREFIX0=/usr/
fi
rm -f /usr/bin/R
rm -f /usr/bin/Rscript
ln -s $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/%libnn/R/bin/R $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/R
ln -s $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/%libnn/R/bin/Rscript $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/Rscript
ln -s $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/%libnn/R/bin/R /usr/bin
ln -s $RPM_INSTALL_PREFIX0/%{_lib}/%{name}-%{DIR_VERSION}/R-%{r_version}/%libnn/R/bin/Rscript /usr/bin

%postun
if test "${revo_prefix}" = ""; then
    revo_prefix=/usr/
fi
revo_prefix=`echo "$revo_prefix" | sed "s/\/*$//"`
if test -h ${revo_prefix}/bin/R
    then
    rm -f ${revo_prefix}/%{libnn}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/R
    rm -f ${revo_prefix}/%{libnn}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/Rscript
    rm -f /usr/bin/R
    rm -f /usr/bin/Rscript
else
    echo "Warning: cannot find Revo executables.  Check revo_prefix."
fi

# %files -f %{name}.lang
%files
%defattr(-, root, root)
%{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/
%{_libdir}/%{name}-%{DIR_VERSION}/COPYING
%{_libdir}/%{name}-%{DIR_VERSION}/README.txt
%{_libdir}/%{name}-%{DIR_VERSION}/ThirdPartyNotices.pdf

# %exclude %{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/%{libnn}/R/etc/repositories
# %exclude %{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/%{libnn}/R/lib/libRblas.so
# %exclude %{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/%{libnn}/R/lib/libRlapack.so
%exclude %{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/R
%exclude %{_libdir}/%{name}-%{DIR_VERSION}/R-%{r_version}/bin/Rscript

%changelog
* Tue Sep 06 2011 The Coon of Ty <Ty@coon.org> 2.8-1
- Initial version of the package
ORG-LIST-END-MARKER
