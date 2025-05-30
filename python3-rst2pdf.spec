#
# Conditional build:
%bcond_without	doc	# manual and documentation

Summary:	Convert reStructured Text to PDF via ReportLab
Summary(pl.UTF-8):	Konwersja formatu reStructured Text do PDF przy użyciu ReportLaba
Name:		python3-rst2pdf
Version:	0.103.1
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/rst2pdf/
Source0:	https://files.pythonhosted.org/packages/source/r/rst2pdf/rst2pdf-%{version}.tar.gz
# Source0-md5:	e806058707cd622eccb97f15d4d71da9
URL:		https://rst2pdf.org/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:64
BuildRequires:	python3-setuptools_scm >= 8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	docutils
BuildRequires:	python3-PyYAML
BuildRequires:	python3-docutils
BuildRequires:	python3-importlib_metadata
BuildRequires:	python3-jinja2
BuildRequires:	python3-packaging
BuildRequires:	python3-pygments
BuildRequires:	python3-reportlab
# gen_docs.sh calls rst2pdf from $PATH
BuildRequires:	python3-rst2pdf >= 0.99
BuildRequires:	python3-smartypants
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The usual way of creating PDF from reStructuredText is by going
through LaTeX. This tool provides an alternative by producing PDF
directly using the ReportLab library.

%description -l pl.UTF-8
Najczęstszym sposobem tworzenia dokumentów PDF z formatu
reStructuredText jest przejście przez LaTeX. To narzędzie udostępnia
alternatywną metodę, tworząc PDF bezpośrednio przy użyciu biblioteki
ReportLab.

%package doc
Summary:	Manual for rst2pdf library
Summary(pl.UTF-8):	Podręcznik do biblioteki rst2pdf
Group:		Documentation

%description doc
Manual for rst2pdf library.

%description doc -l pl.UTF-8
Podręcznik do biblioteki rst2pdf.

%prep
%setup -q -n rst2pdf-%{version}

%{__sed} -i -e '2iset -eu' -e 's,python ,%{__python3} ,' doc/gen_docs.sh

%build
%py3_build_pyproject

%if %{with doc}
cd doc
./gen_docs.sh
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/rst2pdf{,-3}
ln -sf rst2pdf-3 $RPM_BUILD_ROOT%{_bindir}/rst2pdf

%if %{with doc}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p doc/output/rst2pdf.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst Contributors.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/rst2pdf
%attr(755,root,root) %{_bindir}/rst2pdf-3
%{py3_sitescriptdir}/rst2pdf
%{py3_sitescriptdir}/rst2pdf-%{version}.dist-info
%if %{with doc}
%{_mandir}/man1/rst2pdf.1*
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/output/html/{assets,manual.html} doc/output/pdf/manual.pdf
%endif
