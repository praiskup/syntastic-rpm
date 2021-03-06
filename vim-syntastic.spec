%global         vimfiles        %{_datadir}/vim/vimfiles
%global         upstream_name   syntastic

%global         appdata_dir %{_datadir}/appdata

Name:           vim-%{upstream_name}
Version:        3.7.0
Release:        6%{?dist}
Summary:        A vim plugins to check syntax for programming languages
Summary(fr):    Une extension de vim vérifiant la syntaxe pour les langages de programmation

License:        WTFPL
URL:            https://github.com/scrooloose/syntastic
Source0:        https://github.com/scrooloose/syntastic/archive/%{version}.tar.gz
Source1:        vim-syntastic.metainfo.xml

BuildArch:      noarch
Requires:       vim
BuildRequires:  glibc-common
# Needed for AppData check.
BuildRequires:  libappstream-glib
# Rename from 'syntastic'
Provides:       %upstream_name = %version-%release
Obsoletes:      %upstream_name < 3.7.0-6


%description
Syntastic is a syntax checking plugin that runs files through external syntax
checkers and displays any resulting errors to the user. This can be done on
demand, or automatically as files are saved. If syntax errors are detected, the
user is notified and is happy because they didn't have to compile their code or
execute their script to find them.

%description -l fr
Syntastic est une extension vérifiant la syntaxe des fichiers source, un outil
externe de vérification affiche toutes les erreurs trouvées à l'utilisateur.
Ceci peut être fait à la demande ou automatique au moment de la sauvegarde
du fichier. Si une erreur de syntaxe est détecté, les utilisateurs sont
informés et sont heureux de ne pas avoir compiler leur code ou d'avoir
exécuter leur script afin de les trouver.


%define add_subpackage(n:)                                                          \
%package %{-n*}                                                                     \
Summary:        A syntax checker for %{-n*} programming language                    \
Summary(fr):    Un vérificateur de syntaxe pour le langage de programmation %{-n*}  \
Requires:       %{name} =  %{version}-%{release}                                    \
Requires:       %*                                                                  \
Provides:       %upstream_name-%{-n*} = %version-%release                           \
Obsoletes:      %upstream_name-%{-n*} < 3.7.0-6                                     \
%description %{-n*}                                                                 \
Allows checking %{-n*} sources files.                                               \
%description -l fr %{-n*}                                                           \
Permet de vérifier les fichiers sources écrit en %{-n*}.                            \
%global files_to_do %{?files_to_do}                                               \\\
%files_for_lang %{-n*}                                                            \\\
%{expand:%%{?additional_files_for_lang_%{-n*}}}


