if __name__ == "__main__":
  # fix path for tests
  from common import *

  from megadata.svr_nng import *
  hook_quit()

  address = build_address(argv[1], argv[2] if argc>2 else None)

  #try_async(lambda:my_main_nng(address)) # ValueError: set_wakeup_fd only works in main thread
  try_asyncio(lambda:my_main_nng(address)) # OK using asyncio way
  #my_main_nng(address) 


  # NOTES: can override get_builtins here
  #try_async(lambda:start_stdin(get_builtins=get_builtins_default))
  start_stdin(get_builtins=get_builtins_default)

