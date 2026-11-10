"""coastlines.py, the shared Natural Earth coastlines (sprint 057). Run by `just check`; no network."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coastlines  # noqa: E402


def feature(*rings):
    return {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [list(r) for r in rings]}}


class Land(unittest.TestCase):
    def test_a_region_is_its_rings_of_lon_lat_points(self):
        rings = coastlines.land('wallacea')
        self.assertEqual(len(rings), 24)
        self.assertEqual(rings[0][0], (122.78, -8.61))
        self.assertTrue(all(isinstance(p, tuple) for ring in rings for p in ring))

    def test_names_the_regions_it_has_when_asked_for_one_it_has_not(self):
        with self.assertRaises(KeyError) as e:
            coastlines.land('atlantis')
        self.assertIn('wallacea', str(e.exception))

    def test_projects_rings_to_a_plate(self):
        self.assertEqual(coastlines.project([[(110, -1), (111, -2)]], lambda lon: lon - 100, lambda lat: -lat),
                         [[(10, 1), (11, 2)]])


class Region(unittest.TestCase):
    """A region cut from Natural Earth's land: clipped to its box, simplified, rounded."""

    BOX = (0, 0, 10, 10)  # west, south, east, north

    def test_clips_to_the_box_and_drops_land_outside_it(self):
        geo = {'type': 'FeatureCollection', 'features': [
            feature([(5, 5), (15, 5), (15, 8), (5, 8), (5, 5)]),          # runs off the east edge
            feature([(20, 20), (21, 20), (21, 21), (20, 21), (20, 20)]),  # nowhere near
        ]}
        rings = coastlines.region(geo, self.BOX, tolerance=0.01)
        self.assertEqual(len(rings), 1)
        self.assertEqual(sorted(rings[0]), sorted([(5, 5), (10, 5), (10, 8), (5, 8)]))

    def test_simplifies_within_the_tolerance_and_rounds(self):
        jag = [(1, 1), (3, 1.01), (5, 1), (5, 5), (1, 5), (1, 1)]   # (3, 1.01) is within 0.04 of the line
        rings = coastlines.region({'features': [feature(jag)]}, self.BOX, tolerance=0.04)
        self.assertEqual(sorted(rings[0]), sorted([(1, 1), (5, 1), (5, 5), (1, 5)]))

    def test_leaves_out_an_island_smaller_than_the_tolerance(self):
        speck = [(2, 2), (2.01, 2), (2.01, 2.01), (2, 2)]
        self.assertEqual(coastlines.region({'features': [feature(speck)]}, self.BOX, tolerance=0.04), [])


if __name__ == '__main__':
    unittest.main()