# Initialize files_to_do macro here to empty string.  FedoraReview tool, for
# example, runs 'rpm.TransactionSet().parseSpec("syntastic.spec")' _twice_,
# while global macros survive from the first call (we don't want to have all
# %%files sections generated twice).
%global files_to_do %nil
%add_subpackage -n ada gcc-gnat
%add_subpackage -n asciidoc asciidoc
%add_subpackage -n asm nasm
%global additional_files_for_lang_c \
%{vimfiles}/autoload/syntastic/c.vim
%add_subpackage -n c gcc
%add_subpackage -n cabal cabal-install
%add_subpackage -n coffee coffee-script
%add_subpackage -n coq coq
%add_subpackage -n cpp gcc-c++
%add_subpackage -n cs mono-core
%add_subpackage -n css csslint
%add_subpackage -n cucumber rubygem-cucumber
%add_subpackage -n d ldc
%add_subpackage -n docbk /usr/bin/xmllint
%add_subpackage -n elixir elixir
%add_subpackage -n erlang erlang-erts
%add_subpackage -n eruby ruby
%add_subpackage -n fortran gcc-gfortran
%add_subpackage -n glsl mesa-libGLU
%add_subpackage -n go gcc-go
%add_subpackage -n haml rubygem-haml
%add_subpackage -n haskell ghc
%add_subpackage -n html sed curl tidy
%add_subpackage -n java java-devel
%add_subpackage -n javascript jsl
%add_subpackage -n json python-demjson
%add_subpackage -n less nodejs
%add_subpackage -n lex flex
%add_subpackage -n lisp clisp
%add_subpackage -n llvm llvm
%add_subpackage -n lua lua
%add_subpackage -n matlab octave
%add_subpackage -n nasm nasm
%add_subpackage -n objc gcc-objc
%add_subpackage -n objcpp gcc-objc++
%add_subpackage -n ocaml ocaml
%add_subpackage -n perl perl %name-pod
%add_subpackage -n php php
%add_subpackage -n po gettext
%add_subpackage -n pod perl
%add_subpackage -n puppet puppet
%add_subpackage -n python pylint pyflakes
%add_subpackage -n qml /usr/bin/qmllint
%add_subpackage -n rnc rnv
%add_subpackage -n rst python-docutils
%add_subpackage -n ruby ruby
%add_subpackage -n sass rubygem-sass
%add_subpackage -n scala scala
%add_subpackage -n scss rubygem-sass
%add_subpackage -n sh bash
%add_subpackage -n spec rpmlint
%add_subpackage -n tcl tcl
%add_subpackage -n tex texlive-latex
%add_subpackage -n texinfo texinfo
%add_subpackage -n vala vala
%add_subpackage -n verilog iverilog
%add_subpackage -n vhdl freehdl
%add_subpackage -n vim vim
%add_subpackage -n xhtml tidy
%add_subpackage -n xml /usr/bin/xmllint
%add_subpackage -n xslt /usr/bin/xmllint
%add_subpackage -n yacc byacc
%add_subpackage -n yaml nodejs-js-yaml perl-YAML-LibYAML
%add_subpackage -n z80 z80asm
%add_subpackage -n zsh zsh


# Intentional %%define here, intentionally after %%add_subpackage usage.
%define files_for_lang() \
%files %1 \
%license LICENCE \
%{vimfiles}/syntax_checkers/%1


%prep
%setup -q -n %upstream_name-%version
# Use a free D compiler ldc
sed -i "s/dmd/ldc2/g" syntax_checkers/d/dmd.vim
# Use executable script from bindir
sed -i "s|expand\(.*sfile.*\).*|'%{_bindir}/erlang_check_file.erl'|" syntax_checkers/erlang/escript.vim

# Don't use /bin/env like shebangs.
grep -lr '#!.*/bin/env'  | while read file; do
    sed -i '1 s|#!.*/bin/env \(.*\)|#!/usr/bin/\1|' "$file"
done

rm -r syntax_checkers/actionscript
rm -r syntax_checkers/applescript
rm -r syntax_checkers/apiblueprint
rm -r syntax_checkers/bemhtml
rm -r syntax_checkers/bro
rm -r syntax_checkers/chef
rm -r syntax_checkers/co
rm -r syntax_checkers/cobol
rm -r syntax_checkers/cuda
rm -r syntax_checkers/dart
rm -r syntax_checkers/dustjs
rm -r syntax_checkers/handlebars
rm -r syntax_checkers/haxe
rm -r syntax_checkers/hss
rm -r syntax_checkers/jade
rm -r syntax_checkers/limbo
rm -r syntax_checkers/markdown
rm -r syntax_checkers/mercury
rm -r syntax_checkers/nix
rm -r syntax_checkers/nroff
rm -r syntax_checkers/r
rm -r syntax_checkers/racket
rm -r syntax_checkers/slim
rm -r syntax_checkers/sml
rm -r syntax_checkers/sql
rm -r syntax_checkers/stylus
rm -r syntax_checkers/text
rm -r syntax_checkers/twig
rm -r syntax_checkers/typescript
rm -r syntax_checkers/zpt

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{vimfiles}/autoload
mkdir -p %{buildroot}%{vimfiles}/doc

