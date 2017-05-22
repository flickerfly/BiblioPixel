import json, os, sys
from . import defaults
from . importer import make_object
from .. animation import runner
from .. import data_maker
from .. layout import gen_matrix
from .. led.multimap import MultiMapBuilder
from .. util import opener


def make_led(driver, led, maker=None):
    maker = data_maker.Maker(**(maker or {}))
    drivers = []

    def multi_drivers(device_ids, width, height, serpentine=False, **kwds):
        build = MultiMapBuilder()

        for id in device_ids:
            build.addRow(gen_matrix(width, height, serpentine=serpentine))
            d = make_object(width=width, height=height, deviceID=id, **kwds)
            drivers.append(d)

        return build.map

    def make_drivers(multimap=False, **kwds):
        if multimap:
            return multi_drivers(**kwds)

        drivers.append(make_object(**kwds))

    coordMap = make_drivers(maker=maker, **driver)
    return make_object(drivers, coordMap=coordMap, maker=maker, **led)


def make_animation(led, animation, run=None):
    animation = make_object(led, **animation)
    animation.set_runner(runner.Runner(**(run or {})))
    return animation


def project_to_animation(*, path=None, **project):
    if path:
        try:
            path = path.split(':')
        except:
            pass
        sys.path.extend(path)

    kwds = defaults.apply_defaults(project)
    animation = kwds.pop('animation', {})
    run = kwds.pop('run', {})
    led = make_led(**kwds)
    return make_animation(led, animation, run)


def project_to_runnable(project):
    return project_to_animation(**project).start


def run(s):
    try:
        project = json.load(opener.opener(s))
    except:
        project = json.loads(s)

    runnable = project_to_runnable(project)
    runnable()


if __name__ == '__main__':
    run(*sys.argv[1:])