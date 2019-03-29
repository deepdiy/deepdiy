from kivy.app import App



def load_demo():
    app=App.get_running_app()
    app.widget_manager.ids.processing_screens.current='open'
    app.widget_manager.ids.processing_screens.children[0].children[0].add_to_tree('D:\onedrive\program\worm_analyst\demo_img\elegans')
    print(app.widget_manager.ids.processing_screens.children[0].children[0])
