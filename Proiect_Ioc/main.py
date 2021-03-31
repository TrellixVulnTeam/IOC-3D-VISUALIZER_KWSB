import threading

import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import playsound

from lab2 import VideoTracking

is_loading = True


class AppWindow:
    MENU_OPEN = 1
    MENU_EXPORT = 2
    MENU_QUIT = 3
    MENU_SHOW_SETTINGS = 4
    MENU_ABOUT = 5

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.video_tracking = VideoTracking(self.width, self.height)

        self.window = gui.Application.instance.create_window("Aruco 3D App", width, height, 200,200)
        w = self.window

        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(w.renderer)

        em = w.theme.font_size
        self.settings_panel = gui.Vert(0, gui.Margins(0.25 * em, 0.25 * em, 0.25 * em, 0.25 * em))
        self.settings_panel.visible = False

        w.set_on_layout(self.on_layout)
        w.add_child(self.scene)
        w.add_child(self.settings_panel)

        # Menu

        if gui.Application.instance.menubar is None:
            file_menu = gui.Menu()
            file_menu.add_item("Open", AppWindow.MENU_OPEN)
            file_menu.add_separator()
            file_menu.add_item("Quit", AppWindow.MENU_QUIT)
            settings_menu = gui.Menu()
            settings_menu.add_item("Show webcam", AppWindow.MENU_SHOW_SETTINGS)
            settings_menu.set_checked(AppWindow.MENU_SHOW_SETTINGS, False)
            help_menu = gui.Menu()
            help_menu.add_item("About", AppWindow.MENU_ABOUT)

            menu = gui.Menu()
            menu.add_menu("File", file_menu)
            menu.add_menu("Settings", settings_menu)
            menu.add_menu("Help", help_menu)
            gui.Application.instance.menubar = menu

        w.set_on_menu_item_activated(AppWindow.MENU_OPEN, self.open_menu)
        w.set_on_menu_item_activated(AppWindow.MENU_QUIT, gui.Application.instance.quit)
        w.set_on_menu_item_activated(AppWindow.MENU_SHOW_SETTINGS, self._on_menu_toggle_settings_panel)
        w.set_on_menu_item_activated(AppWindow.MENU_ABOUT, self.menu_about)

    def on_layout(self, theme):
        r = self.window.content_rect
        self.scene.frame = r
        width = 17 * theme.font_size
        height = min(r.height, self.settings_panel.calc_preferred_size(theme).height)
        self.settings_panel.frame = gui.Rect(r.get_right() - width, r.y, width, height)

    def open_menu(self):
        playsound.playsound('sunete/primary/ui_tap-variant-03.wav')
        dlg = gui.FileDialog(gui.FileDialog.OPEN, "Choose file to load", self.window.theme)
        dlg.add_filter(
            ".ply .stl .fbx .obj .off .gltf .glb",
            "Triangle mesh files (.ply, .stl, .fbx, .obj, .off, "
            ".gltf, .glb)")
        dlg.add_filter(
            ".xyz .xyzn .xyzrgb .ply .pcd .pts",
            "Point cloud files (.xyz, .xyzn, .xyzrgb, .ply, "
            ".pcd, .pts)")
        dlg.add_filter("", "All files")

        dlg.set_on_cancel(self.cancel_dialog)
        dlg.set_on_done(self.finish_dialog)
        self.window.show_dialog(dlg)

    def cancel_dialog(self):
        self.window.close_dialog()

    def finish_dialog(self, filename):
        self.window.close_dialog()
        self.load(filename)

    def _on_menu_toggle_settings_panel(self):
        self.settings_panel.visible = not self.settings_panel.visible
        gui.Application.instance.menubar.set_checked(AppWindow.MENU_SHOW_SETTINGS, self.settings_panel.visible)

        if self.settings_panel.visible:
            self.open_camera()
        else:
            self.close_camera()

    def open_camera(self):
        playsound.playsound('sunete/primary/ui_tap-variant-03.wav')
        camera_thread = threading.Thread(target=self.video_tracking.video_stream)
        camera_thread.start()

    def close_camera(self):
        self.video_tracking.close = True
        pass

    def menu_about(self):
        playsound.playsound('sunete/primary/ui_tap-variant-03.wav')

        em = self.window.theme.font_size
        dlg = gui.Dialog("About")

        dlg_layout = gui.Vert(em, gui.Margins(em, em, em, em))
        dlg_layout.add_child(gui.Label("Aruco example program"))

        ok = gui.Button("OK")
        ok.set_on_clicked(self._on_about_ok)

        h = gui.Horiz()
        h.add_stretch()
        h.add_child(ok)
        h.add_stretch()
        dlg_layout.add_child(h)

        dlg.add_child(dlg_layout)
        self.window.show_dialog(dlg)

    def _on_about_ok(self):
        self.window.close_dialog()

    def load(self, path):
        self.scene.scene.clear_geometry()

        geometry = None
        geometry_type = o3d.io.read_file_geometry_type(path)

        mesh = None
        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            mesh = o3d.io.read_triangle_mesh(path)
        if mesh is not None:
            if len(mesh.triangles) == 0:
                mesh = None
            else:
                mesh.compute_vertex_normals()
                mesh.paint_uniform_color([0, 0, 0])
                geometry = mesh
            if not mesh.has_triangle_uvs():
                uv = np.array([[0.0, 0.0]] * (3 * len(mesh.triangles)))
                mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)
        else:
            print("[Info]", path, "appears to be a point cloud")

        if geometry is None:
            cloud = None
            try:
                cloud = o3d.io.read_point_cloud(path)
            except Exception:
                pass
            if cloud is not None:
                print("[Info] Successfully read", path)
                if not cloud.has_normals():
                    cloud.estimate_normals()
                cloud.normalize_normals()
                geometry = cloud
            else:
                print("[WARNING] Failed to read points", path)

        if geometry is not None:
            try:
                material = rendering.Material()
                material.shader = "normals"
                self.scene.scene.add_geometry("__model__", geometry, material)
                bounds = geometry.get_axis_aligned_bounding_box()
                self.scene.setup_camera(60, bounds, bounds.get_center())
            except Exception as e:
                print(e)


def main():
    gui.Application.instance.initialize()

    w = AppWindow(1600, 800)
    global is_loading

    is_loading = False

    gui.Application.instance.run()

    playsound.playsound('sunete/primary/ui_lock.wav')


def loading_sound():
    global is_loading
    while is_loading:
        playsound.playsound('sunete/secondary/ui_loading.wav')


if __name__ == "__main__":
    thread = threading.Thread(target=loading_sound)
    thread.start()
    main()
