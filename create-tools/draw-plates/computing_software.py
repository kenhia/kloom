"""computing plates, segment "Software, shared", plus `cloud` (sprint 015). See plates_for.py."""
import hashlib
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _to(d, p, q, size=4, gap=0):
    """A straight line from p to q with an arrowhead at q, stopped `gap` short of it."""
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    qx, qy = q[0] - gap * math.cos(ang), q[1] - gap * math.sin(ang)
    d.line(p, (qx, qy))
    _arrow(d, qx, qy, ang, size)


def _box(d, x0, y0, x1, y1):
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def _dashed(d, x0, x1, y, dash=5, gap=4):
    """A horizontal dashed line, as one path of short segments."""
    segs, x = [], x0
    while x < x1:
        segs.append([(x, y), (min(x + dash, x1), y)])
        x += dash + gap
    d.lines(segs)


def unix():
    """The Unix file system: a path through directories to i-numbers, the i-list, one i-node's
    block addresses on the disk, and a special file, /dev/ppt, whose i-node leads to a device."""
    d = D()
    # the directory tree: (name, x, y, parent, is_dir)
    nodes = {
        '/': (58, 44, None, True),
        'bin': (24, 94, '/', True), 'dev': (58, 94, '/', True), 'usr': (98, 94, '/', True),
        'ppt': (44, 146, 'dev', False), 'tty': (72, 146, 'dev', False),
        'ken': (98, 146, 'usr', True),
        'paper': (98, 198, 'ken', False),
    }
    ilist_x0, ilist_x1, ilist_y0, slot = 150, 178, 36, 22
    inum = {'/': 1, 'bin': 2, 'dev': 3, 'usr': 4, 'ppt': 5, 'tty': 6, 'ken': 7, 'paper': 8}
    slot_y = lambda i: ilist_y0 + slot * (i - 1) + slot / 2
    # the i-node drawn open, and the disk's blocks
    ix0, ix1, iy0 = 214, 290, 150
    fields = ['MODE', 'SIZE'] + [f'ADDR {k}' for k in range(4)]
    fy = [iy0 + 14 * k for k in range(len(fields) + 1)]
    bx0, by0, bw, bh, cols, rows = 318, 40, 14, 12, 5, 16
    block = lambda c, r: (bx0 + c * bw, by0 + r * bh)
    used = [(1, 3), (3, 6), (0, 10), (2, 13)]  # the four blocks that hold `paper`

    # construction: each name carried across to its i-number; the disk's block grid
    d.group('thin')
    d.lines([[(x + 8, y), (ilist_x0, slot_y(inum[n]))] for n, (x, y, _, _) in nodes.items()])
    d.lines([[(bx0 + c * bw, by0), (bx0 + c * bw, by0 + rows * bh)] for c in range(cols + 1)])
    d.lines([[(bx0, by0 + r * bh), (bx0 + cols * bw, by0 + r * bh)] for r in range(rows + 1)])
    # the tree of directories: circles for directories, squares for files
    d.group()
    for n, (x, y, parent, is_dir) in nodes.items():
        if parent:
            px, py = nodes[parent][0], nodes[parent][1]
            d.line((px, py + 5), (x, y - 5))
        if is_dir:
            d.circle(x, y, 5)
        else:
            _box(d, x - 4.5, y - 4.5, x + 4.5, y + 4.5)
    # the i-list, and the i-node of `paper` opened out
    d.group()
    _box(d, ilist_x0, ilist_y0, ilist_x1, ilist_y0 + slot * 8)
    d.lines([[(ilist_x0, ilist_y0 + slot * k), (ilist_x1, ilist_y0 + slot * k)] for k in range(1, 8)])
    _box(d, ix0, fy[0], ix1, fy[-1])
    d.lines([[(ix0, y), (ix1, y)] for y in fy[1:-1]])
    # the i-list slot opened into the i-node; the address fields to their blocks
    d.group('mid')
    s8 = slot_y(8)
    d.line((ilist_x1, s8 - slot / 2), (ix0, fy[0]))
    d.line((ilist_x1, s8 + slot / 2), (ix0, fy[-1]))
    for k, (c, r) in enumerate(used):
        x, y = block(c, r)
        _to(d, (ix1, fy[2 + k] + 7), (x, y + bh / 2), size=3.5)
    # the special file's i-node points at no blocks, but at a device: a paper-tape punch
    d.group()
    for c, r in used:
        x, y = block(c, r)
        d.line((x + 3, y + 3), (x + bw - 3, y + bh - 3))
        d.line((x + 3, y + bh - 3), (x + bw - 3, y + 3))
    tx0, tx1, ty = 150, 300, 256
    d.line((tx0, ty - 11), (tx1, ty - 11))
    d.line((tx0, ty + 11), (tx1, ty + 11))
    d.group('mid')
    s5 = slot_y(5)
    d.line((ilist_x1, s5), (198, s5), (198, ty - 26))
    _to(d, (198, ty - 26), (198, ty - 13), size=3.5)
    holes = []
    for k in range(17):
        x = tx0 + 7 + k * 8.5
        code = (k * 37 + 11) % 32  # a five-hole code per row, and the small sprocket hole
        for bit in range(5):
            if code >> bit & 1:
                y = ty - 7.5 + bit * 3.6 + (1.8 if bit > 2 else 0)
                holes.append([(x - 1.3, y), (x + 1.3, y)])
        holes.append([(x - 0.5, ty + 3.3), (x + 0.5, ty + 3.3)])
    d.lines(holes)
    # labels
    d.group()
    for n, (x, y, _, is_dir) in nodes.items():
        if n != '/':
            d.text(x, y + 16, n, size=7)
    for n, i in inum.items():
        d.text(ilist_x1 - 7, slot_y(i) + 3, str(i), size=7)
    for f, y in zip(fields, fy):
        d.text(ix0 + 4, y + 10, f, size=6.5, anchor='start')
    d.text(164, 26, 'I-LIST', size=7)
    d.text(252, 140, 'I-NODE 8', size=7)
    d.text(349, 30, 'DISK BLOCKS', size=7)
    d.text(58, 30, '/usr/ken/paper', size=7)
    d.text(225, 284, '/dev/ppt · THE PAPER-TAPE PUNCH, WRITTEN AS A FILE', size=7)
    return d


