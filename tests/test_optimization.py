import unittest
from sgdot.tools.grid_optimizer import GridOptimizer
from sgdot.grids import Grid
import sys
sys.path.append(".. /")


class TestOptimization(unittest.TestCase):

    def setUp(self):
        """ Code that runs before every test"""
        self.grid = Grid(_id='test_grid')
        self.grid.clear_nodes_and_links()

        self.opt = GridOptimizer(
            mst_algorithm_linking_hubs="Kruskal",
            sa_omega=0.2,
            sa_starting_temperature="auto",
            sa_ratio_temperatue_at_two_third_of_steps=1/20,
            sa_runtime=20,
            sa_flip_rep=1,
            sa_swap_rep=3,
            sa_swap_option='random',
            ga_number_of_generations=30,
            ga_population_size=20,
            ga_mutation_probability=0.2,
            ga_mutation_type_ratio=0.75,
            ga_number_of_elites=2,
            ga_number_of_survivors=1,
            ga_crossover_type="neighbor_pair",
            ga_number_of_processors_for_parallelization=8,
            ga_parent_selection="linear_rank_selection",
            ga_initialization_strategy="random",
            ga_delta=5,
            ga_max_runtime=20,
            fps=3
        )

    def tearDown(self):
        """ Code that runs before every test"""
        pass

    def test_connect_nodes_to_nereast_hubs(self):

        self.grid.add_node('0', 10, 20, 'household', False, '0')
        self.grid.add_node('1', 50, 67, 'household', False, '0')
        self.grid.add_node('2', 20, 90, 'meterhub', False, '0')
        self.grid.add_node('3', 82, 34, 'meterhub', False, '0')
        self.grid.add_node('4', 15, 70, 'powerhub', False, '0')

        self.opt.connect_household_to_nereast_hubs(self.grid)

        self.assertEqual(int(self.grid.get_links()['distance'][0]), 91)
        self.assertEqual(int(self.grid.get_links()['distance'][1]), 63)

        self.assertEqual(self.grid.get_links()['type'][0], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][1], 'distribution')

    def test_connect_nodes_to_capacitated_hubs(self):
        self.grid.add_node('0', 100, 100, 'meterhub', False, '0')
        self.grid.add_node('1', 90, 110, 'household', False, '0')
        self.grid.add_node('2', 90, 100, 'household', False, '0')
        self.grid.add_node('3', 90, 90, 'household', False, '0')
        self.grid.add_node('4', 110, 100, 'household', False, '0')
        self.grid.add_node('5', 200, 100, 'meterhub', False, '0')
        self.grid.add_node('6', 200, 110, 'household', False, '0')
        self.grid.add_node('7', 200, 90, 'household', False, '0')

        self.opt.connect_nodes(self.grid)

        self.assertEqual(int(self.grid.get_links()['distance'][0]), 18)
        self.assertEqual(int(self.grid.get_links()['distance'][1]), 25)
        self.assertEqual(int(self.grid.get_links()['distance'][2]), 25)
        self.assertEqual(int(self.grid.get_links()['distance'][3]), 163)
        self.assertEqual(int(self.grid.get_links()['distance'][4]), 18)
        self.assertEqual(int(self.grid.get_links()['distance'][5]), 18)
        self.assertEqual(int(self.grid.get_links()['distance'][6]), 182)

        self.assertEqual(self.grid.get_links()['type'][0], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][1], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][2], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][3], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][4], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][5], 'distribution')
        self.assertEqual(self.grid.get_links()['type'][6], 'interhub')

    def test_remove_last_node(self):
        self.grid.clear_nodes_and_links()
        self.grid.add_node('0', 50, 300, 'household', False, '0')
        self.grid.add_node('1', 250, 200, 'meterhub', False, '0')

        self.assertEqual(self.grid.get_nodes().shape[0], 2)
        self.opt.remove_last_node(self.grid)
        self.assertEqual(self.grid.get_nodes().shape[0], 1)
        self.assertEqual(self.grid.get_nodes().index[-1], '0')

    def test_segmented_minimum_spanning_tree_Kruskal(self):
        self.grid.add_node(label='0',
                           pixel_x_axis=90,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='1',
                           pixel_x_axis=95,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='2',
                           pixel_x_axis=100,
                           pixel_y_axis=90,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='3',
                           pixel_x_axis=100,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')
        self.grid.add_node(label='4',
                           pixel_x_axis=110,
                           pixel_y_axis=110,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')
        self.grid.add_node(label='3',
                           pixel_x_axis=120,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')

        self.opt.connect_hubs_using_MST_Kruskal(self.grid)

        self.assertIs(self.grid.does_link_exist('0', '1'), True)
        self.assertIs(self.grid.does_link_exist('1', '2'), True)
        self.assertIs(self.grid.does_link_exist('0', '2'), False)
        self.assertIs(self.grid.does_link_exist('3', '1'), False)

    def test_segmented_minimum_spanning_tree_Prims(self):
        self.grid.add_node(label='0',
                           pixel_x_axis=90,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='1',
                           pixel_x_axis=95,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='2',
                           pixel_x_axis=100,
                           pixel_y_axis=90,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='0')
        self.grid.add_node(label='3',
                           pixel_x_axis=100,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')
        self.grid.add_node(label='4',
                           pixel_x_axis=110,
                           pixel_y_axis=110,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')
        self.grid.add_node(label='3',
                           pixel_x_axis=120,
                           pixel_y_axis=100,
                           node_type='meterhub',
                           type_fixed=False,
                           segment='1')

        self.opt.connect_hubs_using_MST_Prims(self.grid)

        self.assertIs(self.grid.does_link_exist('0', '1'), True)
        self.assertIs(self.grid.does_link_exist('1', '2'), True)
        self.assertIs(self.grid.does_link_exist('0', '2'), False)
        self.assertIs(self.grid.does_link_exist('3', '1'), False)

    def test_k_mean_clustering(self):
        self.grid.add_node('0',
                           pixel_x_axis=100,
                           pixel_y_axis=100,
                           node_type='household',
                           type_fixed=False,
                           segment='0',
                           allocation_capacity=0)

        self.grid.add_node('1',
                           pixel_x_axis=200,
                           pixel_y_axis=100,
                           node_type='household',
                           type_fixed=False,
                           segment='0',
                           allocation_capacity=0)

        self.grid.add_node('2',
                           pixel_x_axis=100,
                           pixel_y_axis=250,
                           node_type='household',
                           type_fixed=False,
                           segment='0',
                           allocation_capacity=0)

        self.grid.add_node('3',
                           pixel_x_axis=200,
                           pixel_y_axis=250,
                           node_type='household',
                           type_fixed=False,
                           segment='0',
                           allocation_capacity=0)

        self.assertTrue(
            bool((opt.k_means_cluster_centers(self.grid, 1)
                  == [[150., 175.]]).all()))

        self.assertTrue(
            bool((opt.k_means_cluster_centers(self.grid, 2)
                  == [[150., 100.], [150., 250.]]).all()
                 or (opt.k_means_cluster_centers(self.grid, 2)
                     == [[150., 250.], [150., 100.]]).all()))


if __name__ == '__main__':
    unittest.main()
