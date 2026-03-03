import pd_code_sanity
import pd_code_pre_nxt
import json

# 为编码增加前缀
def add_prefix(pd_code:list[list], prefix:str) -> list[list]:
    pd_code = json.loads(json.dumps(pd_code))
    for i in range(len(pd_code)):
        for j in range(len(pd_code[i])):
            pd_code[i][j] = prefix + str(pd_code[i][j])
    return json.loads(json.dumps(pd_code))

# 替换一个值恰好一次
def replace_val(crossing:list, val_now:str, val_new:str):
    cnt = 0
    for i in range(len(crossing)):
        if crossing[i] == val_now:
            crossing[i] = val_new
            cnt += 1
    if cnt != 1:
        raise ValueError()

# 检查一个 crossing 是否包含某个值
def check_has(crossing:list, val_now:str) -> bool:
    for i in range(len(crossing)):
        if crossing[i] == val_now:
            return True
    return False

# 检查两个元素同时存在
def check_has2(crossing:list, val1:str, val2:str) -> bool:
    return (
        check_has(crossing, val1) and 
        check_has(crossing, val2))

get_num_set = pd_code_pre_nxt.get_num_set

# 按照顺序对循环进行遍历
def dfs(val, nxt:dict[str, str], vis: set[int], idx:dict[str, int]):
    if val in vis:
        return
    assert nxt.get(val) is not None

    # 向已经访问元素队列中添加该节点
    vis.add(val)
    idx[val] = len(vis) # 当前元素个数，就是当前节点新编号

    if nxt[val] not in vis:
        dfs(nxt[val], nxt, vis, idx)
    
# 在有向图中重新编号
def get_new_number_map(nxt:dict[str, str], num_set:list[int]) -> dict[str, int]:
    vis = set()
    idx = dict()
    for val in num_set:
        if val not in vis:
            dfs(val, nxt, vis, idx)
    return idx

# 检查有多少个 crossing 包含了 val_now
def count_crossing_exists(pd_code_now:list[list], val_now) -> int:
    ans = 0
    for crossing in pd_code_now:
        if check_has(crossing, val_now):
            ans += 1
    return ans

# 找到同一个连通分量中合法的位置
def find_avaible_pos(pd_code:list[list], val_now):
    for crossing in pd_code:
        if check_has(crossing, val_now):
            values = []
            for i in range(len(crossing)):
                if crossing[i] != val_now and crossing[i] not in values:
                    values.append(crossing[i])
            if len(values) == 1:
                return None
            else:
                return values[0]
    
    # 在这里报错说明 pd_code 中没找到 val_now
    raise AssertionError()

# 删除 pd_code1 中 val_1 所在的 crossing
# 然后把两个扭结直接合并
# 然后重新编号
def del_component_and_merge(pd_code1, pd_code2, val_1, val_2) -> list[list]:
    suc = False
    for i in range(len(pd_code1)):
        if check_has(pd_code1[i], val_1):
            suc = True
            pd_code1 = pd_code1[:i] + pd_code1[i+1:] # 跳过第 i 个元素
    
    # 这里报错说明没找到 val_1 对应的 component
    if not suc:
        raise AssertionError()
    
    # 获取元素集合
    num_set_1 = add_prefix([get_num_set(pd_code1)], "a_")[0]
    num_set_2 = add_prefix([get_num_set(pd_code2)], "b_")[0]

    # 增加前缀编码
    pd_code1 = add_prefix(pd_code1, "a_")
    pd_code2 = add_prefix(pd_code2, "b_")

    # 计算前驱后继
    _, nxt1 = pd_code_pre_nxt.get_pre_nxt(pd_code1)
    _, nxt2 = pd_code_pre_nxt.get_pre_nxt(pd_code2)
    nxt = nxt1 | nxt2

    # 合并得到新的 pd_code
    new_pd_code = json.loads(json.dumps(pd_code1 + pd_code2))

    # 获得新的编号方式
    num_map = get_new_number_map(nxt, num_set_1 + num_set_2)
    for crossing in new_pd_code:
        for i in range(len(crossing)):
            if num_map.get(crossing[i]) is None:
                assert AssertionError()
            crossing[i] = num_map[crossing[i]]
    return sorted(new_pd_code)

