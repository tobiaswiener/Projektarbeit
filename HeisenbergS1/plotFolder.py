import plot
import os.path


folder = "SamplerTests/ersteTests/"
filenameList=[]
for filename in os.listdir(folder):
    if filename.endswith(".log"):
        filenameList.append(filename)
    else:
        continue
plot.SubPlotFromFile(filenameList, folder)