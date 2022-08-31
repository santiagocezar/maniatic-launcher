desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [files('io.github.santiagocezar.maniatic-launcher.desktop')]
  )
endif

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', files('io.github.santiagocezar.maniatic-launcher.appdata.xml')]
  )
endif

install_data(
    'io.github.santiagocezar.maniatic-launcher.svg',
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons/hicolor/scalable/apps')
)

install_data(
    'io.github.santiagocezar.maniatic-launcher.desktop',
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'applications')
)

install_data(
    'io.github.santiagocezar.maniatic-launcher.appdata.xml',
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'appdata')
)
