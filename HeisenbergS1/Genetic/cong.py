from concurrent import futures
import numpy as np
import geneticMain
import netket as nk
seeds = np.random.randint(1,9999999,size=nk.MPI.size())
# with futures.ProcessPoolExecutor(max_workers=32) as executors:
#     wait_for = [executors.submit(geneticMain.test_hyper, seed) for seed in seeds]
geneticMain.test_hyper(seeds[nk.MPI.rank()])
print(str(nk.MPI.rank())+"-"+str(seeds[nk.MPI.rank()]))
