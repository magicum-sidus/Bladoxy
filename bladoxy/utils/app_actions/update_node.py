from bladoxy.utils.kill_process import kill_possible_sslocal_processes
from bladoxy.utils.nodes import change_node
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.start_process import start_sslocal
from bladoxy.utils.check_availability import check_availability


def update_node():
    # 停止 sslocal 进程
    kill_possible_sslocal_processes()
    change_node()
    configure_port(is_init=False, onlyss=True)
    start_sslocal()
    check_availability()



    
