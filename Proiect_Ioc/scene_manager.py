import threading

import numpy as np
import open3d as o3d

import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
from multiprocessing.connection import Listener

import psutil
import win32gui
import win32process


class SceneManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.window = gui.Application.instance.create_window("scene", self.width, self.height, 50, 50, True)
        w = self.window

        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(w.renderer)

        r = self.window.content_rect
        self.scene.frame = r
        w.add_child(self.scene)

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

    @staticmethod
    def close():
        gui.Application.instance.quit()


def initialize_listener(o3d_scene):
    print("Starting listening")
    address = ('localhost', 9998)
    listener = Listener(address, authkey=bytes('secret password', 'utf-8)'))
    conn = listener.accept()
    print('Connection accepted from ' + str(listener.last_accepted[0]) + ":" + str(listener.last_accepted[1]))
    while True:
        msg = conn.recv()
        if msg == 'close':
            conn.close()
            break
        elif msg.startswith('file'):
            _, path = msg.split(" ")
            o3d_scene.load(path)
        else:
            print(msg)
    print('Connection closed')
    listener.close()
    o3d_scene.close()
    print("aici")


if __name__ == "__main__":
    gui.Application.instance.initialize()

    scene = SceneManager(1600, 800)

    listener_thread = threading.Thread(target=initialize_listener, args=[scene])
    listener_thread.start()

    gui.Application.instance.run()
    print("exit")
