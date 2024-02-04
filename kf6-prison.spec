#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		prison

Summary:	A barcode abstraction layer
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	a0f8a4100bf3f320b42741b75abe4954
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Multimedia-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	hspell-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libdmtx-devel
BuildRequires:	ninja
BuildRequires:	qrencode-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zxing-cpp-nu-devel >= 1.2.0
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Prison has a Prison::AbstractBarcode, which is the base class for the
actual barcode generators, currently Prison::QRCodeBarcode and
Prison::DataMatrixBarcode are the two implemented barcode generators.

Prison currently ships a BarcodeWidget, which is a QWidget with a
barcode painted upon, as well as a BarcodeItem, which is a
QGraphicsItem with a barcode painted upon.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories6/prison.categories
%ghost %{_libdir}/libKF6Prison.so.6
%{_libdir}/libKF6Prison.so.5.*.*
%ghost %{_libdir}/libKF6PrisonScanner.so.6
%{_libdir}/libKF6PrisonScanner.so.5.*.*
%{_libdir}/qt6/qml/org/kde/prison
%{_datadir}/qlogging-categories6/prison.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/Prison
%{_libdir}/cmake/KF6Prison
%{_libdir}/libKF6Prison.so
%{_includedir}/KF6/PrisonScanner
%{_libdir}/libKF6PrisonScanner.so
