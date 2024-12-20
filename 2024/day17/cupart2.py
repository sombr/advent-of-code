#!/usr/bin/python3

import numpy
from numba import cuda

@cuda.jit
def run_program(offset, expect, output_array):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    if pos < output_array.size:  # Check array boundaries
        op = 0
        a = pos + offset
        while a > 0 and op < len(expect):
            b = (a % 8) ^ 2
            c = a // (1<<b)
            b = b ^ 3 ^ c
            out = b % 8
            if op < len(expect) and expect[op] != out:
                break
            op += 1
            a = a // 8

        res = 0
        if a == 0 and op == len(expect):
            res = 1
        cuda.syncthreads()
        output_array[pos] = res

def main():
    print(cuda.gpus)
    expect = numpy.asarray((2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0))

    for offset in range(922337203):
        span = 10_000_000_000
        start = 37214372088832 + span * offset
        print(f">>> start: {start}")
        out = cuda.device_array((span), dtype=numpy.byte)

        # Set the number of threads in a block
        threadsperblock = 64

        # Calculate the number of thread blocks in the grid
        blockspergrid = (out.size + (threadsperblock - 1)) // threadsperblock

        # Now start the kernel
        run_program[blockspergrid, threadsperblock](start, expect, out)
        res = out.copy_to_host()

        nonz = numpy.nonzero(res)[0]
        if len(nonz) > 0:
            print("offset >> ", offset)
            print("idx >> ", nonz[0])
            print("start + idx", start + nonz[0])
            break

main()
