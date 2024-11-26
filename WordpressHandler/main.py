import wphandler
import os
import atexit
from time import perf_counter
from wpapi import get_plugins

def begin_wp_thread():
    wphandler.wsl("daemonize /usr/bin/syncthing serve $OPTS")
    def terminate_wp_instance():
        os.system("wsl --shutdown")
    atexit.register(terminate_wp_instance)

if __name__ == "__main__":
    que = []
    last_installed = None
    def on_exit():
        os.system("wsl --unregister Debian")

    atexit.register(on_exit)
    wphandler.start_wp_instance()
    begin_wp_thread()
    while True:
        user_input = input(">")
        split_input = user_input.split(" ")
        match split_input[0]:
            case "exit":
                exit()
            case "restore":
                wphandler.restore_wp_backup()
                begin_wp_thread()
            case "install":
                if split_input[1]:
                    wphandler.install_plugin(split_input[1])
                else:
                    print("Please supply a slug.")
            case "plugins":
                for plugin in que:
                    print(plugin)
                print(f"{str(len(que))} plugins currently in que.")
            case "query":
                start = perf_counter()
                name, description, slug, active_installs = "", "", "", 0
                for inp in split_input:
                    param = inp.split("=")
                    match param[0]:
                        case "query":
                            continue
                        case "name":
                            name = param[1]
                        case "desc":
                            description = param[1]
                        case "slug":
                            slug = param[1]
                        case "installs":
                            if param[1].isnumeric():
                                active_installs = param[1]
                            else:
                                print("WARNING: 'installs' parameter MUST be numeric. Defaulting to disregard install count.")
                        case _:
                            print(f"Parameter '{param[0]}' not recognized. Ignoring...")
                que = get_plugins(name=name, description=description, slug=slug, install_count=active_installs)
                stop = perf_counter() - start
                print(f"{str(len(que))} plugin(s) found and queued in f{str(stop)}s")
            case "next":
                wphandler.install_plugin(que[0])
                if last_installed:
                    wphandler.uninstall_plugin(last_installed)
                last_installed = que[0]
                que.pop(0)

