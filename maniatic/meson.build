python = import('python')
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'maniatic')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'maniatic.in',
  output: 'maniatic',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('ui')

sources = [
  '__init__.py',
  'launcher.py',
  'setup_game.py',
]



install_data(sources, install_dir: moduledir)