import taichi as ti
import taichi as tc

tc.set_gdb_trigger(True)

val = ti.var(ti.i32)
f = ti.var(ti.f32)

ti.cfg.use_llvm = True
ti.cfg.arch = ti.cuda
# ti.cfg.print_ir = True
ti.cfg.print_kernel_llvm_ir = True

n = 32

@ti.layout
def values():
  ti.root.dense(ti.i, 4).dense(ti.i, 2).place(val, f)

@ti.kernel
def test():
  for i in range(256):
    ti.print(i)
    s = 0
    for j in range(10):
      s += j
    a = ti.Vector([0.4, 0.3])
    val[i] = s + ti.cast(a.norm() * 100, ti.i32)
    ti.print(val[i])
    f[i] = ti.sin(ti.cast(i, ti.f32))
    ti.print(f[i])

for i in range(1):
  test()
for i in range(100):
  print(i, val[i], f[i])