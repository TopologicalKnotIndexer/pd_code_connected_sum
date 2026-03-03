# pd_code_connected_sum
caculate connected sum for link pd_code.

## Install

```bash
pip install pd-code-connected-sum
```

## Usage

```python
import pd_code_connected_sum

# L2a1
link_pd_code_1 = [[4, 1, 3, 2], [2, 3, 1, 4]]

# L4a1
link_pd_code_2 = [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]

connect_pos_1 = 1
connect_pos_2 = 1

print(pd_code_connected_sum.connected_sum(
    link_pd_code_1, link_pd_code_2, connect_pos_1, connect_pos_2))
```