def _tree(n_levels=3, x0=0, x1=160, y0=0, dy=62):
    """A binary tree's node positions, level by level, centred in [x0, x1]."""
    levels = []
    for lv in range(n_levels):
        k = 2 ** lv
        w = (x1 - x0) / k
        levels.append([(x0 + w * (i + 0.5), y0 + dy * lv) for i in range(k)])
    return levels


def free_software():
    """Two family trees of one program. Under a permissive licence a descendant may close its
    source, and its own descendants stay closed; under copyleft every descendant carries the
    source and the same licence."""
    d = D()
    left = _tree(3, 14, 186, 62)
    right = _tree(3, 214, 386, 62)
    closed = {(1, 1), (2, 2), (2, 3), (2, 0)}  # (level, index) of closed versions on the left
    w, h = 30, 26

    def node(x, y, open_, lic):
        _box(d, x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        if open_:
            # a page of source, with its folded corner and three lines of text
            px, py = x - 7, y - 9
            d.line((px, py), (px + 10, py), (px + 14, py + 4), (px + 14, py + 18), (px, py + 18), closed=True)
            d.line((px + 10, py), (px + 10, py + 4), (px + 14, py + 4))
            d.lines([[(px + 3, py + 8 + 3 * k), (px + 11, py + 8 + 3 * k)] for k in range(3)])
        else:
            # a sealed binary: the box hatched through
            segs = []
            for k in range(-4, 6):
                xa = x - w / 2 + k * 6
                p, q = (xa, y + h / 2), (xa + h, y - h / 2)
                # clip the diagonal to the box
                t0 = max(0, (x - w / 2 - p[0]) / (q[0] - p[0]))
                t1 = min(1, (x + w / 2 - p[0]) / (q[0] - p[0]))
                if t1 > t0:
                    segs.append([(p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0),
                                 (p[0] + (q[0] - p[0]) * t1, p[1] + (q[1] - p[1]) * t1)])
            d.lines(segs)
        if lic:
            d.circle(x + w / 2 - 1, y + h / 2 - 1, 4)

    # construction: the generations as rules across both trees
    d.group('thin')
    for lv in range(3):
        y = 62 + 62 * lv
        d.line((8, y), (392, y))
    d.line((200, 30), (200, 262))
    # the lines of descent
    d.group('mid')
    for tree in (left, right):
        for lv in (1, 2):
            for i, (x, y) in enumerate(tree[lv]):
                px, py = tree[lv - 1][i // 2]
                _to(d, (px, py + h / 2), (x, y - h / 2), size=3.5)
    # the versions
    d.group()
    for lv, row in enumerate(left):
        for i, (x, y) in enumerate(row):
            node(x, y, (lv, i) not in closed, False)
    d.group()
    for lv, row in enumerate(right):
        for i, (x, y) in enumerate(row):
            node(x, y, True, True)
    # labels
    d.group()
    d.text(100, 34, 'PERMISSIVE', size=8)
    d.text(300, 34, 'COPYLEFT · GNU GPL', size=8)
    d.text(100, 206 + 44, 'SOURCE MAY BE CLOSED', size=7)
    d.text(300, 206 + 44, 'SOURCE AND LICENCE TRAVEL', size=7)
    d.text(100, 272, '3 OF 7 VERSIONS OPEN', size=7)
    d.text(300, 272, '7 OF 7 VERSIONS OPEN', size=7)
    return d


def linux():
    """The Tanenbaum–Torvalds argument as two sections: a monolithic kernel (Linux), where a
    system call traps once into one privileged program, and a microkernel (MINIX), where files,
    memory and drivers are separate processes that pass messages through a small kernel."""
    d = D()
    line_y = 150  # the privilege boundary
    # left: monolithic
    L0, L1 = 16, 186
    R0, R1 = 214, 384
    procs_y = (60, 92)
    # construction: the privilege boundary across both, and the centre line
    d.group('thin')
    _dashed(d, 8, 392, line_y)
    d.line((200, 28), (200, 272))
    # user processes on both sides; the kernels
    d.group()
    for k in range(3):
        x = L0 + 8 + k * 56
        _box(d, x, procs_y[0], x + 44, procs_y[1])
    _box(d, L0, 176, L1, 256)  # the whole monolithic kernel
    # right: two user processes and three servers above the line, a small kernel below
    rx = [R0 + 4 + k * 58 for k in range(3)]
    _box(d, rx[0], procs_y[0], rx[0] + 50, procs_y[1])
    _box(d, rx[2], procs_y[0], rx[2] + 50, procs_y[1])
    sv_y = (104, 136)
    for k in range(3):
        _box(d, rx[k], sv_y[0], rx[k] + 50, sv_y[1])
    _box(d, R0 + 40, 196, R1 - 40, 236)
    # the monolithic kernel's parts, all in one address space
    d.group('mid')
    parts = ['SCHED', 'MEMORY', 'FILES', 'DRIVERS']
    pw = (L1 - L0 - 10) / 4
    for k in range(4):
        _box(d, L0 + 5 + k * pw + 2, 206, L0 + 5 + (k + 1) * pw - 2, 244)
    # the paths: a system call on the left; messages through the microkernel on the right
    d.group()
    x = L0 + 8 + 56 + 22
    _to(d, (x, procs_y[1]), (x, 204), size=4)
    kc = (R0 + R1) / 2
    fs = rx[1] + 25
    dv = rx[2] + 25
    p0 = rx[0] + 25
    path = [(p0, procs_y[1]), (kc - 30, 196), (fs, sv_y[1]), (kc, 196), (dv, sv_y[1])]
    for a, b in zip(path, path[1:]):
        _to(d, a, b, size=4)
    # labels
    d.group()
    for k, name in enumerate(['sh', 'gcc', 'bash']):
        d.text(L0 + 30 + k * 56, 80, name, size=7)
    d.text(rx[0] + 25, 80, 'sh', size=7)
    d.text(rx[2] + 25, 80, 'cc', size=7)
    for k, name in enumerate(['MM', 'FS', 'DISK']):
        d.text(rx[k] + 25, 124, name, size=7)
    for k, name in enumerate(parts):
        d.text(L0 + 5 + (k + 0.5) * pw, 228, name, size=6)
    d.text(kc, 219, 'KERNEL', size=7)
    d.text(101, 34, 'MONOLITHIC · LINUX', size=8)
    d.text(299, 34, 'MICROKERNEL · MINIX', size=8)
    d.text(392, line_y - 4, 'USER', size=6, anchor='end')
    d.text(392, line_y + 10, 'KERNEL', size=6, anchor='end')
    d.text(x + 6, 172, 'TRAP', size=6, anchor='start')
    d.text(299, 256, 'MESSAGES', size=6)
    d.text(101, 272, 'ONE PROGRAM, ONE ADDRESS SPACE', size=7)
    d.text(299, 272, 'SERVERS OUTSIDE THE KERNEL', size=7)
    return d


def open_source():
    """Git's history as a graph: each commit names its parent by the hash of its contents, a
    branch leaves the main line and a merge commit with two parents brings it back; above, one
    commit opened into its tree of files."""
    d = D()
    main_y, br_y = 212, 160
    xs = [28 + 44 * k for k in range(9)]
    # main line commits 0..8; a branch forks after main[2] and merges at main[6]
    branch = [(xs[3] + 22, br_y), (xs[4] + 22, br_y), (xs[5] + 22, br_y)]
    commits = [(x, main_y) for x in xs]
    h = lambda s: hashlib.sha1(s.encode()).hexdigest()[:4]
    r = 9
    # construction: the time axis, and the fork and merge points projected down
    d.group('thin')
    d.line((14, 262), (392, 262))
    d.lines([[(x, main_y + r), (x, 262)] for x in xs])
    # the commits
    d.group()
    for x, y in commits + branch:
        d.circle(x, y, r)
    # each commit points back to its parent (the arrow runs from child to parent)
    d.group('mid')
    for (x0, y0), (x1, y1) in zip(commits, commits[1:]):
        _to(d, (x1 - r, y1), (x0, y0), size=3.5, gap=r + 0.5)
    _to(d, branch[0], commits[2], size=3.5, gap=r + 0.5)
    for a, b in zip(branch[1:], branch):
        _to(d, a, b, size=3.5, gap=r + 0.5)
    _to(d, commits[6], branch[2], size=3.5, gap=r + 0.5)
    # the merge commit, drawn doubled: it has two parents
    d.group()
    d.circle(commits[6][0], main_y, r - 3.5)
    # one commit opened out into its tree and the files (blobs) it names
    cx, cy = branch[1]
    top = 44
    tb = (cx - 26, top, cx + 26, top + 26)
    blobs = [(cx - 96 + 64 * k, top + 64) for k in range(4)]
    d.group('mid')
    d.line((cx, cy - r), (cx, top + 26 + 8))
    _box(d, *tb)
    for bx, by in blobs:
        _box(d, bx - 25, by, bx + 25, by + 20)
        _to(d, (cx, top + 26), (bx, by), size=3.5)
    # labels
    d.group()
    for k, (x, y) in enumerate(commits):
        d.text(x, main_y + 24, h(f'main {k}'), size=6)
    for k, (x, y) in enumerate(branch):
        d.text(x, br_y - 14, h(f'topic {k}'), size=6)
    d.text(cx, top + 17, 'TREE', size=7)
    for (bx, by), name in zip(blobs, ['README', 'Makefile', 'main.c', 'lib.c']):
        d.text(bx, by + 13, name, size=6)
    d.text(xs[6] + 16, main_y - 14, 'MERGE', size=6, anchor='start')
    d.text(392, 276, 'EACH COMMIT NAMES ITS PARENT BY HASH', size=7, anchor='end')
    d.text(branch[0][0] - 14, br_y - 14, 'BRANCH', size=6, anchor='end')
    d.text(14, main_y - 14, 'MAIN', size=6, anchor='start')
    return d


def cloud():
    """A computer divided by a hypervisor: three virtual machines, each with its own operating
    system, over one set of hardware; a guest's privileged instruction traps to the hypervisor,
    which emulates it and returns."""
    d = D()
    X0, X1 = 30, 370
    hw = (232, 268)
    hv = (196, 224)
    vm_w, gap = 100, 20
    vms = [X0 + k * (vm_w + gap) for k in range(3)]
    os_y = (150, 182)
    app_y = (70, 138)
    # construction: the layers carried across, and each VM's outline
    d.group('thin')
    for y in (hw[0], hv[0], os_y[0], app_y[0]):
        d.line((12, y), (388, y))
    for x in vms:
        _box(d, x - 4, app_y[0] - 8, x + vm_w + 4, os_y[1] + 6)
    # hardware and hypervisor
    d.group()
    _box(d, X0, hw[0], X1, hw[1])
    _box(d, X0, hv[0], X1, hv[1])
    # each VM: a guest OS and its applications
    d.group()
    for x in vms:
        _box(d, x, os_y[0], x + vm_w, os_y[1])
        for k in range(3):
            ax = x + 4 + k * 32
            _box(d, ax, app_y[0] + 30, ax + 28, app_y[1])
    # the hardware's parts
    d.group('mid')
    parts = ['CPU', 'MEMORY', 'DISK', 'NETWORK']
    pw = (X1 - X0 - 20) / 4
    for k in range(4):
        _box(d, X0 + 10 + k * pw + 4, hw[0] + 6, X0 + 10 + (k + 1) * pw - 4, hw[1] - 6)
    # trap and emulate, in the middle VM
    d.group()
    tx = vms[1] + 8
    _to(d, (tx, os_y[1]), (tx, hv[0] + 12), size=4)
    _to(d, (tx + 32, hv[0] + 12), (tx + 32, os_y[1]), size=4)
    d.arc(tx + 16, hv[0] + 12, 16, 180, 0, n=24)
    # labels
    d.group()
    for k, x in enumerate(vms):
        d.text(x + vm_w / 2, os_y[0] + 20, 'GUEST OS', size=7)
        d.text(x + vm_w / 2, app_y[0] + 18, f'VM {k + 1}', size=7)
    d.text(vms[2] + vm_w / 2, hv[0] + 18, 'HYPERVISOR', size=7)
    for k, p in enumerate(parts):
        d.text(X0 + 10 + (k + 0.5) * pw, hw[0] + 21, p, size=6.5)
    d.text(tx - 4, os_y[1] + 12, 'TRAP', size=6, anchor='end')
    d.text(tx + 36, os_y[1] + 12, 'RETURN', size=6, anchor='start')
    d.text(200, 34, 'ONE MACHINE, THREE MACHINES · TRAP AND EMULATE', size=8)
    d.text(200, 290, 'CP/CMS, 1967 · VMWARE, 1999 · XEN UNDER EC2, 2006', size=7)
    return d


PLATES = {'unix': unix, 'free-software': free_software, 'linux': linux,
          'open-source': open_source, 'cloud': cloud}
