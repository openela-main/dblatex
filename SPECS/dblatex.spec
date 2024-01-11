%{!?python3_sitelib: %define python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:       dblatex
Version:    0.3.10
Release:    8%{?dist}
Summary:    DocBook to LaTeX/ConTeXt Publishing
BuildArch:  noarch
# Most of package is GPLv2+, except:
# xsl/ directory is DMIT
# lib/dbtexmf/core/sgmlent.txt is Public Domain
# latex/misc/enumitem.sty, multirow2.sry and ragged2e.sty are LPPL
# latex/misc/lastpage.sty is GPLv2 (no +)
# latex/misc/passivetex is MIT (not included in binary RPM so not listed)
License:    GPLv2+ and GPLv2 and LPPL and DMIT and Public Domain
URL:        http://dblatex.sourceforge.net/
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source1 is from http://docbook.sourceforge.net/release/xsl/current/COPYING
Source1:    COPYING-docbook-xsl
Patch0:     dblatex-0.3.10-enable-python3.patch
Patch1:     dblatex-0.3.10-disable-debian.patch
Patch2:     dblatex-0.3.10-use-shutil-which.patch
Patch3:     dblatex-0.3.10-fix-shebangs.patch

BuildRequires:  python3-devel
BuildRequires:  libxslt
BuildRequires:  texlive-base
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-collection-xetex
BuildRequires:  texlive-collection-htmlxml
BuildRequires:  texlive-xmltex-bin
BuildRequires:  texlive-anysize
BuildRequires:  texlive-appendix
BuildRequires:  texlive-changebar
BuildRequires:  texlive-fancybox
BuildRequires:  texlive-jknapltx
BuildRequires:  texlive-multirow
BuildRequires:  texlive-overpic
BuildRequires:  texlive-pdfpages
BuildRequires:  texlive-subfigure
BuildRequires:  texlive-stmaryrd
BuildRequires:  texlive-wasysym
Requires:       texlive-base
Requires:       texlive-collection-latex
Requires:       texlive-collection-xetex
Requires:       texlive-collection-htmlxml
Requires:       texlive-collection-fontsrecommended
Requires:       texlive-passivetex
Requires:       texlive-xmltex texlive-xmltex-bin
Requires:       texlive-anysize
Requires:       texlive-appendix
Requires:       texlive-bibtopic
Requires:       texlive-changebar
Requires:       texlive-ec
Requires:       texlive-fancybox
Requires:       texlive-jknapltx
Requires:       texlive-multirow
Requires:       texlive-overpic
Requires:       texlive-passivetex
Requires:       texlive-pdfpages
Requires:       texlive-subfigure
Requires:       texlive-stmaryrd
Requires:       texlive-wasysym
Requires:       texlive-xmltex-bin
Requires:       libxslt docbook-dtds
Recommends:     texlive-epstopdf-bin
Recommends:     transfig
Recommends:     inkscape

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

Authors:
--------
   Benoît Guillon <marsgui at users dot sourceforge dot net>
   Andreas Hoenen <andreas dot hoenen at arcor dot de>


%prep
%setup -q
%patch0 -p1 -b .enable-python3
%patch1 -p1 -b .disable-debian
%patch2 -p1 -b .use-shutil-which
%patch3 -p1 -b .fix-shebangs

rm -rf lib/contrib

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --root $RPM_BUILD_ROOT
# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/ xelatex/; do
  rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

## also move .xetex files
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.xetex' ` ; do
  mv $file $RPM_BUILD_ROOT%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/`basename $file`;
done

rmdir $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl


%files
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{python3_sitelib}/dbtexmf/
%{python3_sitelib}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texlive/texmf-dist/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex

%post -p /usr/bin/texhash

%postun -p /usr/bin/texhash

%changelog
* Wed Jun 13 2018 Nikola Forró <nforro@redhat.com> - 0.3.10-8
- switch to Python 3 (#1590857)

* Wed May 16 2018 Than Ngo <than@redhat.com> - 0.3.10-7
- fixed bz#1545772 - FTBFS

* Wed Apr 18 2018 Nikola Forró <nforro@redhat.com> - 0.3.10-6
- remove ImageMagick dependency (#1564991)

* Wed Apr 11 2018 Nikola Forró <nforro@redhat.com> - 0.3.10-5
- make non-critical graphic tools weak dependencies
- recommend inkscape, which can be used to convert SVG images

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.10-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Michael J Gruber <mjg@fedoraproject.org> - 0.3.10-1
- rebase with upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.9-1
- bugfix and feature release

* Mon Aug 01 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.8-1
- bugfix and feature release

* Mon Aug 01 2016 Michael J Gruber <mjg@fedoraproject.org> - 0.3.7-1
- bugfix release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 jchaloup <jchaloup@redhat.com> - 0.3.6-1
- Update to 0.3.6
  resolves: #1222169

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 jchaloup <jchaloup@redhat.com> - 0.3.5-1
- Update to 0.3.5.

* Thu Aug 08 2013 Michael J Gruber <mjg@fedoraproject.org> - 0.3.4-8
- Merge in licensing changes from  Stanislav Ochotnicky <sochotnicky@redhat.com>:
-* Mon Jul 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.4-8
-- Add Public Domain license and licensing comment
-* Mon Jul 29 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.4-7
-- Add DMIT, GPLv2 and LPPL licenses
-- Fix space and tab mixing
-- Cleanup old spec file parts

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Michael J Gruber <mjg@fedoraproject.org> - 0.3.4-6
- Add mising R texlive-multirow.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Benjamin De Kosnik  <bkoz@redhat.com> - 0.3.4-1
- Update to 0.3.4.
- Adjust for texlive rebase.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Apr 12 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.3-1
- Update to 0.3
- Cleanup spec: drop some unnecessary conditionals for old releases (< F-11)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Neal Becker <ndbecker2@gmail.com> - 0.2.10-2
- remove dblatex-0.2.9-xetex.patch

* Sun May 10 2009 Neal Becker <ndbecker2@gmail.com> - 0.2.10-1
- Update to 0.2.10

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.9-3
- Rebuild for Python 2.6

* Fri Jul  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.9-2
- BR: texlive-xetex -> tex(xetex) for F-10 and later

* Thu Jun 12 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.9-1
- Update to latest upstream (0.2.9) (#448953)
- Remove some redundant Requires and BuildRequires (passivetex pulls
  in the tetex/tex requires, python dep added automatically)
- For F-9+ BR on tex(latex) and texlive-xetex, fix the installation
  scripts to install extra new files.
- Add patch from dblatex mailing list for better handling of a missing
  xetex.
- Conditionally add .egg-info file only if F9+ to allow for unified
  spec file

* Sun Dec 16 2007 Patrice Dumas <pertusus@free.fr> - 0.2.8-2.1
- don't install in docbook directory, it is a link to a versioned
  directory and may break upon docbook update (#425251,#389231)

* Sun Nov 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.8-1
- Update to 0.2.8

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-16
- convert spec to utf8
- change to gplv2+

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-15
- Add copyright info

* Mon Nov  5 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-14
- Req tetex-fonts for texhash
- Fix post, postun

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-13
- Add texhash

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Fix xsl link

* Sat Nov  3 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Various fixes from pertusus@free.fr:
- rm iconv stuff
- simplify docs installation

* Fri Nov  2 2007  <ndbecker2@gmail.com> - 0.2.7-11
- Various minor fixes

* Thu Nov  1 2007  <ndbecker2@gmail.com> - 0.2.7-10
- Add some reqs and brs
- rmdir /usr/share/dblatex/latex/{misc,contrib/example,style}

* Sat Oct 27 2007  <ndbecker2@gmail.com> - 0.2.7-9
- link /usr/share/dblatex/xsl -> /usr/share/sgml/docbook/xsl-stylesheets/dblatex
- rmdir /usr/share/dblatex/latex/{misc,specs,style}
- own /etc/dblatex
- change $(...) -> `...`
- Preserve timestamps on iconv

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-9
- mv all .sty files to datadir/texmf/tex/latex/dblatex
- Add Conflicts tetex-tex4ht
- mv all xsl stuff to datadir/sgml/docbook/xsl-stylesheets/dblatex/

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- rm redundant latex files

* Tue Sep 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- Fixed encodings in docs directory
- Install docs at correct location

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-7
- Revert back to GPLv2
- untabify

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-6
- Fix source URL
- Install all docs
- Tabify

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-5
- Add BR tetex-latex

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-4
- Add  BR tetex, ImageMagick

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-3
- Add BR libxslt

* Wed Sep 19 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-2
- Add BR python-devel

* Fri Sep  7 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-1
- Initial