# 将 pd_code1 里面的 val_1 和 pd_code2 里面的 val_2 连接起来
def connected_sum(
    pd_code1:list[list], pd_code2:list[list], val_1, val_2) -> list[list]:
    
    # 如果有一个扭结平凡，则不需要连接
    if pd_code1 == [] or pd_code2 == []:
        return json.loads(json.dumps(pd_code1 + pd_code2))

    # 检查 pd_code 的弱合法性
    for pd_code in [pd_code1, pd_code2]:
        if not pd_code_sanity.sanity(pd_code):
            raise TypeError()
    
    # 检查 val_1 和 val_2 是否出现了
    lis_wrap_1 = [0]
    lis_wrap_2 = [0]
    lis_wrap = [lis_wrap_1, lis_wrap_2]
    for cnt_wrap, val_now, pd_now in [
        (lis_wrap_1, val_1, pd_code1),
        (lis_wrap_2, val_2, pd_code2)
    ]:
        for crossing in pd_now:
            for term in crossing:
                if term == val_now:
                    cnt_wrap[0] += 1
    
    # 检查出现次数是否正确
    for i in range(2):
        if lis_wrap[i][0] != 2:
            raise ValueError(f"val_{i+1} not in pd_code{i+1}")

    # 分别计算两个需要连接的地方
    # 是不是在一个 r1 crossing 上
    #   如果 has_val_x_cnt[0] != 2
    #     则说明，val_x 在一个 r1 crossing
    #     其中 x = 1 或者 2
    has_val_1_cnt = [0]
    has_val_2_cnt = [0]
    for pd_code_now, has_val_cnt, val_now in [
        (pd_code1, has_val_1_cnt, val_1),
        (pd_code2, has_val_2_cnt, val_2)
    ]:
        has_val_cnt[0] = count_crossing_exists(pd_code_now, val_now)

    vals = [val_1, val_2]
    for val_pos, pd_code_now, pd_code_other, has_cnt_now in [
            (0, pd_code1, pd_code2, has_val_1_cnt),
            (1, pd_code2, pd_code1, has_val_2_cnt),
        ]:
            if has_cnt_now[0] != 2:

                # 在同一个连通分量中
                # 找到一个出现在多个 crossing 中的编号
                vals_new = find_avaible_pos(pd_code_now, vals[val_pos])
                if vals_new is None:

                    # 遇到了 [a, b, b, a] 或者 [a, a, b, b] 之类的
                    # 直接删掉当前 components 然后 merge 即可
                    return del_component_and_merge(
                        pd_code_now, pd_code_other, vals[val_pos], vals[1-val_pos])
                
                vals[val_pos] = vals_new
    
    # 覆盖旧的元素
    val_1, val_2 = vals

    # 获取元素集合
    num_set_1 = add_prefix([get_num_set(pd_code1)], "a_")[0]
    num_set_2 = add_prefix([get_num_set(pd_code2)], "b_")[0]
    
    # 增加前缀编码
    pd_code1 = add_prefix(pd_code1, "a_")
    pd_code2 = add_prefix(pd_code2, "b_")

    # 由于不存在 nugatory crossing 和 r1 crossing
    # 所以两侧各有两个相关 crossing
    _, nxt1 = pd_code_pre_nxt.get_pre_nxt(pd_code1)
    _, nxt2 = pd_code_pre_nxt.get_pre_nxt(pd_code2)
    nxt = nxt1 | nxt2

    # 带有字母前缀的成分
    a_val_1 = f"a_{val_1}"
    b_val_2 = f"b_{val_2}"

    # 将两组 pd_code 合并
    # 需要注意 nxt[a_val_1] 和 pre[a_val_1] 可能相同
    # 所以要保证只替换一次
    suc_1 = False
    suc_2 = False
    new_pd_code = json.loads(json.dumps(pd_code1 + pd_code2))
    for crossing in new_pd_code:
        if not suc_1 and check_has2(crossing, a_val_1, nxt[a_val_1]):
            replace_val(crossing, a_val_1, b_val_2)
            suc_1 = True
        if not suc_2 and check_has2(crossing, b_val_2, nxt[b_val_2]):
            replace_val(crossing, b_val_2, a_val_1)
            suc_2 = True
        if suc_1 and suc_2:
            break

    # 调整前驱后继关系
    nxt[b_val_2] = nxt1[a_val_1]
    nxt[a_val_1] = nxt2[b_val_2]

    # 获得新的编号方式
    num_map = get_new_number_map(nxt, num_set_1 + num_set_2)
    for crossing in new_pd_code:
        for i in range(len(crossing)):
            if num_map.get(crossing[i]) is None:
                assert AssertionError()
            crossing[i] = num_map[crossing[i]]

    ans_pd_code = sorted(new_pd_code)
    if not pd_code_sanity.sanity(ans_pd_code):
        raise AssertionError()
    return ans_pd_code

if __name__ == "__main__":
    print(connected_sum([[1, 2, 2, 1]], [[1, 2, 2, 1]], 1, 1))
