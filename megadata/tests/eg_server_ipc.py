from megadata.svr_ipc_bin import my_main_ipc,on_quit,start_stdin,build_address,hook_quit,on_quit_default
hook_quit(on_quit_default)
#my_main_ipc(build_address('wtf'))
my_main_ipc(build_address('wtf'),mode='asyncio')
