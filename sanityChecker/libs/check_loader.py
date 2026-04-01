# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import os
import importlib

from sanityChecker.resources.logger import sanity_stream_logger

log = sanity_stream_logger('SanityChecker')

CHECKS_IMPORT_PATH = 'sanityChecker.maya_checks.'
CHECKS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'maya_checks')


def check_loader() -> list:
    """Collect checks dynamically from checks folder."""
    checks = []
    for check_py_file in sorted(os.listdir(CHECKS_PATH)):
        if check_py_file.startswith('_'):
            continue

        check_name, ext = os.path.splitext(check_py_file)
        if ext != '.py':
            continue
        import_string = CHECKS_IMPORT_PATH + check_name
        try:
            module = importlib.import_module(import_string)
            class_instance = getattr(module, 'Check')()
            checks.append(class_instance)
        except ImportError as e:
            log.warning(f'Missing Check {import_string} {e}')
            continue
        except AttributeError as e:
            log.warning(f'Invalid Check module {import_string} {e}')
            continue
        except Exception as e:
            log.warning(f'Failed loading Check {import_string} {e}')
            continue

    return checks


if __name__ == '__main__':
    cl = check_loader()
