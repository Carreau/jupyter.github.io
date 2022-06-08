import nox
from pathlib import Path
from textwrap import dedent

nox.options.reuse_existing_virtualenvs = True

CONDA_DEPS = ["c-compiler", "compilers", "cxx-compiler", "ruby", "python=3.8"]

def install_deps(session):
    # Jekyll w/ Conda installation instructions roughly pulled from
    # https://s-canchi.github.io/2021-04-30-jekyll-conda/
    session.conda_install("--channel=conda-forge", *CONDA_DEPS)
    session.run(*"gem install jekyll bundler".split())
    session.run(*"bundle install".split())
    

@nox.session(name="build-live", venv_backend='conda')
def build_live(session):
    install_deps(session)
    session.run(*"bundle exec jekyll serve liveserve".split())

@nox.session(venv_backend='conda')
def build(session):
    install_deps(session)
    session.run(*"bundle exec jekyll build".split())

@nox.session(name="update-security-doc")
def update_security_doc(session):
    session.install("requests")

    import requests
    URL_SECURITY = "https://github.com/jupyter/security/raw/main/docs/vulnerability-handling.md"
    resp = requests.get(URL_SECURITY)
    includes = Path("_includes/security_protocol.md")
    text = dedent("""\
    <!--
      🛑🛑THIS IS A COPY, DO NOT PROPOSE CHANGES DO THIS FILE🛑🛑
      The text here is copied from the URL below:
      https://github.com/jupyter/security/raw/main/docs/vulnerability-handling.md

      If you wish to make updates to this text, propose those changes in the security repository.
      You may update the text below if it is copy-pasting updates from the security repo version.
    -->

    """)
    includes.write_text(text + resp.text)
