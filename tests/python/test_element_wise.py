import taichi as ti
from taichi import approx
from random import random, randint, seed
import math


def _c_mod(a, b):
    return a - b * int(float(a) / b)


def rand(dtype):
    if ti.core.is_integral(dtype):
        return randint(1, 5)
    else:
        return float(randint(1, 5)) / 5


@ti.host_arch_only
def _test_matrix_element_wise_unary(dtype, n, m, ti_func, math_func):
    a = ti.Matrix(n, m, dt=ti.f32, shape=())
    u = ti.Matrix(n, m, dt=ti.f32, shape=())

    w = []
    for i in range(n * m):
        w.append(rand(dtype))

    for i in range(n):
        for j in range(m):
            u[None][i, j] = w[i * m + j]

    @ti.kernel
    def func():
        a[None] = ti_func(u[None])

    func()

    for i in range(n):
        for j in range(m):
            expected = math_func(w[i * m + j])
            assert a[None][i, j] == approx(expected)


@ti.host_arch_only
def _test_matrix_element_wise_binary(dtype, n, m, ti_func, math_func):
    a = ti.Matrix(n, m, dt=dtype, shape=())
    b = ti.Matrix(n, m, dt=dtype, shape=())
    c = ti.Matrix(n, m, dt=dtype, shape=())
    u1 = ti.Matrix(n, m, dt=dtype, shape=())
    u2 = ti.Matrix(n, m, dt=dtype, shape=())
    u3 = ti.var(dt=dtype, shape=())

    w1 = []
    w2 = []
    for i in range(n * m):
        w1.append(rand(dtype))
        w2.append(rand(dtype))

    w3 = rand(dtype)

    for i in range(n):
        for j in range(m):
            u1[None][i, j] = w1[i * m + j]
            u2[None][i, j] = w2[i * m + j]

    u3[None] = w3

    @ti.kernel
    def func():
        a[None] = ti_func(u1[None], u2[None])
        b[None] = ti_func(u1[None], u3[None])
        c[None] = ti_func(u3[None], u1[None])

    func()

    for i in range(n):
        for j in range(m):
            expected = math_func(w1[i * m + j], w2[i * m + j])
            assert a[None][i, j] == approx(expected)
            expected = math_func(w1[i * m + j], w3)
            assert b[None][i, j] == approx(expected)
            expected = math_func(w3, w1[i * m + j])
            assert c[None][i, j] == approx(expected)


def test_matrix_element_wise_binary():
    seed(666)
    for n, m in [(5, 4), (3, 1)]:
        _test_matrix_element_wise_binary(ti.f32, n, m, ti.atan2, math.atan2)
        _test_matrix_element_wise_binary(ti.f32, n, m, ti.min, min)
        _test_matrix_element_wise_binary(ti.i32, n, m, ti.min, min)
        _test_matrix_element_wise_binary(ti.f32, n, m, ti.max, max)
        _test_matrix_element_wise_binary(ti.i32, n, m, ti.max, max)
        _test_matrix_element_wise_binary(ti.f32, n, m, pow, pow)
        _test_matrix_element_wise_binary(ti.i32, n, m, pow, pow)
        _test_matrix_element_wise_binary(ti.i32, n, m, ti.raw_mod, _c_mod)


def test_matrix_element_wise_unary():
    seed(233)
    for n, m in [(5, 4), (3, 1)]:
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.sin, math.sin)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.cos, math.cos)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.tan, math.tan)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.asin, math.asin)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.acos, math.acos)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.tanh, math.tanh)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.sqrt, math.sqrt)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.exp, math.exp)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.log, math.log)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.ceil, math.ceil)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.floor, math.floor)
        _test_matrix_element_wise_unary(ti.f32, n, m, ti.abs, abs)
        _test_matrix_element_wise_unary(ti.i32, n, m, ti.abs, abs)
        # TODO(archibate): why ti.inv, ti.sqr doesn't work?
