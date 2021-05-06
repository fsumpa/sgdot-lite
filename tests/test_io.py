import os
import unittest
import shutil
import pandas as pd
import sys
sys.path.append('../sgdot/')
import tools.io as io           # noqa: E402
from grids import Grid          # noqa: E402


class TestIo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists('data/backup'):
            shutil.rmtree('data/backup')

    @classmethod
    def tearDown(cls):
        if os.path.exists('data'):
            shutil.rmtree('data')

    def setUp(self):
        """ Code that runs before every test"""
        self.grid = Grid(_id='test_grid')

    def test_make_folder(self):
        folder_test_export = 'unittest_folder_export'
        io.make_folder(folder_test_export)
        self.assertTrue(os.path.exists(folder_test_export))
        self.assertTrue(os.path.exists(folder_test_export))
        os.removedirs(folder_test_export)

    def test_export_grid_default_path(self):
        io.export_grid(self.grid)
        self.assertTrue(
            os.path.exists('data/backup/test_grid/backup_test_grid'))
        self.assertEqual(
            len(os.listdir('data/backup/test_grid/backup_test_grid')), 6)

        shutil.rmtree('data/backup')

    def test_export_grid_specified_path(self):
        path_to_folder = 'test_Backup'
        folder_name = 'test_folder_name'
        io.export_grid(
            self.grid,
            folder=path_to_folder,
            backup_name=folder_name)
        self.assertTrue(os.path.exists(path_to_folder + '/' + folder_name))
        shutil.rmtree(path_to_folder)

    def test_export_grid_save_images(self):
        io.export_grid(self.grid)
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/Grid_test_grid.png'
                )
            )
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/initial_image.png'
                )
            )
        shutil.rmtree('data/backup')

    def test_export_grid_save_nodes_and_links(self):
        io.export_grid(self.grid)
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/nodes.csv'
                )
            )
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/links.csv'
                )
            )
        shutil.rmtree('data/backup')

    def test_export_grid_save_config_files(self):
        io.export_grid(self.grid)
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/config_cv2.cfg'
                )
            )
        self.assertTrue(
            os.path.exists(
                'data/backup/test_grid/backup_test_grid/config_grid.cfg'
                )
            )
        shutil.rmtree('data/backup')

    def test_import_grid(self):
        self.grid.add_node(label='0',
                           pixel_x_axis=100,
                           pixel_y_axis=200,
                           node_type='household',
                           type_fixed=False,
                           segment='0')

        self.grid.add_node(label='1',
                           pixel_x_axis=50,
                           pixel_y_axis=150,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.clear_links()
        self.grid.add_link('0', '1')

        io.export_grid(self.grid)
        g_imported =\
            io.import_grid('data/backup/test_grid/backup_test_grid')


        #self.assertIsNone(pd.testing.assert_frame_equal(
        #    self.grid.get_links(),
        #    g_imported.get_links()))
        #self.assertIsNone(pd.testing.assert_frame_equal(
        #    self.grid.get_nodes(),
        #    g_imported.get_nodes()))

        self.assertTrue(self.grid.get_links().equals(g_imported.get_links()))

        #self.assertTrue(self.grid.get_nodes().equals(g_imported.get_nodes()))

        self.assertEqual(g_imported.get_id(), self.grid.get_id())


if __name__ == '__main__':
    unittest.main()