cp      -rp       autoload/*                            %{buildroot}%{vimfiles}/autoload/
install -p -m0644 doc/syntastic.txt                     %{buildroot}%{vimfiles}/doc/syntastic.txt
cp      -rp       plugin/                               %{buildroot}%{vimfiles}/plugin
cp      -rp       syntax_checkers/                      %{buildroot}%{vimfiles}/syntax_checkers

# not install -ped :
# applescript.vim    -> mac os
# coffe.vim          -> no coffe executable in repo
# cuda.vim           -> no nvcss executable in repo
# go.vim and go dir  -> no go executable in repo
# haskell.vim        -> no ghc-mod executable in repo
# haxe.vim           -> no haxe executable in repo
# less.vim           -> no lessc executable in repo
# matlab.vim         -> no mlint executable in repo
# z80.vim            -> no 80_syntax_checker.pyt executable in repo
# zpt.vim            -> no zptlint executable in repo

# Install AppData.
mkdir -p %{buildroot}%{appdata_dir}
install -m 644 %{SOURCE1} %{buildroot}%{appdata_dir}


%check
# Check the AppData add-on to comply with guidelines.
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.metainfo.xml


%post
umask 022
cd %{vimfiles}/doc
vim -u NONE -esX -c "helptags ." -c quit
exit 0


%postun
if [ $1 -eq 0 ]; then
umask 022
cd %{vimfiles}/doc
>tags
vim -u NONE -esX -c "helptags ." -c quit
fi
exit 0

%files
%license LICENCE
%doc _assets/screenshot_1.png README.markdown
%{vimfiles}/plugin/syntastic.vim
%{vimfiles}/plugin/syntastic
%{vimfiles}/doc/syntastic.txt
%dir %{vimfiles}/syntax_checkers/
%dir %{vimfiles}/autoload/syntastic/
%{vimfiles}/autoload/syntastic/log.vim
%{vimfiles}/autoload/syntastic/postprocess.vim
%{vimfiles}/autoload/syntastic/preprocess.vim
%{vimfiles}/autoload/syntastic//util.vim
%{appdata_dir}/vim-syntastic.metainfo.xml


%files_to_do


%changelog
* Sun Sep 18 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-6
- don't use obsoletes < NVR

* Fri Sep 16 2016 Vít Ondruch <vondruch@redhat.com> - 3.7.0-5
- add AppData support

* Fri Sep 16 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-5
- rename to vim-syntastic

* Wed Sep 14 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-3
- add license to all subpackages
- condense the spec file a bit more
- remove cobol subpackage (open-cobol orphaned in F25+)

* Thu Sep 08 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-1
- unretirement, rebase to 3.7.0 (rhbz#1374138)

* Mon Sep 08 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 3.5.0-1
- Upstream 3.5.0 (RHBZ #1074998, RHBZ #1135416)
- Fix BR to java-devel (RHBZ #1113308)
- Add R: syntastic-pod to syntastic-perl (RHBZ #1109519)
- Fix R: rubygem-sass for scss subpackage as scss is provided by rubygem-sass

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 3.4.0-18
- Update to rev 3.4.0

* Mon Mar 10 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 3.3.0-17.20140309gitda6520c
- Version 3.3.0

* Sun Mar 09 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2.3.0-16.20140309gitda6520c
- Update to latest rev

* Thu Oct 24 2013 Jonathan MERCIER <bioinfornatics@gmail.com> - 2.3.0-15.20131023gitd238665
- Update to rev d238665

* Sat Aug 10 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-14.20130809git48208d4
- Update to rev 48208d4

* Mon Aug 05 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-13.20130805gita4fa323
- Update to rev a4fa323

* Sun Aug 04 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-12.20130731gite380a86
- Update to rev e380a86

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-11.20120917git72856e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3.0-10.20120917git72856e6
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-9.20120917git72856e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 03 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-8.20120917git72856e6
- fix spec

* Thu Sep 27 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-7.20120917git72856e6
- fix spec file

* Wed Sep 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-6.20120917git72856e6
- fix spec file

* Wed Sep 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-5.20120917git72856e6
- put  inautoload/syntastic/c.vimto c subpackage

* Mon Sep 17 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-4.20120917git72856e6
- Update to latest rev

* Thu Aug 23 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-3.20120802gite5dfcc3
- fix License
- remove unused macro
- Fix dependecies

* Mon Jun 18 2012  Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-2.20120617git1e94b98
- Update spec file

* Sun Jun 17 2012  Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-1.20120617git1e94b98
- initial release
