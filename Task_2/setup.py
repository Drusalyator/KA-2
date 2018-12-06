from cx_Freeze import setup, Executable


includefiles = ['in.txt', 'out.txt']

setup(
    name = "task_2",
    version = "1.0",
    description = "Ford-Folkerson",
    options = {'build_exe': {'include_files':includefiles}},
    executables = [Executable("main.py")]
)