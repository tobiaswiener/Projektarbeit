import SamplerTests.load as load
import netket as nk

FOLDER = "SamplerTests/ersteTests"
FILE = ""
def main1():
    load.specs_runnable.run_file(FOLDER,FILE)
def Folder():
    load.specs_runnable.run_all_files(FOLDER)

if __name__ == "__main__":
    Folder()