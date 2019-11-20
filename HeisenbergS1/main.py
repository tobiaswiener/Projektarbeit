import SamplerTests.load as load


FOLDER = "SamplerTests/ersteTests"

def main1():
    load.specs_runnable.run_file(FOLDER,"30_FFNN_AdaMax_MetropolisHop1.ip")
def Folder():

    load.specs_runnable.run_all_files(FOLDER)


if __name__ == "__main__":
    Folder()