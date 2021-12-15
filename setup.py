import cx_Freeze

__version__ = "1.0.0"

with open("first_run.txt", "w", encoding="utf-8") as file:
    file.write("first run")

executables = [
    cx_Freeze.Executable(
        script=r"main.py",
        base="Win32GUI",
        targetName="TimeFork.exe",
        icon=r"\photos\icon.ico",
    )
]
excludes = [
    "test",
    "tkinter",
    "lib2to3",
    "pydoc_data",
    "pkg_resources",
    "idna",
    "asyncio",
    "requests",
    "unittest",
    "urllib3",
    "concurrent",
    "packaging",
    "openpyxl",
    "et_xmlfile",
    "email",
    "http",
    "html",
    "distutils",
    "multiprocessing",
    "xmlrpc",
    "wsgiref",
    "werkzeug",
    "xml",
    "werkzeug",
    "itsdangerous",
]
zip_include_packages = [
    "collections",
    "encodings",
    "importlib",
    "json",
    "click",
    "ctypes",
    "logging",
    "urllib",
    "threading",
    "sqlite3_api",
    "sqlite3",
    "interpretare.py",
]

cx_Freeze.setup(
    name="TimeFork",
    options={
        "build_exe": {
            "packages": ["PyQt5", "pyperclip"],
            "include_files": ["first_run.txt", "photos", "interpretare.py"],
            "excludes": excludes,
            "zip_include_packages": zip_include_packages,
        },
    },
    version=__version__,
    description="TimeFork - движок для создания и интерпретации текстовых квестов",
    author="StrayGuy",
    executables=executables,
)

