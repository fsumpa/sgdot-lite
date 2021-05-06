import sys
import unittest
sys.path.append('../sgdot/')
from sgdot.grids import Grid          # noqa: E402


class TestGrid(unittest.TestCase):

    def setUp(self):
        """ Code that runs before every test"""
        self.grid = Grid(_id='test_grid')
        self.grid.clear_nodes_and_links()

    def tearDown(self):
        """ Code that runs before every test"""
        pass

    def test_add_nodes(self):
        self.assertEqual(self.grid.get_nodes().shape[0], False, 0)
        self.grid.add_node('0', 100, 200, 'household', False, '0', 0)
        self.assertEqual(self.grid.get_nodes().shape[0], 1)
        self.grid.add_node('1', 50, 110, 'meterhub', False, '0', 0)
        self.assertEqual(self.grid.get_nodes().shape[0], 2)

    def test_add_link(self):
        self.grid.add_node('0', 50, 300, 'household', False, '0', 0)
        self.grid.add_node('1', 250, 200, 'meterhub', False, '0', 0)
        self.grid.add_node('2', 100, 110, 'household', False, '0', 0)

        self.assertEqual(self.grid.get_links().shape[0], 0)

        self.grid.add_link('0', '1')
        self.assertEqual(self.grid.get_links().shape[0], 1)
        self.grid.add_link('0', '2')
        self.assertEqual(self.grid.get_links().shape[0], 2)

        self.assertIs(self.grid.does_link_exist('0', '1'), True)
        self.assertIs(self.grid.does_link_exist('0', '2'), True)
        self.assertIs(self.grid.does_link_exist('1', '2'), False)

    def test_distance_between_nodes(self):
        self.grid.add_node('0', 50, 300, 'household', False, '0', 0)
        self.grid.add_node('1', 250, 200, 'meterhub', False, '0', 0)
        self.grid.add_node('2', 100, 110, 'household', False, '0', 0)

        self.assertEqual(
            self.grid.distance_between_nodes('0', '1'),
            407.2928338677583
        )
        self.assertEqual(
            self.grid.distance_between_nodes('0', '2'),
            357.8618634968843
        )

    def test_get_cable_distance_from_households_to_powerhub(self):
        self.grid.add_node('0', 1000, 1000, 'powerhub', False, '0', 0)
        self.grid.add_node('1', 1000, 1200, 'meterhub', False, '0', 0)
        self.grid.add_node('2', 1100, 1000, 'household', False, '0', 0)
        self.grid.add_node('3', 1100, 1200, 'household', False, '0', 0)

        self.grid.add_link('0', '1')
        self.grid.add_link('0', '2')
        self.grid.add_link('1', '3')

        distance_df =\
            self.grid.get_cable_distance_from_households_to_powerhub()

        self.assertEqual(int(distance_df['interhub cable [m]']['0']), 0)
        self.assertEqual(int(distance_df['distribution cable [m]']['0']), 0)

        self.assertEqual(int(distance_df['interhub cable [m]']['1']), 364)
        self.assertEqual(int(distance_df['distribution cable [m]']['1']), 0)

        self.assertEqual(int(distance_df['interhub cable [m]']['2']), 0)
        self.assertEqual(int(distance_df['distribution cable [m]']['2']), 182)

        self.assertEqual(int(distance_df['interhub cable [m]']['3']), 364)
        self.assertEqual(int(distance_df['distribution cable [m]']['3']), 182)

    def test_compute_voltage_drop_at_each_nodes(self):
        self.grid.add_node('0', 1000, 1000, 'powerhub', False,  '0', 0)
        self.grid.add_node('1', 1000, 1200, 'meterhub', False, '0', 0)
        self.grid.add_node('2', 1100, 1000, 'household', False, '0', 0)
        self.grid.add_node('3', 1100, 1200, 'household', False, '0', 0)

        self.grid.add_link('0', '1')
        self.grid.add_link('0', '2')
        self.grid.add_link('1', '3')

        voltage_drop_df =\
            self.grid.get_voltage_drop_at_nodes()

        self.assertEqual(int(voltage_drop_df['voltage drop [V]']['0']), 0)

        self.assertEqual(voltage_drop_df['voltage drop [V]']['1'],
                         3.1147118644067797)

        self.assertEqual(voltage_drop_df['voltage drop [V]']['2'],
                         2.4917694915254236)

        self.assertEqual(voltage_drop_df['voltage drop [V]']['3'],
                         5.606481355932203)

    def test_flip_node(self):
        self.grid.add_node('0', 10, 20, 'household', False,  '0', 0)
        self.assertEqual(self.grid.get_nodes()['node_type'][0], 'household')
        self.grid.flip_node('0')
        self.assertEqual(self.grid.get_nodes()['node_type'][0], 'meterhub')

        self.grid.add_node('1', 10, 20, 'powerhub', False,  '0', 0)
        self.assertEqual(self.grid.get_nodes()['node_type'][1], 'powerhub')
        self.grid.flip_node('0')
        self.assertEqual(self.grid.get_nodes()['node_type'][1], 'powerhub')

    def test_set_all_node_types(self):
        self.grid.add_node('0', 10, 20, 'household', False, '0', 0)
        self.grid.add_node('1', 20, 90, 'meterhub', False, '0', 0)
        self.grid.add_node('2', 15, 70, 'powerhub', False, '0', 0)
        self.grid.set_all_node_type_to_households()

        for i in range(2):
            self.assertEqual(self.grid.get_nodes()['node_type'][i],
                             'household')
        self.assertEqual(self.grid.get_nodes()['node_type'][2],
                         'powerhub')
        self.grid.set_all_node_type_to_meterhubs()
        for i in range(2):
            self.assertEqual(self.grid.get_nodes()['node_type'][i],
                             'meterhub')
        self.assertEqual(self.grid.get_nodes()['node_type'][2],
                         'powerhub')

    def test_clear_links(self):
        self.grid.add_node('0', 10, 20, 'household', False, 0)
        self.grid.add_node('1', 50, 67, 'household', False, 0)

        self.grid.clear_links()

        self.assertEqual(self.grid.get_links().shape[0], 0)

    def test_price(self):
        self.grid.add_node('0', 10, 20, 'household', False, 0)
        self.grid.add_node('1', 50, 67, 'household', False, 0)
        self.grid.add_node('2', 20, 90, 'meterhub', False, 0)
        self.grid.add_node('3', 82, 34, 'meterhub', False, 0)
        self.grid.add_node('4', 15, 70, 'powerhub', False, 0)

        self.assertEqual(self.grid.price(), 2500)


if __name__ == '__main__':
    unittest.main()
