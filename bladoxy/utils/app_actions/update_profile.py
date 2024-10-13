from bladoxy.utils.kill_process import kill_possible_sslocal_processes
from bladoxy.utils.nodes import ssconfig_handler
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.start_process import start_sslocal
from bladoxy.utils.check_availability import check_availability


def update_profile():
    print("更新配置...")
    # 停止 sslocal 进程
    kill_possible_sslocal_processes()
    ssconfig_handler()
    configure_port(is_init=False, onlyss=True)
    start_sslocal()
    check_availability()
    print("成功更新配置。")


