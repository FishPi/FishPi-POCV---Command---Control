
#
# FishPi - An autonomous drop in the ocean
#
# View Controller for POCV MainView
#  - control logic split out from UI
#

import logging
import math
import os

from PIL import Image

# callback interval in milli seconds
callback_interval = 50

def run_main_view_wx(config):
    """ Runs main UI view based on wx framework. """
    # imports
    import wx
    import socket
    # might be some cross platform (windows) issues reported with wxReactor
    from twisted.internet import wxreactor
    # add twisted / wx interaction support
    wxreactor.install()
    # add logging observer
    from twisted.python.log import PythonLoggingObserver
    observer = PythonLoggingObserver()
    observer.start()

    # then can do normal reactor imports
    from twisted.internet import reactor
    # and wx specific implementations
    from ui.view_model_wx import MainViewController
    from ui.view_model_wx import MainViewModel
    from ui.main_view_wx import MainWindow

    # ip address *much* faster than by device name
    ipaddr = socket.gethostbyname(config.server_name)

    # create rpc client
    from web.webclient import RPCClient, RPCClientFactory
    rpc_client = RPCClient()
    
    # create view model
    view_model = MainViewModel()
    
    # create view controller
    controller = MainViewController(rpc_client, view_model, config)
    
    # create wxApp and main window
    wxApp = wx.App(False)
    frame = MainWindow(None, "fishpi - Proof Of Concept Vehicle control", controller, ipaddr, config.rpc_port, config.camera_port)
    frame.Show()
    
    # run reactor rather than usual 'wxApp.MainLoop()'
    rpc_factory = RPCClientFactory(frame)
    controller.set_rpc_factory(rpc_factory)
    reactor.registerWxApp(wxApp)
    logging.debug("RPC:\tconnecting to %s (%s) on port %s" % (config.server_name, ipaddr, config.rpc_port))
    reactor.connectTCP(ipaddr, config.rpc_port, rpc_factory)
    #reactor.callLater(5, update_callback)
    reactor.run()

def run_main_view_tk(kernel):
    """ Runs main UI view based on tk framework. """
    # imports
    import Tkinter
    
    from ui.view_model_tk import MainViewController
    from ui.view_model_tk import MainViewModel
    from ui.main_view_tk import MainView
    
    # initialise UI system
    root = Tkinter.Tk()
    root.title("fishpi - Proof Of Concept Vehicle control")
    root.minsize(800,600)
    root.maxsize(800,600)
    
    # create view model
    view_model = MainViewModel(root)
    
    # create view controller
    controller = MainViewController(kernel, view_model)
    
    # create view
    view = MainView(root, controller)

    # add callback to kernel for updates
    # longer delay on first callback to give UI time for initialisation
    root.after(5000, update_callback_tk, root, controller, view)

    # run ui loop
    root.mainloop()

def update_callback_tk(root, controller, view):
    """ Callback to perform updates etc. Needs to reregister callback at end. """
    # update kernel - note this will need revisiting for non-interactive modes...
    logging.debug("UI:\tIn update...")
    controller._kernel.set_capture_img_enabled(controller.model.capture_img_enabled.get())
    controller._kernel.update()
    # tell controller to update model (from kernel)
    controller.update()
    # annoyingly, images don't seem to bind so calling back to view to tell it to update image
    view.update_callback()
    # reregister callback
    root.after(callback_interval, update_callback_tk, root, controller, view)

