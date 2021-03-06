#
#    fty-asset-mapping-rest - Asset mapping REST API
#
#   NOTE: This file was customized after generation,
#   take care to keep this during updates.
#
#    Copyright (C) 2018 - 2020 Eaton
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# To build with draft APIs, use "--with drafts" in rpmbuild for local builds or add
#   Macros:
#   %_with_drafts 1
# at the BOTTOM of the OBS prjconf
%bcond_with drafts
%if %{with drafts}
%define DRAFTS yes
%else
%define DRAFTS no
%endif
Name:           fty-asset-mapping-rest
Version:        1.0.0
Release:        1
Summary:        asset mapping rest api
License:        GPL-2.0+
URL:            https://42ity.org
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xmlto
# Note that with current implementation of zproject use-cxx-gcc-4-9 option,
# this effectively hardcodes the use of specifically 4.9, not allowing for
# "4.9 or newer".
BuildRequires:  devtoolset-3-gcc devtoolset-3-gcc-c++
BuildRequires:  gcc-c++ >= 4.9.0
BuildRequires:  libsodium-devel
BuildRequires:  zeromq-devel
BuildRequires:  czmq-devel >= 3.0.2
BuildRequires:  cxxtools-devel
BuildRequires:  fty-common-devel
BuildRequires:  fty-common-logging-devel
BuildRequires:  fty-common-mlm-devel
BuildRequires:  fty-common-rest-devel
BuildRequires:  fty-security-wallet-devel
BuildRequires:  tntdb-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
fty-asset-mapping-rest asset mapping rest api.

%package -n libfty_asset_mapping_rest1
Group:          System/Libraries
Summary:        asset mapping rest api shared library

%description -n libfty_asset_mapping_rest1
This package contains shared library for fty-asset-mapping-rest: asset mapping rest api

%post -n libfty_asset_mapping_rest1 -p /sbin/ldconfig
%postun -n libfty_asset_mapping_rest1 -p /sbin/ldconfig

# Note: the .so file is delivered as part of main package for tntnet to find it
%files -n libfty_asset_mapping_rest1
%defattr(-,root,root)
%{_libdir}/libfty_asset_mapping_rest.so.*
%{_libdir}/libfty_asset_mapping_rest.so

%package devel
Summary:        asset mapping rest api
Group:          System/Libraries
Requires:       libfty_asset_mapping_rest1 = %{version}
Requires:       libsodium-devel
Requires:       zeromq-devel
Requires:       czmq-devel >= 3.0.2
Requires:       cxxtools-devel
Requires:       fty-common-devel
Requires:       fty-common-logging-devel
Requires:       fty-common-mlm-devel
Requires:       fty-common-rest-devel
Requires:       fty-security-wallet-devel
Requires:       tntdb-devel

%description devel
asset mapping rest api development tools
This package contains development files for fty-asset-mapping-rest: asset mapping rest api

# Note: the .so file is delivered as part of main package for tntnet to find it
%files devel
%defattr(-,root,root)
%{_includedir}/*
###%{_libdir}/libfty_asset_mapping_rest.so
%{_libdir}/pkgconfig/libfty_asset_mapping_rest.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%prep

%setup -q

%build
sh autogen.sh
%{configure} --enable-drafts=%{DRAFTS}
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f


%changelog
