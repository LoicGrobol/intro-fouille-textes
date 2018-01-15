#!/usr/bin/env sh

# This script is used for testing using Travis
# It is intended to work on their VM set up: Ubuntu 12.04 LTS
# A minimal current TL is installed adding only the packages that are
# required

# See if there is a cached version of TL available
set -x

export PATH=/tmp/texlive/bin/x86_64-linux:$PATH
if ! command -v tlmgr > /dev/null; then
  # Obtain TeX Live
  wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
  tar -xzf install-tl-unx.tar.gz
  cd install-tl-20*

  # Install a minimal system
  ./install-tl --profile=../texlive.profile

  cd ..
fi

tlmgr init-usertree

# Needed for any use of texlua even if not testing LuaTeX
tlmgr install luatex

# Required to build plain and LaTeX formats:
# TeX90 plain for unpacking, pdfLaTeX, LuaLaTeX and XeTeX for tests
tlmgr install cm etex knuth-lib latex-bin tex tex-ini-files unicode-data xetex

# Additional requirements for (u)pLaTeX
tlmgr install babel ptex uptex ptex-base uptex-base ptex-fonts \
  uptex-fonts platex uplatex

# Assuming a 'basic' font set up, metafont is required to avoid
# warnings with some packages and errors with others
tlmgr install metafont mfware

# Set up graphics: nowadays split over a few places and requiring
# HO's bundle
tlmgr install graphics graphics-cfg graphics-def oberdiek

# Contrib packages for testing
#
# The packages themselves are done with --no-depends to avoid
# picking up l3kernel, etc.
#
# fontspec comes first as other packages tested have it as a dep
tlmgr install fontspec
tlmgr install ifluatex lm lualibs luaotfload ifxetex luatexbase ctablestack filehook


# Try to detect and install the packages used by the documents in the repository
# Plus some superpackages that are not (yet) automatically detected, packages
# whose texlive name doesn't match the file name and dependencies that tlmgr
# apparently doesn't know.
# A better solution might be to build the documents locally in a complete texlive
# install to get the list of the packages that are actually used and use that list
# to tell Travis what to install.
# Or Travis could, y'know, have an up-to-date texlive distribution using a ppa
# And Ubuntu maintainers could actually care.
# Eh, daydreaming, back to your programs.
tlmgr install texliveonfly
tlmgr install $(cat **/*.tex | sed -n 's/^[^%]*\\usepackage[^{]*{\([^}]*\)}.*$/\1/p' | sed 's/,\s*/ /p' | paste -sd ' ' -)

tlmgr install \
    amscls \
    amsfonts \
    amsmath \
    bbm-macros \
    beamer \
    biber \
    caption \
    carlisle \
    cm-super \
    etextools \
    etex-pkg \
    etoolbox \
    fira \
    doclicense \
    ec \
    fmtcount \
    hyph-utf8 \
    hyphen-english \
    hyphen-french \
    ifmtarg \
    latexmk \
    libertine \
    libertinus \
    logreq \
    metropolis \
    microtype \
    ms \
    pgf \
    shadethm \
    textpos \
    tools \
    titlesec \
    translator \
    ucharcat \
    url \
    varwidth \
    xits \
    xifthen \
    xkeyval \
    xstring \
    xunicode

# Keep no backups (not required, simply makes cache bigger)
tlmgr option -- autobackup 0

# Update the TL install but add nothing new
tlmgr update --self --all --no-auto-install
