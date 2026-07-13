from copy import deepcopy
import unittest

import pd_code_sanity
from pd_code_connected_sum import connected_sum, normalize_pd_code


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


class ConnectedSumTests(unittest.TestCase):
    def test_two_trefoils_produce_six_crossings_and_complete_maps(self):
        left = deepcopy(TREFOIL)
        right = deepcopy(TREFOIL)
        result, mapping = connected_sum(left, right, 1, 1)
        self.assertEqual(len(result), 6)
        self.assertTrue(pd_code_sanity.sanity(result))
        self.assertEqual(set(mapping), {
            *(f"a_{label}" for label in range(1, 7)),
            *(f"b_{label}" for label in range(1, 7)),
        })
        self.assertEqual(left, TREFOIL)
        self.assertEqual(right, TREFOIL)

    def test_negative_sparse_labels_cannot_collide(self):
        labels = {-3: -30, -2: 90, -1: -10, 0: 70, 1: 20, 2: 50}
        relabeled = [[labels[value - 4] for value in crossing] for crossing in TREFOIL]
        result, mapping = connected_sum(relabeled, relabeled, -30, -30)
        self.assertEqual(len(result), 6)
        self.assertTrue(pd_code_sanity.sanity(result))
        self.assertEqual(len(mapping), 12)
        self.assertEqual(set(mapping.values()), set(range(1, 13)))

    def test_unknot_is_identity_and_normalization_does_not_mutate(self):
        source = deepcopy(TREFOIL)
        result, mapping = connected_sum([], source, 999, 1)
        normalized, expected_map = normalize_pd_code(source)
        self.assertEqual(result, normalized)
        self.assertEqual(mapping, {f"b_{old}": new for old, new in expected_map.items()})
        self.assertEqual(source, TREFOIL)

    def test_rejects_missing_selected_label(self):
        with self.assertRaisesRegex(ValueError, "val_1"):
            connected_sum(TREFOIL, TREFOIL, 999, 1)


if __name__ == "__main__":
    unittest.main()
